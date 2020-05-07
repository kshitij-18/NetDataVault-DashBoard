import CloudFlare
import base64


class CloudFlareWork():
    def __init__(self, api_key, email):
        self.api_key = api_key
        self.email = email

    def zone_list(self):
        """
        This function returns the zone ids and the names of the zones that the user has
        return type: list(list())
        e.g. [[zone_id_1, zone_name_1], [zone_id_2, zone-name_2]]
        """
        cf = CloudFlare.CloudFlare(email=self.email, token=self.api_key)
        zones = cf.zones.get()
        out_li = []
        for zone in zones:
            zone_id = zone['id']
            zone_name = zone['name']
            out_li.append([zone_id, zone_name])
        return out_li

    def get_zone_id(self, zone_name):
        '''
        Function takes the zone_name and returns the corresponding zone id.
        '''
        zones = self.zone_list()
        for zone in zones:
            if zone_name == zone[1]:
                return zone[0]

    def get_zone_analytics_24_hrs(self, zone_name):
        '''
        gives the analytics of the zone in the last 24 hrs.
        '''
        cf = CloudFlare.CloudFlare(email=self.email, token=self.api_key)
        zone_id = self.get_zone_id(zone_name)
        data = cf.zones.analytics.dashboard(
            zone_id, params={'since': -43200}).get('totals')
        return data


def encode_string(normal_string):
    # this will return binary form of string
    message_bytes = normal_string.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    return base64_message


def decode_string(encoded_string):
    base64_bytes = encoded_string.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')

    return message
