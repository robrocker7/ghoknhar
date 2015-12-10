import requests


class ZWave(object):

    """ Control using ZWave JSON API. """

    def __init__(self, ip="127.0.0.1", port=8083):
        # PRIVATE
        self._ip = ip
        self._port = port

        # PUBLIC
        self.inclusion = False

    def _request(self, command, device):
        pass

    @property
    def url(self):
        return '{0}:{1}/ZWaveAPI/Run/'.format(self._ip, self._port)

    def get_data_from_controller(self):
        data_url = self.url
