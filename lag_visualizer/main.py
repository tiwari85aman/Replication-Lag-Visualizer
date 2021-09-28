"""
SQL Query to find pg replication log:

pg version < 10

SELECT pg_current_xlog_insert_location() as current_lsn, slot_name,restart_lsn,
round((pg_current_xlog_insert_location()-restart_lsn) / 1024 / 1024 , 2) AS GB_behind
FROM pg_replication_slots;

"""
import pg8000.native
import click
from datetime import datetime
import matplotlib.pyplot as plt
import time


@click.command()
@click.option('--host', default="localhost", help='Postgres hostname, default: localhost')
@click.option('--port', default=5432, help='Postgres port, default: 5432')
@click.option('--database', default="postgres", help='Postgres database, default: postgres')
@click.option('--user', default="postgres", help='Postgres user, default: postgres')
@click.option('--password', default="postgres", help='Postgres password')
@click.option('--slot', help='Replication slot name')
@click.option('--frequency', default=1, help='lag data collection query frequency in seconds, default: 1s')
@click.option('--unit', default="mb", help='Y-axis unit type possible values are: b,kb,mb,gb , default: mb')
def arg_parser(host, port, user, password, database, slot, frequency, unit):
    """Parse the postgres connectivity configurations"""
    args = {
        "postgres": {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database
        },
        "config": {
            "slot_name": slot,
            "frequency": frequency,
            "unit": unit
        }

    }
    return args


class MetaInfo:
    """ This class deals with all the constants, conversion or meta info"""

    def __init__(self):
        self.factor = {
            "gb": 1024 * 1024 * 1024,
            "mb": 1024 * 1024,
            "kb": 1024,
            "b": 1,
        }
        self.lag_query = {
            "10": """""",
            "9": """SELECT pg_current_xlog_insert_location() as current_lsn, slot_name,restart_lsn, 
                round((pg_current_xlog_insert_location()-restart_lsn) / :factor , 2) AS GB_behind 
                FROM pg_replication_slots where slot_name=:slot;"""
        }


class ReplicationLag:
    """This class deals with all replication Lag realted functionalities"""

    def __init__(self, config):
        self.__frequency = config["config"]["frequency"]
        self.__slot_name = config["config"]["slot_name"]
        self.__unit = config["config"]["unit"]
        self.__meta = MetaInfo()
        self.__connection = pg8000.native.Connection(**config.get("postgres"))

    def current_lag(self):
        try:
            query = self.__connection.prepare(self.__meta.lag_query.get("9"))
            return query.run(slot=self.__slot_name, factor=self.__meta.factor.get(self.__unit))
        except Exception as err:
            print(f"Something went wrong while executing query with err {err.__str__()}")
            exit(1)

    def start_monitoring(self):
        xar = []
        yar = []
        fig = plt.figure()
        chart = fig.add_subplot(1, 1, 1)

        while True:
            result = self.current_lag()
            xar.append(datetime.now().strftime("%H:%M:%S"))
            yar.append(int(result[0][3]))
            chart.clear()
            chart.plot(xar, yar)
            plt.pause(self.__frequency)
            time.sleep(self.__frequency)


if __name__ == '__main__':
    args = arg_parser(standalone_mode=False)
    pg = ReplicationLag(args)
    pg.start_monitoring()
