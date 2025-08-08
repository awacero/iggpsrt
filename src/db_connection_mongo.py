from pymongo import MongoClient, errors
from urllib.parse import quote_plus
import logging
from datetime import datetime
 

def connect_to_mongodb(user, password, host, port, database,collection_name, timeout_ms=5000):
    """
    Connects to a MongoDB instance and returns the database object.

    :param user: MongoDB username
    :param password: MongoDB password
    :param host: MongoDB host address
    :param port: MongoDB port
    :param database: Database name
    :param timeout_ms: Connection timeout in milliseconds (default 5000ms)
    :return: Database object (db)
    """
    uri = f"mongodb://{quote_plus(user)}:{quote_plus(password)}@{host}:{port}/{database}"
    
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=timeout_ms)
        # Force a call to the server to ensure connection
        client.admin.command("ping")
        logging.error(f"Connected successfully to MongoDB at {host}:{port}")
        return client[database][collection_name]
    except errors.ServerSelectionTimeoutError as e:
        logging.error(f"Connection timeout: {e}")
    except errors.OperationFailure as e:
        logging.error(f"Authentication failed: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    return None



def send_to_mongo(data, mongo_collection):
    """
    Write structured GPS data to a MongoDB collection.

    Parameters
    ----------
    data : dict
        Dictionary with ordered GPS information.
    mongo_collection : pymongo.collection.Collection
        MongoDB collection instance where the data will be inserted.
    """
    try:
        # Prepare the document for MongoDB
        document = {
            "site_id": data.get("site_id", "UNKNOWN"),
            "gps_datetime": data["gps_datetime"],
            "satellite_number": data["satellite_number"],
            "position": {
                "x": data["position_x"],
                "y": data["position_y"],
                "z": data["position_z"],
                "e": data["position_e"],
                "n": data["position_n"],
                "u": data["position_u"]
            },
            "inserted_at": datetime.utcnow()
        }

        # Insert the document into MongoDB
        mongo_collection.insert_one(document)
        logging.debug(f"Data sent to MongoDB: {document}")
        print((f"Data sent to MongoDB: {document}"))

    except Exception as e:
        logging.error(f"Error sending to MongoDB: {e}")
