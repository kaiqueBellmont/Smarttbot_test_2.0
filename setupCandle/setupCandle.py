from typing import List, Any, Dict

from candle.candle import Candle
from datetime import datetime
from requester.requester import Requester
from models.candleModels import CandlesModel

import time


class SetupCandle:
    COINS = ["BTC_BTS", "BTC_XMR", "BTC_DOGE"]

    def __init__(
        self,
        candle: Candle = None,
        req: Requester = Requester(),
        datetime: str = None,
        open_candles: list = None,
        closed_candles: list = None,
        counter: int = None,
        first_candle_reference: list = None,
        open_candle_5: list = None,
        open_values: list = None,
        close_values: list = None,
    ) -> None:
        self.req = req
        self.candle = candle
        self.counter = counter
        self.datetime = datetime
        self.open_candles = open_candles
        self.closed_candles = closed_candles
        self.first_candle_reference = first_candle_reference
        self.open_candle_5 = open_candle_5
        self.open_values = open_values
        self.close_values = close_values

    @staticmethod
    def _candle_formater_to_models(candle: dict) -> dict:
        candle = {
            "Moeda": candle["moeda"],
            "Periodicidade": candle["periodicidade"],
            "Datetime": candle["datetime"],
            "Open": candle["open"],
            "Low": candle["low"],
            "High": candle["high"],
            "Close": candle["close"],
        }
        return candle

    def _set_reference_candle(self):
        if self.counter == 0:
            for index, element in enumerate(self.open_candles):
                self.first_candle_reference.append(element["Open"])

    def _make_close_request_and_set_datetime(self):
        closed_candles_request = self.req.get_json_response()
        self.datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]
        return closed_candles_request

    def _map_coin_type_and_values(self, lista: list, datetime: str) -> List[Any]:
        lista_de_moedas = []
        for index, element in enumerate(lista):
            candle = Candle(
                moeda=self.COINS[index],
                periodicidade=0,
                datetime=datetime,
                open=element["last"],
                low=element["low24hr"],
                high=element["high24hr"],
                close=element["last"],
            )

            formated_candle = self._candle_formater_to_models(candle.__dict__)
            lista_de_moedas.append(formated_candle)
        return lista_de_moedas

    def _close_candles(self, closed_candles: list) -> List[Any]:
        reference_candle = self.first_candle_reference
        closed_candles_to_save = []
        for index, element in enumerate(closed_candles):
            if self.counter:
                element["Open"] = self.open_values[index]
                element["Close"] = self.close_values[index]
                element["Datetime"] = self.datetime
                element["Periodicidade"] = 1
                closed_candles_to_save.append(element)
            if self.counter == 5:
                # recebe os open candles de 5 min atras
                periodicity_5_candle = {
                    **element,
                    "Close": self.close_values[index],
                    "Open": reference_candle[index],
                    "Periodicidade": 5,
                }
                self.open_candle_5.append(self.close_values[index])
                closed_candles_to_save.append(periodicity_5_candle)

            if self.counter == 10:
                periodicity_5_candle2 = {
                    **element,
                    "Close": self.close_values[index],
                    "Open": self.open_candle_5[index],
                    "Periodicidade": 5,
                }
                closed_candles_to_save.append(periodicity_5_candle2)

                periodicity_10_candle = {
                    **element,
                    "Close": self.close_values[index],
                    "Open": reference_candle[index],
                    "Periodicidade": 10,
                }
                closed_candles_to_save.append(periodicity_10_candle)

        return closed_candles_to_save

    def _get_open_values_from_candles(self, res: dict) -> None:
        coin_list = [res[coin] for coin in self.COINS]
        self.open_candles = self._map_coin_type_and_values(
            lista=coin_list, datetime=self.datetime
        )
        self.open_values = [element["Open"] for element in self.open_candles]

    def _set_closed_candles(self, res):
        coin_list = [res[coin] for coin in self.COINS]
        self.closed_candles = self._map_coin_type_and_values(
            lista=coin_list, datetime=self.datetime
        )
        self.close_values = [element["Close"] for element in self.closed_candles]

    def setup_candles(self, db: CandlesModel) -> None:
        self.counter = 0
        self.first_candle_reference = []
        self.open_candle_5 = []
        while self.counter < 11:

            open_candles_request = self.req.get_json_response()
            self._get_open_values_from_candles(open_candles_request)

            self._set_reference_candle()

            time.sleep(58)

            closed_candles_values_from_request = (
                self._make_close_request_and_set_datetime()
            )

            # sets self.closed_candles to be used in self._close_candles
            self._set_closed_candles(closed_candles_values_from_request)

            finished_candles = self._close_candles(self.closed_candles)
            db.save_many(finished_candles)

            self.counter += 1

            if self.counter == 11:
                self.counter = 0


a = SetupCandle()
a.setup_candles(CandlesModel())
