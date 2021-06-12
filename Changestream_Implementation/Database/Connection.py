import pymongo

# Class for mongodb connection
class DBConnections:

# Get event_db connection
    def get_event_db():
    
        client = pymongo.MongoClient('mongodb://127.0.0.1:27017', replicaSet='rs1')
        eventdb = client['EventDB']

        return eventdb
