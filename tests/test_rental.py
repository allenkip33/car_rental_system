from models.rental import Rental


def test_rental_days():
    rental = Rental(
        "R001",
        "john",
        "C001",
        "2026-09-12",
        "2026-09-15",
        3000
    )

    assert rental.rental_days() == 3


def test_total_cost():
    rental = Rental(
        "R002",
        "john",
        "C001",
        "2026-09-12",
        "2026-09-15",
        3000
    )

    assert rental.total_cost() == 9000


def test_cancel_rental():
    rental = Rental(
        "R003",
        "john",
        "C001",
        "2026-09-12",
        "2026-09-15",
        3000
    )

    rental.cancel()

    assert rental.status == "Cancelled"
