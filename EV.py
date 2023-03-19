import smartcar
from smartcar import auth_client as ac
from flask import Flask, redirect, request, jsonify
from flask_cors import CORS
import os


CLIENT_ID = 'c717a263-3545-4ef2-ae71-e696582c114f';
CLIENT_SECRET = '5090d782-104b-4a0a-852e-ad72b7ebd584';
REDIRECT_URI = 'http://localhost:8000/callback'


client = smartcar.AuthClient(
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    redirect_uri =REDIRECT_URI,
    mode='simulated'
)
scope = ['read_vehicle_info',
             'read_location',
             'read_odometer',
             'control_security']
    
auth_url = client.get_auth_url(scope)
app = Flask (__name__)
@app.route("/", methods=["GET"])
def login():
    # TODO: Authorization Step 2: Launch Smartcar authentication dialog
   
    return f'''
        <h1>Welcome to EV Analyzer </h1>
        <a href={auth_url}>
        <button style='text-align:center'>Connect Vehicle</button>
        </a>
'''

# global variable to save our access_token
access = None

# Ensure SETUP is completed, then instantiate an AuthClient
#client = smartcar.AuthClient(mode="test")

@app.route("/callback", methods=["GET"])
def exchange_code():
    """
    To work, this route must be in your Smartcar developer dashboard as a Redirect URI.

    i.e. "http://localhost:8000/exchange"
    """
    code = request.args.get("code")

    # access our global variable and store our access tokens
    global access

    # in a production app you'll want to store this in some kind of
    # persistent storage
    access = client.exchange_code(code)
    return redirect("/vehicle")


@app.route("/vehicle", methods=["GET"])
def get_vehicle():
    # access our global variable to retrieve our access tokens
    global access

    # receive a `Vehicles` NamedTuple, which has an attribute of 'vehicles' and 'meta'
    result = smartcar.get_vehicles(access.access_token)

    # get the first vehicle
    id_of_first_vehicle = result.vehicles[0]

    # instantiate the first vehicle in the vehicle id list
    vehicle = smartcar.Vehicle(id_of_first_vehicle, access.access_token)

    # use the attributes() method to call to Smartcar API and get information about the vehicle.
    # These vehicle methods return NamedTuples with attributes
    attributes = vehicle.attributes()

    return jsonify(
        {"make": attributes.make, "model": attributes.model, "year": attributes.year}
    )


app.run(port=8000)