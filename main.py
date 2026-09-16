from rich.console import Console

from services.auth import AuthService
from services.data_manager import DataManager
from services.rental_service import RentalService
from utils.decorators import login_required, admin_required
from utils.validators import validate_date, validate_price, validate_required


console = Console()

USERS_FILE = "data/user.json"
CARS_FILE = "data/cars.json"
RENTALS_FILE = "data/rentals.json"

manager = DataManager()
auth = AuthService(manager, USERS_FILE)
rental_service = RentalService(manager, RENTALS_FILE, CARS_FILE)

require_auth = login_required(auth)
require_admin = admin_required(auth)


def show_header(title):
    console.print()
    console.print("----------------------------------------")
    console.print(f"            {title}")
    console.print("----------------------------------------")


def register():
    show_header("REGISTER")

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if not validate_required(username) or not validate_required(password):
        console.print("Username and password are required.")
        return

    console.print("\nAccount type:")
    console.print("1. Customer")
    console.print("2. Admin")

    role_choice = input("Choose account type: ").strip()

    if role_choice == "1":
        role = "Customer"
    elif role_choice == "2":
        role = "Admin"
    else:
        console.print("Invalid account type.")
        return

    if auth.register(username, password, role):
        console.print("Account created successfully.")

        user = auth.login(username, password)

        if user:
            console.print(f"Welcome, {user.username}!")
    else:
        console.print("Username already exists.")


def login():
    show_header("LOGIN")

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    user = auth.login(username, password)

    if user:
        console.print(f"\nLogin successful. Welcome, {user.username}!")
        return True

    console.print("Invalid username or password.")
    return False


def list_cars():
    cars = manager.load_data(CARS_FILE)

    if not cars:
        console.print("\nNo cars found.")
        return

    console.print("\nID       Brand       Model       Year       Price/Day       Status")
    console.print("---------------------------------------------------------------------")

    for car in cars:
        status = "Available" if car["available"] else "Rented"

        console.print(
            f"{car['car_id']:<8}"
            f"{car['brand']:<12}"
            f"{car['model']:<12}"
            f"{car['year']:<11}"
            f"KSh {car['price_per_day']:<10.2f}"
            f"{status}"
        )


@require_admin
def add_car():
    show_header("ADD CAR")

    car_id = input("Car ID: ").strip()
    brand = input("Brand: ").strip()
    model = input("Model: ").strip()
    year = input("Year: ").strip()
    price = input("Price per day: ").strip()

    if not validate_required(car_id):
        console.print("Car ID is required.")
        return

    if not validate_required(brand) or not validate_required(model):
        console.print("Brand and model are required.")
        return

    try:
        year = int(year)
    except ValueError:
        console.print("Year must be a number.")
        return

    if not validate_price(price):
        console.print("Price must be greater than zero.")
        return

    cars = manager.load_data(CARS_FILE)

    if any(car["car_id"] == car_id for car in cars):
        console.print("That car ID already exists.")
        return

    price = str(price).replace(",", "")

    new_car = {
        "car_id": car_id,
        "brand": brand,
        "model": model,
        "year": year,
        "price_per_day": float(price),
        "available": True
    }

    cars.append(new_car)
    manager.save_data(CARS_FILE, cars)

    console.print("\nCar added successfully.")


@require_admin
def delete_car():
    show_header("DELETE CAR")

    cars = manager.load_data(CARS_FILE)

    if not cars:
        console.print("There are no cars to delete.")
        return

    list_cars()

    car_id = input("\nEnter the car ID to delete: ").strip()

    car = next(
        (car for car in cars if car["car_id"] == car_id),
        None
    )

    if car is None:
        console.print("Car not found.")
        return

    if not car["available"]:
        console.print("A rented car cannot be deleted.")
        return

    cars.remove(car)
    manager.save_data(CARS_FILE, cars)

    console.print("Car deleted successfully.")


