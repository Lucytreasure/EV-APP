import smartcar
from smartcar import auth_client as ac
from flask import Flask, redirect, request, jsonify
from flask_cors import CORS
import os

CLIENT_ID = '09cd57cd-7fac-49d5-8609-8fdda65d746d' #Enalyzer client id
# EV app client_id 'c717a263-3545-4ef2-ae71-e696582c114f';
CLIENT_SECRET = 'd4683f88-cf36-42b9-a6ae-b0118c484c4e' #Enalazer client secret
#EV app secret '5090d782-104b-4a0a-852e-ad72b7ebd584';
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
             'control_security',
             'control_charge',
             'read_engine_oil',
             'read_battery',
             'read_battery',
             'read_charge',
             'control_charge',
             'read_fuel'
             ]
    
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
    model = str(attributes.model);
    make = str(attributes.make);
    year = str(attributes.year);
    return f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css" integrity="sha384-xOolHFLEh07PJGoPkLv1IbcEPTNtaed2xpHsD9ESMhqIYd0nLMwNLD69Npy4HI+N" crossorigin="anonymous">
            <title>EV Analyzer Home</title>
        </head>
        <body>
            <div class='container text-center'>
                <div class='row col-md-6 text-center'>
                    <div class='card'>
                        <h3>Make: {make}</h3>
                        <h3>Model: {model}</h3>
                        <h3>Year: {year}</h3>
                        <div class='nav'>
                            <a href='/location'>
                                <button class='btn btn-primary'>location</button>
                            </a>
                            <a href='/odometer'>
                                <button class='btn btn-info'>odometer</button>
                            </a>
                            <a href='/engine/oil'>
                                <button class= 'btn btn-info'>Engine oil</button>
                            </a>
                            <a href='/battery/capacity'>
                                <button class='btn btn-info'>Battery Capacity</button>
                            </a>
                            <a href='/battery'>
                                <button class= 'btn btn-info'>Battery</button>
                            </a>
                            <a href='/charge'>
                                <button class= 'btn btn-info'>Charging</button>
                            </a>
                            <a href='/fuel'>
                                <button class='btn btn-info'>Fuel</button>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            <script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-Fy6S3B9q64WdZWQUiU+q4/2Lc9npb8tCaSX9FK7E8HnRr0Jz8D6OP9dO5Vg3Q9ct" crossorigin="anonymous"></script>
        </body>
        </html>
'''
@app.route("/location")
def get_location():
    global access

    # Get all vehicles associated with this access token
    response = smartcar.get_vehicles(access.access_token)

    # Construct a new vehicle instance using the first vehicle's id
    vehicle = smartcar.Vehicle(response.vehicles[0], access.access_token)

    try:
        # Fetch the vehicle's location
        location = vehicle.location()
        latitude = location.latitude
        longitude = location.longitude
        
        return f'''
            <html>
            <head>
            <head>
            <body>
                <h6>Latitude: {latitude}</h6>
                <h6>Longitude: {longitude}</h6>
            </body>
            </html>
            
    '''
    except Exception as e:
        return redirect("/Error")
    

@app.route("/odometer")
def get_odometer():
    global access

    # Get all vehicles associated with this access token
    response = smartcar.get_vehicles(access.access_token)

    # Construct a new vehicle instance using the first vehicle's id
    vehicle = smartcar.Vehicle(response.vehicles[0], access.access_token)
    try:
        # Fetch the vehicle's location
        odometer = vehicle.odometer()
        
        return f'''
            <html>
            <head>
            <body>
                <h3>Odometer: {odometer.distance}</h3>
            </body>
            </html>
    '''
    except Exception as e:
        return redirect("/Error")

@app.route("/engine/oil")
def get_engine_oil():
    global access

    # Get all vehicles associated with this access token
    response = smartcar.get_vehicles(access.access_token)

    # Construct a new vehicle instance using the first vehicle's id
    vehicle = smartcar.Vehicle(response.vehicles[0], access.access_token)

    try:
        engine_oil = vehicle.engine_oil()
        return f'''
            <html>
            <head>
            </head>
            <body>
                <h2>LifeRemaining: {engine_oil.life_remaining}</h2>
                <h4>{engine_oil.meta}
            </body>
            </html>
    ''',200
    except Exception as c:
        return redirect('/Error')
@app.route("/Error")
def Error_page():
    return f'''
    <h3>Sorry Your car do not support this function you are trying to access!!!
''',500

@app.route("/battery/capacity")
def get_battery_capacity():
    global access

    # Get all vehicles associated with this access token
    response = smartcar.get_vehicles(access.access_token)

    # Construct a new vehicle instance using the first vehicle's id
    vehicle = smartcar.Vehicle(response.vehicles[0], access.access_token)
    try:
        battery_capacity = vehicle.battery_capacity()
        print(battery_capacity)
        return f'<h2>Battery Capacity: {battery_capacity.capacity}</h2>',200
    except Exception as e:
        return redirect("/Error")


@app.route("/battery")
def get_battery():
    global access

    # Get all vehicles associated with this access token
    response = smartcar.get_vehicles(access.access_token)

    # Construct a new vehicle instance using the first vehicle's id
    vehicle = smartcar.Vehicle(response.vehicles[0], access.access_token)
    try:
        battery = vehicle.battery()
        print(battery)
        return f'h2{battery.percent_remaining}</h2>',200
    except Exception as e:
        return redirect("/Error")

@app.route("/charge", methods=["POST"])
def get_charge():
    global access

    # Get all vehicles associated with this access token
    response = smartcar.get_vehicles(access.access_token)

    # Construct a new vehicle instance using the first vehicle's id
    vehicle = smartcar.Vehicle(response.vehicles[0], access.access_token)
    try:
        charge = vehicle.charge()
        print(charge)
        return f'',200
    except Exception as e:
        return redirect("/Error")

@app.route("/fuel")
def get_fuel():
    global access

    # Get all vehicles associated with this access token
    response = smartcar.get_vehicles(access.access_token)

    # Construct a new vehicle instance using the first vehicle's id
    vehicle = smartcar.Vehicle(response.vehicles[0], access.access_token)
    try:
        fuel = vehicle.fuel()
        print(fuel)
        return f'''
            <h2>Fuel range:{fuel.range}</h2>
            <h2>Amount remaining:{fuel.amount_remaining}
            <h2>Percentage remaining:{fuel.percent_remaining}
    ''',200
    except Exception as e:
        return redirect("/Error")

app.run(port=8000)