# Artists Popularity Tracker

## Overview

![workstructure](/imgs/work_principle.jpg)

The Artist-Tracker-ETL is a portfolio ETL (Extract, Transform, Load) project that retrieves and transforms data from two different sources and loads it into a PostgreSQL database using Docker, Apache Airflow, and Python as the primary technologies.

## Technologies Used
- Docker
- Apache Airflow
- PostgreSQL
- Python

## Prerequisites 

- Docker installed on your machine
- Basic understanding of Airflow, Docker, PostgreSQL and Python

## Getting Started

The following steps will guide you to run this project on your local machine for development and testing purposes.

### Installation

1. Download or clone this repository to your local machine.

```bash
git clone https://github.com/hzlocs/artist-tracker-etl.git 
cd artist-tracker-etl 
```

```bash
docker-compose --env-file src/.env up
```
## Usage

After starting the services (it can take a little bit time), you can access the Airflow web interface by going to: `http://localhost:8080`. Here, you'll be able to see the DAGs that have been defined, schedule and trigger DAG runs, and monitor their status. 
Credentials:  
    - `username: airflow`  
    - `password: airflow`  
Run some of the flows to fetch data into the database, and then using apps such as DBeaver, you can see fetched data.