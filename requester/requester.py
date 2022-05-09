import requests
from datetime import datetime


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

    def get_json_response(self):
        self.__res = self._make_request()
        return self.__res

    # todo fazer para outras moedas
    # todo fazer a função de setar periodicidade
    # dica: começar com um candle.py de 1 minuto, setar ele como referencia de 1
    # dica 2: setar um candle.py de 5 minutos
    def bitcoin(self):
        self.__res = self._make_request()
        bitcoin = self.__res["BTC_BTS"]
        bitcoin = {
            "Moeda": "Bitcoin",
            "Periodicidade": "reference_candle",
            "Datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4],
            "Open": bitcoin["last"],
            "Low": bitcoin["low24hr"],
            "High": bitcoin["high24hr"],
            "close": bitcoin["last"],
        }
        return bitcoin


# print(a.make_request())
# print(datetime.now())
