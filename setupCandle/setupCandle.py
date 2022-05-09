from typing import List, Any

from candle.candle import Candle
from datetime import datetime
from requester.requester import Requester
from models.candleModels import Candles

import time


class SetupCandle(Candle):
    COINS = ["BTC_BTS", "BTC_XMR", "BTC_DOGE"]

    def __init__(
        self,
        moeda: str = None,
        periodicidade: int = None,
        datetime: str = None,
        open: str = None,
        low: str = None,
        high: str = None,
        close: str = None,
        req: Requester = Requester(),
        *args,
        **kwargs
    ) -> None:
        self.req = req
        super().__init__(moeda, periodicidade, datetime, open, low, high, close)

    def _map_coin_type(self, lista: list, datetime: str) -> List[Any]:
        lista_de_moedas = []
        for index, element in enumerate(lista):
            self.moeda = self.COINS[index]
            self.periodicidade = None
            self.datetime = datetime
            self.open = element["last"]
            self.low = element["low24hr"]
            self.high = element["high24hr"]
            self.close = element["last"]
            setting = {
                "Moeda": self.moeda,
                "Periodicidade": self.periodicidade,
                "Datetime": self.datetime,
                "Open": self.open,
                "Low": self.low,
                "High": self.high,
                "Close": self.close,
            }
            lista_de_moedas.append(setting)
        return lista_de_moedas

    def close_candle(
        self,
        datetime: str,
        open_candle_list: list,
        new_candle_list: list,
        contator: int,
        first_candle_reference: list,
        open_candle_5: list,
        open_values: list,
        close_values: list,
    ) -> List[Any]:
        # print('Dentro da função Open')
        # print(open_values[1])
        # print('Dentro da função Close')
        # print(close_values[1])

        open_candle_1 = first_candle_reference
        final_candle_list = []
        for index, element in enumerate(new_candle_list):
            if contator:
                element["Open"] = open_values[index]
                element["Close"] = close_values[index]
                element["Datetime"] = datetime
                element["Periodicidade"] = 1
                final_candle_list.append(element)
            if contator == 5:
                # recebe os open candles de 5 min atras
                teste0 = {
                    **element,
                    "Close": close_values[index],
                    "Open": open_candle_1[index],
                    "Periodicidade": 5,
                }
                open_candle_5.append(close_values[index])
                final_candle_list.append(teste0)

            if contator == 10:
                teste = {
                    **element,
                    "Close": close_values[index],
                    "Open": open_candle_5[index],
                    "Periodicidade": 5,
                }
                final_candle_list.append(teste)

                teste2 = {
                    **element,
                    "Close": close_values[index],
                    "Open": open_candle_1[index],
                    "Periodicidade": 10,
                }
                final_candle_list.append(teste2)

        # print(final_candle_list)
        return final_candle_list

    def setup_candles(self) -> None:
        contador = 0
        first_candle_reference = []
        open_candle_5 = []
        while contador < 11:
            response = self.req.get_json_response()
            self.datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]
            coin_list = [response[coin] for coin in self.COINS]
            open_candles = self._map_coin_type(coin_list, self.datetime)
            open_values = [element["Open"] for element in open_candles]
            # print("Fora da função Open")
            print(open_values)
            if contador == 0:
                for index, element in enumerate(open_candles):
                    first_candle_reference.append(element["Open"])

            time.sleep(60)

            response2 = self.req.get_json_response()
            self.datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]
            coin_list = [response2[coin] for coin in self.COINS]
            new_candles = self._map_coin_type(coin_list, self.datetime)
            close_values = [element["Close"] for element in new_candles]
            print(close_values)
            # print("Fora da função Close")
            # print(close_values[1])
            final = self.close_candle(
                self.datetime,
                open_candles,
                new_candles,
                contador,
                first_candle_reference,
                open_candle_5,
                open_values,
                close_values,
            )
            database = Candles()
            database.save_many(final)
            for item in final:
                print(item)
            contador += 1
            if contador == 11:
                contador = 0


a = SetupCandle()
a.setup_candles()
# for item in a.setup_candles():
#     print(item)
# BTC_DASH
# BTC_DOGE
