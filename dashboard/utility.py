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
            zone_id, params={'since': -1440}).get('totals')
        return data

    def get_zone_analytics_timeseries_requests(self, zone_name):
        """
        gives timeseries requests analytics of the zone in last 24 hours
        """
        cf = CloudFlare.CloudFlare(email=self.email, token=self.api_key)
        zone_id = self.get_zone_id(zone_name)
        data_all = cf.zones.analytics.dashboard(
            zone_id, params={'since': -1440}).get('timeseries')
        since_until = {}  # for storing the since until data
        for data in data_all:
            since_data = data.get('since')
            until_data = data.get('until')
            data_requests = data.get('requests').get('all')
            since_until[(since_data, until_data)] = data_requests
        since_until_list = []
        requests_list = []
        for timestamp in since_until:
            since_until_list.append(timestamp)
            requests_list.append(since_until[timestamp])
        return since_until_list, requests_list
        return since_until_list, requests_list

    def get_zone_analytics_timeseries_visitors(self, zone_name):
        """
        gives timeseries unique visistors analytics of the zone in last 24 hours
        """
        cf = CloudFlare.CloudFlare(email=self.email, token=self.api_key)
        zone_id = self.get_zone_id(zone_name)
        data_all = cf.zones.analytics.dashboard(
            zone_id, params={'since': -1440}).get('timeseries')
        since_until = {}  # for storing the since until data
        for data in data_all:
            since_data = data.get('since')
            until_data = data.get('until')
            data_unique = data.get('uniques').get('all')
            since_until[(since_data, until_data)] = data_unique
        since_until_list = []
        unique_visitor_list = []
        for timestamp in since_until:
            since_until_list.append(timestamp)
            unique_visitor_list.append(since_until[timestamp])
        return since_until_list, unique_visitor_list

    def get_zone_analytics_timeseries_data_served(self, zone_name):
        """
        gives timeseries for the data served in the last 24 hours.
        """
        cf = CloudFlare.CloudFlare(email=self.email, token=self.api_key)
        zone_id = self.get_zone_id(zone_name)
        data_all = cf.zones.analytics.dashboard(
            zone_id, params={'since': -1440}).get('timeseries')
        data_to_give = []
        for data in data_all:
            data_served = (data.get('bandwidth').get('all'))/(1000*1000)
            data_served_final = float("{:.2f}".format(data_served))
            data_to_give.append(data_served_final)
        return data_to_give

    def get_zone_analytics_timeseries_percent_cached(self, zone_name):
        """
        gives timeseries for the % cached data served in the last 24 hours.
        """
        cf = CloudFlare.CloudFlare(email=self.email, token=self.api_key)
        zone_id = self.get_zone_id(zone_name)
        data_all = cf.zones.analytics.dashboard(
            zone_id, params={'since': -1440}).get('timeseries')
        data_to_give = []
        for data in data_all:
            data_cached = data.get('bandwidth').get('cached')
            data_served = data.get('bandwidth').get('all')
            long_data = (data_cached/data_served)*100
            good_data = float("{:.2f}".format(long_data))
            data_to_give.append(good_data)
        return data_to_give

    def get_zone_analytics_timeseries_data_cached(self, zone_name):
        """
        gives timeseries for the total cached data served in the last 24 hours.
        """
        cf = CloudFlare.CloudFlare(email=self.email, token=self.api_key)
        zone_id = self.get_zone_id(zone_name)
        data_all = cf.zones.analytics.dashboard(
            zone_id, params={'since': -1440}).get('timeseries')
        data_to_give = []
        for data in data_all:
            data_cached = (data.get('bandwidth').get('all'))/(1000)
            data_served_final = float("{:.2f}".format(data_cached))
            data_to_give.append(data_served_final)
        return data_to_give

    def get_date(self, zone_name):
        since_until_list, _ = self.get_zone_analytics_timeseries_visitors(
            zone_name)
        month_mapping = {'01': 'Jan',
                         '02': 'Feb',
                         '03': 'Mar',
                         '04': 'Apr',
                         '05': 'May',
                         '06': 'Jun',
                         '07': 'Jul',
                         '08': 'Aug',
                         '09': 'Sept',
                         '10': 'Oct',
                         '11': 'Nov',
                         '12': 'Dec'
                         }
        # Finding the previous day's date
        since_until_first = since_until_list[0]
        since_first, until_first = since_until_first
        since_first_date = since_first.split('T')[0]
        since_first_date_list = since_first_date.split('-')
        since_first_date_final = since_first_date_list[-1] + \
            ' ' + month_mapping[since_first_date_list[-2]]

        # Finding the current day's date
        since_until_last = since_until_list[-1]
        since_last, _ = since_until_last
        since_last_date = since_last.split('T')[0]
        since_last_date_list = since_last_date.split('-')
        since_last_date_final = since_last_date_list[-1] + \
            ' '+month_mapping[since_last_date_list[-2]]
        return since_first_date_final, since_last_date_final


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
