#!python3

# For this stub, implement items marked with "Implement:"

"""
This is a console client that connects to a Bottle server running the "widget" API
It supports basic methods: GET, POST, PUT, DELETE
"""

# Implement: import of needed packages
import json
import requests



while True:
    # String s holds the command and any input parameters separated by space
    s = input(">> ")
    cmd = s.split()[0]
    if cmd == "get":
        # Implement: logic to send a GET to the server and print the response or status
        r = requests.get('http://127.0.0.1:5000/widget_models')
        print(r.json())
        
    elif cmd == "post":
        # Implement: logic to send a POST to the server and print the response or status
     
        
        #j = '{' + '"model": ' + s.split()[1] + '}'
        payload = {'model': s.split()[1]}
        r = requests.post('http://127.0.0.1:5000/widget_models', json= payload)
        
        print(r.json())
        
    elif cmd == "put":
        # Implement: logic to send a PUT to the server and print the response or status
        oldname = s.split()[1]
        newname = s.split()[2]
        r = requests.put(f"http://127.0.0.1:5000/widget_models/{oldname}", json = {'model': newname})
        
        print(r.json())
    elif cmd == "delete":
        oldname = s.split()[1]
        r = requests.delete(f"http://127.0.0.1:5000/widget_models/{oldname}")
        # Implement: logic to send a DELETE to the server and print the response or status
        if r.status_code != 404 and r.status_code != 400:
            print(f"{r.status_code} " + ": " + oldname + " Deleted Sucessfully")
        else:
            print("Invalid Input")        
    elif cmd == "x":
        break
    else:
        print('\nunknown command')

