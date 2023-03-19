import smartcar
import itertools

access_token = "239c04ca-8abe-4b26-946e-37c5a21dd294"
response = smartcar.get_vehicles(access_token)
#vid =response(['vehicles'][access_token])
#vehicle = smartcar.Vehicle(vid,access_token)
print(response)