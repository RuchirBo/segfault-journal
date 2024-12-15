import os
import pymongo as pm

LOCAL = "0"
CLOUD = "1"

SEGFAULT_DB = 'segfaultDB'

client = None

MONGO_ID = '_id'


def connect_db():
    global client
    if client is None:  # not connected yet!
        print("Setting client because it is None.")
        if os.environ.get("CLOUD_MONGO", LOCAL) == CLOUD:
            password = os.environ.get("MONGO_PW")
            if not password:
                raise ValueError('You must set your password '
                                 + 'to use Mongo in the cloud.')
            print("Connecting to Mongo in the cloud.")
            try:
                client = pm.MongoClient(
                    f'mongodb+srv://segfaulter:{password}'
                    '@swe.fcpo7.mongodb.net/'
                    '?retryWrites=true'
                    '&w=majority'
                    '&appName=SWE',
                    tls=True,
                    tlsAllowInvalidCertificates=True,
                    serverSelectionTimeoutMS=5000,
                    connectTimeoutMS=30000,
                    socketTimeoutMS=None,
                    connect=False,
                    maxPoolsize=1
                )
                client.admin.command('ping')
                print("Successfully connected to MongoDB!")
            except Exception as e:
                print(f"Connection error: {e}")
                raise
        else:
            print("Connecting to Mongo locally.")
            client = pm.MongoClient()
    return client


def create(collection, doc, db=SEGFAULT_DB):
    """
    Insert a single doc into collection.
    """
    print(f'{db=}')
    return client[db][collection].insert_one(doc)


def fetch_one(collection, filt, db=SEGFAULT_DB):
    """
    Find with a filter and return on the first doc found.
    Return None if not found.
    """
    for doc in client[db][collection].find(filt):
        convert_mongo_id(doc)
        return doc


def convert_mongo_id(doc: dict):
    if MONGO_ID in doc:
        # Convert mongo ID to a string so it works as JSON
        doc[MONGO_ID] = str(doc[MONGO_ID])


def update(collection, filters, update_dict, db=SEGFAULT_DB):
    return client[db][collection].update_one(filters, update_dict)


def read(collection, db=SEGFAULT_DB, no_id=True) -> list:
    ret = []
    for doc in client[db][collection].find():
        if no_id:
            del doc[MONGO_ID]
        else:
            convert_mongo_id(doc)
        ret.append(doc)
    return ret


def read_dict(collection, key, db=SEGFAULT_DB, no_id=True) -> dict:
    recs = read(collection, db=db, no_id=no_id)
    recs_as_dict = {}
    for rec in recs:
        recs_as_dict[rec[key]] = rec
    return recs_as_dict


# def delete(collection, filt, db=SEGFAULT_DB):
#     """
#     Delete a document from the collection.
#     """
#     print(f'{filt=}')
#     del_result = client[db][collection].delete_one(filt)
#     return del_result.deleted_count

def delete(collection, filt, db=SEGFAULT_DB):
    """
    Delete documents from the collection.
    If the filter is empty, it deletes all documents in the collection.
    """
    print(f'{filt=}')
    del_result = client[db][collection].delete_many(filt)
    return del_result.deleted_count
