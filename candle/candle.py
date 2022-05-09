class Candle(object):
    def __init__(
        self,
        moeda: str,
        periodicidade: int,
        datetime: str,
        open: str,
        low: str,
        high: str,
        close: str,
    ) -> None:
        self.moeda = moeda
        self.periodicidade = periodicidade
        self.datetime = datetime
        self.open = open
        self.low = low
        self.high = high
        self.close = close
