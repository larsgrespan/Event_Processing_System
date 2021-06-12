# Helper script to delete the database collections
import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017' , replicaSet='rs1')
client.drop_database('EventDB')
client.drop_database('ResultDB')
client.drop_database('PreprocessDB')