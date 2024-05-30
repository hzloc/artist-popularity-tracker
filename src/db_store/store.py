import logging
import os
from typing import List

import psycopg2
from dotenv import load_dotenv

from src.utils.logger import get_logger

load_dotenv()


class Store:
    """
    Is being used to store information into database

    """
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.username = os.getenv("DB_USERNAME")
        self.password = os.getenv("DB_PASSWORD")
        self.db_name = os.getenv("DB_NAME")
        self.db_port = os.getenv("DB_PORT")
        self.log = get_logger("DB Log", level=logging.ERROR)

        self.conn: psycopg2._psycopg.connection = None
        self.cur: psycopg2._psycopg.cursor = None

    def _connect(self):
        try:
            self.conn = psycopg2.connect(dbname=self.db_name, host=self.host, user=self.username, password=self.password, port=int(self.db_port))
            self.cur = self.conn.cursor()
        except psycopg2.Error as conn_err:
            self.log.fatal(conn_err)
            raise Exception("Terminating! Database is down!")

    def _close(self):
        try:
            self.cur.close()
            self.conn.close()
        except psycopg2.Error as conn_err:
            self.log.critical(conn_err)

    def store(self, data: list[dict[str, str]], table: str):
        self._connect()
        column_names: List[str] = list(data[0].keys())
        column_names_placeholders: List[str] = [f"%({column})s" for column in column_names]

        column_names_as_str = ', '.join(column_names)
        column_names_placeholders_as_str = ', '.join(column_names_placeholders)

        stmt = "INSERT INTO {} ({}) VALUES ({}) ON CONFLICT DO NOTHING".format(table, column_names_as_str, column_names_placeholders_as_str)

        try:
            self.log.info("Adding values into database..")

            for row in data:
                self.cur.execute(stmt, row)

            self.conn.commit()
        except psycopg2.Error as err:
            self.log.error(err)
        finally:
            self._close()


if __name__ == "__main__":
    storage = Store()
    storage._connect()