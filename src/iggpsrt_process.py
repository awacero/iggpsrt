import subprocess
import time
import multiprocessing
from datetime import datetime, timedelta
import logging



def start_listener(host, eryo_command, max_retries, influx_client):
    """Start a listener process with retry logic.

    Parameters
    ----------
    host : str
        Host identifier of the listener.
    eryo_command : str
        Command used to spawn the listener.
    max_retries : int
        Maximum number of restart attempts.
    influx_client : InfluxDBClient
        Client used for writing data to InfluxDB.
    """
    retries = 0
    while retries < max_retries:
        if run_process(host, eryo_command,influx_client):
            return  # Exit loop on success
        retries += 1
        time.sleep(2 ** retries)  # Exponential backoff

    logging.critical(f"Max retries reached for {host}:{eryo_command}. Exiting.")


def run_process(host, eryo_command, influx_client):
    """Execute a command and handle its output.

    Parameters
    ----------
    host : str
        Host identifier of the listener.
    eryo_command : str
        Command string to execute.
    influx_client : InfluxDBClient
        Client used for writing data.

    Returns
    -------
    bool
        ``True`` on success, ``False`` otherwise.
    """
    try:
        logging.info(f"Starting listener for {host}:{eryo_command}")
        ##process = subprocess.Popen(eryo_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        process = subprocess.Popen(eryo_command, shell=True, text=True, stdout=subprocess.PIPE)

        process_output(process, host, eryo_command,influx_client)
        process.wait()

        if process.returncode != 0:
            log_error(process, host, eryo_command)
            return False  # Indicate failure
        return True  # Indicate success

    except Exception as e:
        logging.error(f"Unexpected error for {host}:{eryo_command}: {e}")
        return False


def process_output(process, host, eryo_command, influx_client):
    """Parse lines from the running process and send complete data to InfluxDB.

    Parameters
    ----------
    process : subprocess.Popen
        Running process producing the output.
    host : str
        Host identifier of the listener.
    eryo_command : str
        Command executed.
    influx_client : InfluxDBClient
        Client used for writing parsed data.
    """
    collected_data = {}

    for line in process.stdout:        
        if line.strip():
            parsed_data = parse_line(line.strip())
            if parsed_data:
                
                collected_data.update(parsed_data)
                if is_data_complete(collected_data):
                    ##Modify the dictionary that will be send to influx
                    ## xyz metros ??, sat number, realtime enu en centimetros, REAL time
                    collected_data["gps_datetime"]=gps_to_utc(collected_data['gps_week'],collected_data['gps_millisecond']) 

                    temp_dict =order_gps_data(collected_data)
                    send_to_influx(temp_dict,influx_client)
                    collected_data.clear()
                
        else:
            logging.warning(f"Empty response received from {host}:{eryo_command}")

def order_gps_data(collected_data):
    """Reformat collected data to the structure expected by InfluxDB."""

    gps_data = {}
    gps_data['site_id'] = collected_data['site_id']
    gps_data['position_x'] = collected_data['xyz'][0]
    gps_data['position_y'] = collected_data['xyz'][1]
    gps_data['position_z'] = collected_data['xyz'][2]
    gps_data['satellite_number'] = collected_data['satellite_number']
    gps_data['position_e'] = collected_data['enu'][0]
    gps_data['position_n'] = collected_data['enu'][1]
    gps_data['position_u'] = collected_data['enu'][2]
    gps_data['gps_datetime'] = collected_data['gps_datetime']



    return gps_data 




def parse_line(line):
    """Return a dictionary with data parsed from a listener line.

    Parameters
    ----------
    line : str
        Raw output line from the listener process.

    Returns
    -------
    dict
        Parsed values or an empty dictionary if the line is not recognized.
    """
    if "=" not in line:
        return {}

    key, value = map(str.strip, line.split("=", 1))
    if key == "site_id":
        return {"site_id": value}
    elif key == "gps_week":
        return {"gps_week": int(value)}
    elif key == "gps_millisecond":
        return {"gps_millisecond": int(value)}
    elif "Real-time XYZ" in key:
        return {"xyz": tuple(map(float, value.split(",")))}
    elif key == "Satellite number":
        return {"satellite_number": int(value)}
    elif "Real-time ENU" in key:
        return {"enu": tuple(map(float, value.split(",")))}
    return {}


def is_data_complete(data):
    """Return ``True`` if all required fields are present.

    Parameters
    ----------
    data : dict
        Dictionary with parsed values.

    Returns
    -------
    bool
        ``True`` when all mandatory keys exist, ``False`` otherwise.
    """
    required_keys = {"site_id", "gps_week", "gps_millisecond", "xyz", "enu", "satellite_number"}
    return required_keys.issubset(data.keys())


def gps_to_utc(gps_week, gps_millisecond):
    """Convert GPS week and milliseconds to a UTC timestamp in nanoseconds.

    Parameters
    ----------
    gps_week : int
        GPS week number since the epoch (1980-01-06).
    gps_millisecond : int
        Milliseconds within the GPS week.

    Returns
    -------
    int
        UTC timestamp expressed in nanoseconds.
    """
    # Define the GPS epoch (January 6, 1980)
    gps_epoch = datetime(1980, 1, 6)
    
    # Calculate the total number of seconds since the GPS epoch
    total_seconds = gps_week * 7 * 24 * 3600 + gps_millisecond / 1000.0
    
    # Add the total seconds to the GPS epoch
    utc_time = gps_epoch + timedelta(seconds=total_seconds)

    timestamp_ns = int(utc_time.timestamp()) * 1_000_000_000    
    return timestamp_ns




def send_to_influx(data, influx_client):
    """Write structured GPS data to InfluxDB.

    Parameters
    ----------
    data : dict
        Dictionary with ordered GPS information.
    influx_client : InfluxDBClient
        Client instance used to write points.
    """
    try:
        # Create a JSON payload for InfluxDB 1.x
        json_body = [
            {
                "measurement": "gps_position",
                "tags": {
                    "site": data.get("site_id", "UNKNOWN")
                },
                "fields": {
                    "gps_datetime": data["gps_datetime"],
                    "satellite_number": data["satellite_number"],
                    "position_x": data["position_x"],
                    "position_y": data["position_y"],
                    "position_z": data["position_z"],
                    "position_e": data["position_e"],
                    "position_n": data["position_n"],
                    "position_u": data["position_u"]
                }
            }
        ]

        # Write the data to InfluxDB
        influx_client.write_points(json_body)
        logging.debug(f"Data sent to InfluxDB: {data}")

    except Exception as e:
        logging.error(f"Error sending to InfluxDB: {e}")



def log_error(process, host, eryo_command):
    """Log standard error output from a failed process.

    Parameters
    ----------
    process : subprocess.Popen
        Process object that produced the error.
    host : str
        Host identifier of the listener.
    eryo_command : str
        Command that was executed.
    """
    stderr_output = process.stderr.read()
    logging.error(f"Process error for {host}:{eryo_command}: {stderr_output}")


def start_all_listeners(listeners, influx_client):
    """Launch multiple listener processes concurrently.

    Parameters
    ----------
    listeners : list[tuple[str, str]]
        Iterable of ``(host, command)`` pairs.
    influx_client : InfluxDBClient
        Client used for writing data.
    """
    max_retries = 5
    processes = []
    for host, eryo_command in listeners:
        p = multiprocessing.Process(target=start_listener, args=(host, eryo_command,max_retries,influx_client))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

