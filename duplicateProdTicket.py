#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import oracledb
import pandas as pd
import requests
import json

# Provide connection details
username = "username"
password = "password"
dsn = "ip:port/servicename"

try:
    # Connect to the database
    connection = oracledb.connect(user=username, password=password, dsn=dsn)
    print("Connection successful!")

    # Create a cursor to execute queries
    cursor = connection.cursor()

    # Execute a sample query
    query = "select column from table where condition=''"
    # Execute the query and load the result into a DataFrame
    df = pd.read_sql(query, con=connection)

    # Print the DataFrame
    print(df)

    # Close the cursor and connection
    cursor.close()
    connection.close()

except oracledb.Error as e:
    print(f"Error connecting to Oracle Database: {e}")


for index, row in df.iterrows():
    # Prepare the payload for the API call
    url = f"https://api-detail-ticket-prod/listDetail?column={row['column']}"
    payload={}
    headers = {
        'api_id': 'api_id',
        'api_key': 'api_key',
        'Content-Type': 'application/json',
    }

    # Make the POST request
    response = requests.request("GET", url, headers=headers, data=payload)
    response_json = response.json()
    
    data_list = response_json.get('data',[]);

    for item in data_list:
        url_create_ticket=f"https://api-create-ticket/service"
        headers_create_ticket = {
            'api_id': 'api_id',
            'api_key': 'api_key',
        }
        
        payload_create_ticket={
            "data1":item.get("data1"),
            "data2":item.get("data2"),
            "data3":item.get("data3"),
            "data4":item.get("data4")
        }
        
        response_create_ticket = requests.request("POST", url_create_ticket, headers=headers_create_ticket, json=payload_create_ticket)
        response_create_ticket_json = response_create_ticket.json()
        print(response_create_ticket_json)

