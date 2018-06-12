import requests
from decouple import config

def get_location(lat, long):
	url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{long}&key='+config('GOOGLE_MAPS_API_KEY')
	response = requests.get(url).json()
	location = response["results"][1]["formatted_address"] # larger vacinity 
	return location