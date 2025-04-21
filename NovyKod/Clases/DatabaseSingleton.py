import os
import logging
import mysql.connector
from mysql.connector import pooling
import json


class DatabaseSingleton:
    conn = None
    active_connections = []

    def __new__(cls):
        if not cls.conn:
            cls.new_conn()
        connection = cls.conn.get_connection()
        cls.active_connections.append(connection)
        return connection

    @classmethod
    def new_conn(cls):
        try:
            logging.debug(f"Connecting to database: host={cls.readconfig('host')}, port={cls.readconfig('port')}, user={cls.readconfig('user')}, database={cls.readconfig('database')}")
            connection = pooling.MySQLConnectionPool(
                pool_name="Connection_pool",
                host=cls.readconfig("host"),
                port=cls.readconfig("port"),
                user=cls.readconfig("user"),
                password=cls.readconfig("password"),
                database=cls.readconfig("database"),
            )
            cls.conn = connection
            logging.debug("Database connection established successfully")
        except Exception as e:
            logging.error(f"Error connecting to database: {str(e)}")

    @classmethod
    def close_conn(cls, connection=None):
        if (cls.conn):
            if (connection):
                cls.active_connections.remove(connection)
                connection.close()
            else:
                for i in cls.active_connections:
                    cls.active_connections.remove(i)
                    i.close()
                cls.conn = None

    @classmethod
    def readconfig(cls, key):
        try:
            config_path = os.path.join(os.path.dirname(__file__), "appconfig.json")
            logging.debug(f"Reading config from {config_path}")
            with open(config_path, "r") as f:
                config = json.load(f)
                value = config["database"][key]
                logging.debug(f"Config {key}={value}")
                return value
        except Exception as e:
            logging.error(f"Error reading config: {str(e)}")
            raise
