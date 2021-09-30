# Replication-Lag-Visualizer

A simple cli based tool to visualize the replication lag in realtime.


## Supported Database:
- Postgres

### Parameters:
| name | description|default|
|--------|---|---|
| `host` | Postgres Hostname	| localhost
| `port` | Postgres Port	| 5432
| `database` | Postgres Database	| postgres
| `user` | Postgres Username	| postgres
| `password` | Postgres Password | postgres
| `slot` | Replication slot name	|
| `frequency` | frequency of polling	| 1
| `unit` | size unit e.g. b,kb,mb,gb	| mb
| `mode` | mode of visualization e.g. web, matplotlib	| web

## Features:
- creates timeseries replication lag graph in realtime with given `frequency` of given `slot`.
- Two modes supported:
    - Matplotlib based graph
    - Web based graph

## Screenshot:
### Web Mode:
![alt text](img/web.png)

### Matplotlib Mode:
![alt text](img/matplotlib.png)
