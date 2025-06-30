import logging
from pymongo import MongoClient


def get_mongo_client(db_host, db_port, username=None, password=None, db_name=None):
    """Return a configured :class:`MongoClient` and the selected database.

    Parameters
    ----------
    db_host : str
        MongoDB server address.
    db_port : int
        Port number on which MongoDB is listening.
    username : str, optional
        Username for authentication if required.
    password : str, optional
        Password for authentication if required.
    db_name : str, optional
        Name of the database to return. If ``None``, only the client is
        returned.

    Returns
    -------
    tuple(MongoClient, Database or None)
        A ``MongoClient`` instance and, if ``db_name`` is provided, the
        associated database object.

    Raises
    ------
    Exception
        If the connection cannot be established.
    """
    try:
        client = MongoClient(host=db_host, port=db_port,
                             username=username, password=password)
        database = client[db_name] if db_name else None
        return client, database
    except Exception as exc:
        logging.error("Error creating MongoDB client: %s", exc)
        raise Exception(f"Error creating MongoDB client: {exc}")


def insert_into_mongo(database, collection_name, data):
    """Insert a document or list of documents into a MongoDB collection.

    Parameters
    ----------
    database : Database
        MongoDB database instance where the data will be inserted.
    collection_name : str
        Target collection name.
    data : dict or list[dict]
        Document or list of documents to insert.

    Returns
    -------
    InsertOneResult or InsertManyResult
        Result from the insert operation.

    Raises
    ------
    Exception
        If the insertion fails.
    """
    try:
        collection = database[collection_name]
        if isinstance(data, list):
            return collection.insert_many(data)
        return collection.insert_one(data)
    except Exception as exc:
        logging.error("Error inserting into MongoDB: %s", exc)
        raise Exception(f"Error inserting into MongoDB: {exc}")
