import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


engine = db.create_engine(
    "mysql+pymysql://kaiquecosta:Python123@127.0.0.1:3306/smarttbot"
)
conecction = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class CandlesModel(Base):
    __tablename__ = "candles"

    id = Column(Integer, primary_key=True)
    Moeda = Column(String(10), index=True)
    Periodicidade = Column(Integer)
    Datetime = Column(String(120), index=True)
    Open = Column(String(10), index=True)
    Low = Column(String(10), index=True)
    High = Column(String(10), index=True)
    Close = Column(String(10), index=True)

    def __repr__(self) -> str:
        return (
            f"Candle: {self.Moeda} {self.Periodicidade} {self.Datetime} "
            f" {self.Open} {self.Low} {self.High} {self.Close}"
        )

    @classmethod
    def save_many(cls, lista: list) -> None:
        candle_list = [CandlesModel(**item) for item in lista]
        session.add_all(candle_list)
        session.commit()


Base.metadata.create_all(bind=engine)
