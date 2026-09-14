class Car:
    def __init__(self, car_id, brand, model, year, price_per_day):
        self._car_id = car_id
        self._brand = brand
        self._model = model
        self._year = year
        self._price_per_day = price_per_day
        self._available = True

    @property
    def car_id(self):
        return self._car_id

    @property
    def brand(self):
        return self._brand

    @property
    def model(self):
        return self._model

    @property
    def year(self):
        return self._year

    @property
    def price_per_day(self):
        return self._price_per_day

    @property
    def available(self):
        return self._available

    def set_available(self, available):
        self._available = available

    def to_dict(self):
        return {
            "car_id": self._car_id,
            "brand": self._brand,
            "model": self._model,
            "year": self._year,
            "price_per_day": self._price_per_day,
            "available": self._available
        }
