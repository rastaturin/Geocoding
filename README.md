# Geocoding Proxy Service

This is a simple network service that can resolve the lat, lng coordinates for the given address
by using third party geocoding services. The service provides a RESTful HTTP interface and
use JSON for data serialization.

This service uses following external geocoding services to resolve an address: 
- Geocoding Service by [HERE](https://developer.here.com/documentation/geocoder/topics/quick-start.html)
- Geocoding Service by [Google](https://developers.google.com/maps/documentation/geocoding/start)

## Getting started

1. Install Flask and clone the repo:

```ssh
pip install Flask
git clone https://github.com/rastaturin/Geocoding
cd Geocoding
```

2. Update config file `config.ini` with credential from geoservices.
  
3. Start the service  
  
```ssh
export FLASK_APP=main.py
flask run
```

By default it starts at `http://localhost:5000`.

## API
 
### GET /address/\<address\>  
  
The function returns location for the given address in JSON format:

```JSON
{
  "latitude": <latitude>, 
  "longitude": <longitude>
}
```

HTTP Codes:

- 200 - Successful
- 404 - Address not found
- 503 - Service unavailable 


Example:

`GET http://localhost:5000/address/San+Francisco`

```JSON
{
  "latitude": 37.77713, 
  "longitude": -122.41964
}
```

