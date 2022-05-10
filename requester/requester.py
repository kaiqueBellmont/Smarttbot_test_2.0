import requests


class Requester(object):
    _Public_URL = "https://poloniex.com/public?command=returnTicker"

    def __init__(self, req: requests = requests, res: None = None) -> None:
        self.__req = req
        self.__res = res

    @property
    def req(self):
        return self.__req

    @property
    def res(self):
        return self.__res

    @res.setter
    def res(self, value):
        self.__res = value

    def _make_request(self, url: str = _Public_URL) -> dict:
        try:
            response = self.__req.get(url)
            return response.json()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    def get_json_response(self) -> dict:
        self.__res = self._make_request()
        return self.__res
