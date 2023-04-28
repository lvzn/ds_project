# Instructions

Please initialize the database using sqlite first before running the code.

    sqlite3 database.db < initialize.sql

After the database has been initialized, you should must set up the virtual environment and install the required packages:

    python3 -m venv env
    env/bin/activate
    python3 -m pip install -r requirements.txt
    
Now you should be able to run the services:

    python3 server.py &
    python3 visualize.py &
    python3 client.py

NOTE: make sure to run these commands in the virtual environment, `env/bin/activate` before running these commands.

This will make server and visualize services run in background. 

# Prerequisites
 - sqlite3
 - python