@require_auth
def rent_car():
    if auth.current_user.role != "Customer":
        console.print("\nOnly customers can rent cars.")
        return

    show_header("RENT A CAR")

    list_cars()

    car_id = input("\nCar ID: ").strip()
    start_date = input("Start date (YYYY-MM-DD): ").strip()
    end_date = input("End date (YYYY-MM-DD): ").strip()

    if not validate_date(start_date) or not validate_date(end_date):
        console.print("Please enter valid dates.")
        return

    rental = rental_service.create_rental(
        auth.current_user.username,
        car_id,
        start_date,
        end_date
    )

    if rental:
        console.print("\nCar rented successfully.")
        console.print(f"Rental ID: {rental.rental_id}")
        console.print(f"Total cost: KSh {rental.total_cost():.2f}")
    else:
        console.print(
            "\nCould not rent the car. "
            "Check the car ID, availability, or rental dates."
        )


@require_auth
def list_rentals():
    show_header("RENTALS")

    rentals = manager.load_data(RENTALS_FILE)

    if auth.current_user.role == "Admin":
        user_rentals = rentals
    else:
        user_rentals = [
            rental
            for rental in rentals
            if rental["username"] == auth.current_user.username
        ]

    if not user_rentals:
        console.print("No rentals found.")
        return

    console.print(
        "\nRental ID    Username       Car ID       Start Date    End Date      Status"
    )
    console.print(
        "----------------------------------------------------------------------------"
    )

    for rental in user_rentals:
        console.print(
            f"{rental['rental_id']:<13}"
            f"{rental['username']:<15}"
            f"{rental['car_id']:<13}"
            f"{rental['start_date']:<14}"
            f"{rental['end_date']:<14}"
            f"{rental['status']}"
        )


@require_auth
def cancel_rental():
    show_header("CANCEL RENTAL")

    rentals = manager.load_data(RENTALS_FILE)

    if auth.current_user.role == "Admin":
        user_rentals = rentals
    else:
        user_rentals = [
            rental
            for rental in rentals
            if rental["username"] == auth.current_user.username
        ]

    if not user_rentals:
        console.print("No rentals found.")
        return

    list_rentals()

    rental_id = input("\nRental ID: ").strip()

    rental = next(
        (item for item in rentals if item["rental_id"] == rental_id),
        None
    )

    if rental is None:
        console.print("Rental not found.")
        return

    if (
        rental["username"] != auth.current_user.username
        and auth.current_user.role != "Admin"
    ):
        console.print("You cannot cancel this rental.")
        return

    if rental["status"] == "Cancelled":
        console.print("This rental is already cancelled.")
        return

    if rental_service.cancel_rental(rental_id):
        console.print("Rental cancelled successfully.")
    else:
        console.print("Could not cancel the rental.")


def customer_menu():
    while auth.current_user:
        show_header("CUSTOMER DASHBOARD")

        console.print(f"Welcome, {auth.current_user.username}!")

        console.print("\n1. View Available Cars")
        console.print("2. Rent a Car")
        console.print("3. My Rentals")
        console.print("4. Cancel Rental")
        console.print("5. Logout")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            list_cars()
        elif choice == "2":
            rent_car()
        elif choice == "3":
            list_rentals()
        elif choice == "4":
            cancel_rental()
        elif choice == "5":
            auth.logout()
            console.print("Logged out successfully.")
        else:
            console.print("Invalid choice.")


def admin_menu():
    while auth.current_user:
        show_header("ADMIN DASHBOARD")

        console.print(f"Welcome, {auth.current_user.username}!")

        console.print("\n1. View Cars")
        console.print("2. Add Car")
        console.print("3. Delete Car")
        console.print("4. View Rentals")
        console.print("5. Logout")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            list_cars()
        elif choice == "2":
            add_car()
        elif choice == "3":
            delete_car()
        elif choice == "4":
            list_rentals()
        elif choice == "5":
            auth.logout()
            console.print("Logged out successfully.")
        else:
            console.print("Invalid choice.")


def main():
    while True:
        show_header("CAR RENTAL SYSTEM")

        console.print("1. Login")
        console.print("2. Register")
        console.print("3. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            if login():
                if auth.current_user.role == "Admin":
                    admin_menu()
                else:
                    customer_menu()

        elif choice == "2":
            register()

            if auth.current_user:
                if auth.current_user.role == "Admin":
                    admin_menu()
                else:
                    customer_menu()

        elif choice == "3":
            console.print(
                "\nThank you for using the Car Rental System."
            )
            break

        else:
            console.print("Invalid choice.")


if _name_ == "_main_":
    main()