from models.car import Car


def test_create_car():
    car = Car("C001", "Toyota", "Corolla", 2022, 3000)

    assert car.car_id == "C001"
    assert car.brand == "Toyota"
    assert car.available is True


def test_car_availability():
    car = Car("C002", "Honda", "Civic", 2023, 3500)

    car.set_available(False)

    assert car.available is False
