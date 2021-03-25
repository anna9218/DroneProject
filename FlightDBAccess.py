# import sqlite3
# import os
#
# DB_NAME = 'flights_db.db'
#
#
# # Create a function to connect to a database with SQLite
#
# def sqlite_connect():
#     """Connect to a database if exists. Create an instance if otherwise.
#     Args:
#         db_name: The name of the database to connect
#     Returns:
#         an sqlite3.connection object
#     """
#     try:
#         # Create a connection
#         conn = sqlite3.connect(DB_NAME)
#     except sqlite3.Error:
#         print(f"Error connecting to the database '{DB_NAME}'")
#     finally:
#         return conn
#
#
# def execute_query(query: str):
#     connection = sqlite_connect()
#     cursor = connection.cursor()
#     cursor.execute(query)
#     connection.commit()
#     connection.close()
#
#
# def convert_into_binary(file_path):
#     with open(file_path, 'rb') as file:
#         binary = file.read()
#     return binary
#
#
# def read_file(file_path):
#     with open(file_path, 'r') as file:
#         file_txt = file.read()
#     return file_txt
#
#
# def insert_file(file_name, table_name):
#     connection = None
#     try:
#         # Establish a connection
#         connection = sqlite_connect()
#         print(f"Connected to the database `{DB_NAME}`")
#
#         # Create a cursor object
#         cursor = connection.cursor()
#         sqlite_insert_blob_query = f"""INSERT INTO {table_name} (name, data) VALUES (?, ?)"""
#
#         # Convert the file into binary
#
#         binary_file = read_file(file_name)
#         data_tuple = (file_name, binary_file)
#
#         # Execute the query
#         cursor.execute(sqlite_insert_blob_query, data_tuple)
#         connection.commit()
#         print('File inserted successfully')
#         cursor.close()
#
#     except sqlite3.Error as error:
#         print("Failed to insert blob into the table", error)
#     finally:
#         if connection:
#             connection.close()
#             print("Connection closed")
#
# # for root, __, files in os.walk('./data'):
# #     for file_name in files:
# #         with open(os.path.join(root, file_name)) as f:
# # sql_create_table_query = """CREATE TABLE flight (name TEXT NOT NULL, data BLOB);"""
# # execute_query(sql_create_table_query)
# # insert_file('./data/2021-01-07 15-59-47.txt', 'flight')
# insert_file('./data/2021-01-08 17-44-29.txt', 'flight')
#
# import pymongo
#
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#
# mydb = myclient["flights"]
# print(myclient.list_database_names())
#
# dblist = myclient.list_database_names()
# mycol = mydb["customers"]
# mydict = { "name": "John", "address": "Highway 37" }
#
# x = mycol.insert_one(mydict)
# if "flights" in dblist:
#   print("The database exists.")

from pymongo import MongoClient


class FlightDBAccess:
    mongo_client = None
    DB_name = 'flights_db'
    collection_name = 'flights'
    flights_db = None
    flights_collection = None
    parameters_collection = None
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if FlightDBAccess.__instance == None:
            FlightDBAccess()
        return FlightDBAccess.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if FlightDBAccess.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            # eden:eden = user:password in mongoDB cloud
            self.mongo_client = MongoClient(
                "mongodb+srv://eden:eden@dronescluster.srnyo.mongodb.net")
            # self.mongo_client = MongoClient(
            #     "mongodb+srv://eden:eden@dronescluster.srnyo.mongodb.net/Flights_DB?retryWrites=true&w=majority")

            # Create the flights database under the name 'flights_db'
            self.flights_db = self.mongo_client.Flights_DB
            # Create a collection under the name 'flights'
            self.flights_collection = self.flights_db.Flights
            self.parameters_collection = self.flights_db.Parameters
            FlightDBAccess.__instance = self

    def insert_one(self, data: dict, collection=None):
        """
            Insert dict to the flights data base
        """
        if collection is None:
            result = self.flights_collection.insert_one(data)
        else:
            result = collection.insert_one(data)
        print(result)

    def find_one(self, parameters: dict):
        return self.flights_collection.find_one(parameters)

    def find_all(self, parameters: dict):
        return self.flights_collection.find(parameters)

    def update_parameters(self, parameters: list):
        params = self.parameters_collection.find().stats()

        parameters = {param:param for param in parameters}
        try:
            for old_params in params:
                additional_params = {"$set": parameters}
                self.parameters_collection.update_one(old_params, additional_params)
        except:
            self.insert_one(parameters, self.parameters_collection)

    def get_files_parameters(self):
        return self.parameters_collection.find()

    def close_conn(self):
        self.mongo_client.close()


if __name__ == '__main__':
    # client = MongoClient(
    #     "mongodb+srv://eden:eden@dronescluster.srnyo.mongodb.net")
    # db = client.test_db
    # test_coll = db.test
    # res = test_coll.find_one({'age': 15})
    # test_coll.insert_one({'flie_name':'file', 'age': 30})
    # client.close()
    # print(res)
    # FlightDBAccess.getInstance()
        # .insert_one({'a': 'sss', 'age': 66})
    # access.insert_one({'a': 'ede', 'age': 66})
    # access.insert_one({'a': 'sdfdf', 'age': 18})
    for x in FlightDBAccess.getInstance().find_all({'age': '66'}):
        print(x)
