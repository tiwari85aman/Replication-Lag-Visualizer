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
