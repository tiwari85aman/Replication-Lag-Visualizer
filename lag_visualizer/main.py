"""
SQL Query to find pg replication log:

pg version < 10

SELECT pg_current_xlog_insert_location() as current_lsn, slot_name,restart_lsn,
round((pg_current_xlog_insert_location()-restart_lsn) / 1024 / 1024 , 2) AS GB_behind
FROM pg_replication_slots;

"""

from apscheduler.schedulers.background import BackgroundScheduler
from visualizer import Visualizer
from replication import ReplicationLag
import click


@click.command()
@click.option('--host', default="localhost", help='Postgres hostname, default: localhost')
@click.option('--port', default=5432, help='Postgres port, default: 5432')
@click.option('--database', default="postgres", help='Postgres database, default: postgres')
@click.option('--user', default="postgres", help='Postgres user, default: postgres')
@click.option('--password', default="postgres", help='Postgres password')
@click.option('--slot', help='Replication slot name')
@click.option('--frequency', default=1, help='lag data collection query frequency in seconds, default: 1s')
@click.option('--unit', default="mb", help='Y-axis unit type possible values are: b,kb,mb,gb , default: mb')
@click.option('--mode', default="web", help='CLI mode/web/matplotlib , default: mb')
def arg_parser(host, port, user, password, database, slot, frequency, unit, mode):
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
            "unit": unit,
            "mode": mode
        }

    }
    return args


def set_scheduler(job, interval):
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(job, 'interval', seconds=interval)
    sched.start()


if __name__ == '__main__':
    args = arg_parser(standalone_mode=False)
    pg = ReplicationLag(args)
    set_scheduler(job=pg.replication_lag_job, interval=args["config"]["frequency"])
    Visualizer(pg).start(args["config"]["mode"])
