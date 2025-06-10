import logging
import logging.config
import argparse
import sys
import subprocess

from src import iggpsrt_process
from src import iggpsrt_configure
from src import iggpsrt_utils
from src import db_connection

# Configure logging
logging.basicConfig(filename="listener.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def main(args):

    configuration_file = args.iggpsrt_config

    try:
        
        if iggpsrt_utils.check_file_exists(configuration_file):
            logger.info(f"Configuration file {configuration_file} exists")
        else:
            logger.info(f"Configuration file {configuration_file} DOES NOT exists. Exit")
            sys.exit(-1)
    except Exception as e:
        logger.error(f"Error checking configuration  file: {e}" )
        raise Exception(f"Error checking configuration file: {e}" )
   

    try:
        config = iggpsrt_utils.load_yaml_config(configuration_file)
        if config:
            logger.info(f"Configuration file {configuration_file} content ok")
            listeners = list(config['listeners'].items())
            db_config_file = config['influx_db']['database_config_file']
            db_id = config['influx_db']['db_id']

        else:
            logger.info(f"Configuration file {configuration_file} content NOT OK. Exit")
            sys.exit(-1)
        
    except Exception as e:
        logger.error(f"Error reading configuration  file: {e}" )
        raise Exception(f"Error reading configuration file: {e}" )
   

    try:
        if iggpsrt_utils.check_file_exists(db_config_file):
            logger.info(f"DB configuration file {db_config_file} exists")
        else:
            logger.info(f"DB configuration file {db_config_file} DOES NOT exists. Exit")
            sys.exit(-1)
    except Exception as e:
        logger.error(f"Error checking configuration  file: {e}" )
        raise Exception(f"Error checking configuration file: {e}" )
   
    try:
        db_param = iggpsrt_utils.load_json_config(db_config_file)
        if db_param:
            db_param = db_param[db_id]
            print(db_param)
    except Exception as e:
        logger.error(f"Error reading configuration  file: {e}" )
        raise Exception(f"Error reading configuration file: {e}" )
   

    try:

        influx_client = db_connection.get_influxdb_client(db_host=db_param['host'],db_port=db_param['port'],
                                        username= db_param['user'], password=db_param['pass'],
                                        db_name=db_param['DBName'])
        print(influx_client)
    except Exception as e:
        logger.error(f"Error creating influx client: {e}" )
        raise Exception(f"Error creating influx client: {e}" )


    try:
        iggpsrt_process.start_all_listeners(listeners,influx_client)

    except Exception as e:
        logger.error(f"Error starting listeners: {e}" )
        raise Exception(f"Error starting listeners: {e}" )
   


if __name__ == "__main__":

    logger = iggpsrt_configure.configure_logging()
    logger.info("Logging configurated")

    parser = argparse.ArgumentParser(description="Will use default config found in ./config/config.yaml")
    parser.add_argument("--iggpsrt_config",type=str,default="./config/config.yaml",help="Yaml file with site, host and port")
    args = parser.parse_args()

    logger.info(f"iggpsrt config set to:{args.iggpsrt_config}")

    main(args)
    '''
    influx_client = get_influxdb_client(db_host=INFLUXDB_HOST,db_port=INFLUXDB_PORT,
                                        username= INFLUXDB_USER, password=INFLUXDB_PASSWORD,
                                        db_name=INFLUXDB_DATABASE)
    
    start_all_listeners()
    '''
