import json
import mysql.connector
import re
from flask import Flask, request
from urllib.parse import unquote_plus

app = Flask(__name__)


def database_cursor():
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1",
    )
    cursor = mydb.cursor()
    return cursor

def sum_record(a, b, sum):
    cursor = database_cursor()
    cursor.execute("INSERT INTO summation (a, b, c) VALUES ({a}, {b}, {c});".format(a=a, b=b, c=sum))
    cursor.close()

@app.route('/')
def hello_world():
    return 'Hello, Docker!'


@app.route('/widgets')
def get_widgets():
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1",
        database="inventory",
    )
    cursor = mydb.cursor()

    cursor.execute("SELECT * FROM widgets")

    row_headers = [x[0] for x in cursor.description]  # this will extract row headers

    results = cursor.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))

    cursor.close()

    return json.dumps(json_data)


@app.route('/api/print', methods=['POST'])
def print_test():
    """
    Send a POST request to localhost:5000/api/print with a JSON body with a "p" key
    to print that message in the server console.
    :return:
    """
    payload = request.get_json()
    print(payload['p'])
    return ("", 200, None)

@app.route('/api/sum', methods=['POST'])
def sum():
    """
    Send a POST request to localhost:5000/api/sum with a JSON body with an "a" and "b" key
    to have the app add those numbers together and return a response string with their sum.
    :return:
    """
    print("\nProcessing request")
    print('\nrequest: ', request)
    payload = request.get_json()
    print("\nReceived following payload:")
    print(payload)

    print("\nAdding sum...")
    summation = int(payload['a']) + int(payload['b'])
    print("Found sum: {}".format(summation))
    a = payload['a']
    b = payload['b']
    print("creating response string")
    resp = '{a} + {b} = {sum}'.format(a=a, b=b, sum=summation)
    print(resp)
    sum_record(a=a, b=b, sum=summation)
    return resp, 200, None



@app.route('/initdb')
def db_init():
    cursor = database_cursor()

    cursor.execute("DROP DATABASE IF EXISTS inventory")
    cursor.execute("CREATE DATABASE inventory")
    cursor.close()

    cursor = database_cursor()

    cursor.execute("DROP TABLE IF EXISTS widget")
    cursor.execute("CREATE TABLE widget (name VARCHAR(255), description VARCHAR(255))")
    cursor.execute("DROP TABLE IF EXISTS summation")
    cursor.execute("CREATE TABLE summation (a INT, b INT, c INT)")
    cursor.close()

    return 'init database'

if __name__ == "__main__":
    app.run(host='0.0.0.0')