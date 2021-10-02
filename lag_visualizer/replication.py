import pg8000.native
from datetime import datetime
from utils import MetaInfo


class ReplicationLag:
    """This class deals with all replication Lag related functionalities"""

    def __init__(self, config):
        self.__frequency = config["config"]["frequency"]
        self.__slot_name = config["config"]["slot_name"]
        self.__unit = config["config"]["unit"]
        self.__meta = MetaInfo()
        self.__connection = pg8000.native.Connection(**config.get("postgres"))
        self.__pg_version = self.set_pg_version()
        self.lag = {
            "time": [],
            "size": []
        }

    def set_pg_version(self):
        result = self.__connection.prepare("show server_version_num ;").run()
        versions = list(self.__meta.lag_query.keys())
        versions.sort()
        for v in versions:
            if int(v) <= int(result[0][0]):
                return v

    def __current_lag(self):
        try:
            query = self.__connection.prepare(self.__meta.lag_query[self.__pg_version])
            return query.run(slot=self.__slot_name, factor=self.__meta.factor.get(self.__unit))
        except Exception as err:
            print(f"Something went wrong while executing query with err {err.__str__()}")
            exit(1)

    def replication_lag_job(self):
        try:
            result = self.__current_lag()
            self.lag["time"].append(datetime.now().strftime("%H:%M:%S"))
            self.lag["size"].append(int(result[0][3]))
        except Exception as err:
            print(f"Something went wrong while running scheduled task query. Error: {err.__str__()}")
            exit(1)
