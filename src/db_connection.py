import logging
from influxdb import InfluxDBClient
from influxdb import DataFrameClient

from pymongo import MongoClient

def get_mongodb_client(host, port, username, password, db_name, auth_source='admin'):
    """
    Create a client connection to a MongoDB database.
    """
    try:
        uri = f"mongodb://{username}:{password}@{host}:{port}/{db_name}?authSource={auth_source}"
        client = MongoClient(uri)
        return client[db_name]  # Return the DB object directly
    except Exception as e:
        logging.error(f"Error connecting to MongoDB: {e}")
        raise





def get_influxdb_client(db_host, db_port,username,password,db_name):

    """
    Create a client connection to an InfluxDB database.

    This function initializes a connection to an InfluxDB database using the specified 
    connection parameters. It employs the InfluxDBClient for creating this connection.

    :param str db_host: The hostname or IP address of the InfluxDB server.
    :param int db_port: The port number on which the InfluxDB server is listening.
    :param str username: The username used to authenticate with the InfluxDB.
    :param str password: The password used to authenticate with the InfluxDB.
    :param str db_name: The name of the database to connect to in InfluxDB.
    :return: A client object representing the connection to the InfluxDB.
    :rtype: InfluxDBClient
    :raises Exception: If the connection attempt fails, an exception is raised 
                       with a descriptive error message.

    Example usage:
    >>> client = get_influxdb_client('localhost', 8086, 'user', 'password', 'myDatabase')
    """




    try:
        client = InfluxDBClient(host=db_host,port=db_port,username=username,password=password, database=db_name)
        return client
    except Exception as e:
        logging.error("Error in get_influxdb_client: %s" %str(e))
        raise Exception("Error in get_influxdb_client: %s" %str(e))
       
def closeConexion(conexion):
    conexion.close()

        

def get_influx_DF_client(host,port,user,passw,db_name):
    """  
    Obtiene un cliente influx
    
    :param string host: ip del servidor
    :param string port: puerto del servidor
    :param string user: usuario 
    :param string passw: contrasena
    :param string db_name: nombre de la base de datos 
    :return InfluxDBClient
    :Raises Exception e: error al crear el cliente influx
    """
    try:
        return DataFrameClient(host=host,port=port, username=user,password=passw,database=db_name)

    except Exception as e:
        raise Exception("Error creating influxdb DataFrame client: %s" %str(e))


