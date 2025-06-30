import logging
from influxdb import InfluxDBClient
from influxdb import DataFrameClient



def get_influxdb_client(db_host, db_port, username, password, db_name):
    """Return a configured :class:`InfluxDBClient` instance.

    Parameters
    ----------
    db_host : str
        Hostname or IP address of the InfluxDB server.
    db_port : int
        Port on which the InfluxDB server is listening.
    username : str
        Username used for authentication.
    password : str
        Password used for authentication.
    db_name : str
        Name of the database to connect to.

    Returns
    -------
    InfluxDBClient
        Client object representing the connection.

    Raises
    ------
    Exception
        If the connection attempt fails.
    """




    try:
        client = InfluxDBClient(host=db_host,port=db_port,username=username,password=password, database=db_name)
        return client
    except Exception as e:
        logging.error("Error in get_influxdb_client: %s" %str(e))
        raise Exception("Error in get_influxdb_client: %s" %str(e))
       
def closeConexion(conexion):
    """Close an open database connection."""
    conexion.close()

        

def get_influx_DF_client(host, port, user, passw, db_name):
    """Return a :class:`DataFrameClient` configured with the provided parameters.

    Parameters
    ----------
    host : str
        InfluxDB server address.
    port : int
        Port of the InfluxDB server.
    user : str
        Username used for authentication.
    passw : str
        Password used for authentication.
    db_name : str
        Name of the database.

    Returns
    -------
    DataFrameClient
        Configured DataFrame client.

    Raises
    ------
    Exception
        If the client cannot be created.
    """
    try:
        return DataFrameClient(host=host,port=port, username=user,password=passw,database=db_name)

    except Exception as e:
        raise Exception("Error creating influxdb DataFrame client: %s" %str(e))




