import requests


class ZWaveController(object):

    """ Control using ZWave JSON API. """

    def __init__(self, ip="127.0.0.1", port=8083):
        # PRIVATE
        self._ip = ip
        self._port = port

        # PUBLIC
        self.inclusion = False
        self.latest_sync = self.get_data_from_controller()
        self.devices = self.latest_sync['devices']
        self.controller = self.latest_sync['controller']

    def _request(self, url):
        r = requests.get(url)
        return r.json()

    @property
    def url(self):
        return 'http://{0}:{1}/ZWaveAPI/'.format(self._ip, self._port)

    def get_data_from_controller(self):
        data_url = '{0}Data/0/'.format(self.url)
        return self._request(data_url)

    def run_command(self, device, instance, command, value):
        url = '{0}Run/devices[{1}].\
                      instances[{2}].\
                      commandClasses[{3}].\
                      Set({4})'.format(self.url, device, instance, command, value)
        print url
        #requests.async.get(url)
        return
