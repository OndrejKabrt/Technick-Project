import os

import pyodbc
import json


class DatabaseSingleton:
    conn = None
    active_connections = []

    def __new__(cls):
        if not cls.conn:
            cls.new_conn()
        connection = cls.conn
        cls.active_connections.append(connection)
        return connection

    @classmethod
    def new_conn(cls):
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={cls.readconfig('server')};"
            f"DATABASE={cls.readconfig('database')};"
            f"UID={cls.readconfig('user')};"
            f"PWD={cls.readconfig('password')};"
            "Trusted_Connection=no;"
        )
        connection = pyodbc.connect(conn_str)
        cls.conn = connection

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
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Získá adresář současného souboru
        config_path = os.path.join(script_dir, "..", "appconfig.json")  # Jde o úroveň výš
        with open(config_path, "r") as f:
            config = json.load(f)
            return config["database"][key]

# conn = DatabaseSingleton.new_conn()
# DatabaseSingleton.close_conn()
# print("Konec")