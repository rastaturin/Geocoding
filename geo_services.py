import json
import urllib.request
import urllib.parse


class GeoService:
    """This service resolve address using HERE and Google geo services.
    """

    def __init__(self, config):
        """
        Args:
            config (:obj:`str`) Configuration for geo services
        """
        self.providers = [
            HereGeoProvider(config['HERE']),
            GoogleGeoProvider(config['Google']),
        ]

    def get_location(self, address):
        """Returns location for the given address
                
        :param str address: The address to be resolved
        :return: location 
            {
                'latitude': 12.345,
                'longitude': 65.4321
            }
        :rtype: dict
        :raises RuntimeError: If all the geoservices fail  
        :raises NotFoundException: If all the geoservices fail and some of them can't find the address
        """
        address = urllib.parse.quote_plus(address)
        not_found = False
        errors = []
        for provider in self.providers:
            try:
                return provider.get_location(address)
            except NotFoundException:
                not_found = True
            except Exception as e:
                errors.append(str(e))
        if not_found:
            raise NotFoundException
        raise RuntimeError(', '.join(errors))


class AbstractGeoProvider:
    """Abstract geoservice class.
    """
    def get_url(self, address):
        raise NotImplementedError("Should have implemented this")

    def get_location_dict(self, response):
        raise NotImplementedError("Should have implemented this")

    def get_location(self, address):
        """Returns location for the given address
        :param str address: The address to be resolved
        :return: location 
            {
                'latitude': 12.345,
                'longitude': 65.4321
            }
        :rtype: dict
        """
        url = self.get_url(address)
        response = urllib.request.urlopen(url).read()
        data = json.loads(response)
        return self.get_location_dict(data)


class HereGeoProvider(AbstractGeoProvider):
    """HERE geoservice    
    """
    def __init__(self, config):
        self.app_id = config['app_id']
        self.app_code = config['app_code']

    def get_url(self, address):
        return 'https://geocoder.cit.api.here.com/6.2/geocode.json?app_id=%s&app_code=%s&searchtext=%s' \
               % (self.app_id, self.app_code, address)

    def get_location_dict(self, response):
        if not response.get('Response').get('View'):
            raise NotFoundException()
        location = response.get('Response').get('View')[0].get('Result')[0].get('Location').get('NavigationPosition')[0]
        return {'latitude': location.get('Latitude'), 'longitude': location.get('Longitude')}


class GoogleGeoProvider(AbstractGeoProvider):
    """Google geoservice    
    """
    def __init__(self, config):
        self.app_key = config['api_key']

    def get_url(self, address):
        return 'https://maps.googleapis.com/maps/api/geocode/json?key=%s&address=%s' % (self.app_key, address)

    def get_location_dict(self, response):
        if response.get("status") == "ZERO_RESULTS":
            raise NotFoundException()
        location = response.get('results')[0].get('geometry').get('location')
        return {'latitude': location.get('lat'), 'longitude': location.get('lng')}


class NotFoundException(Exception):
    pass
