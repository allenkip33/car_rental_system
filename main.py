from rich.console import Console
from rich.table import Table

from services.auth import AuthService
from services.data_manager import DataManager
from services.rental_service import RentalService
from utils.validators import validate_date, validate_required
from utils.decorators import login_required

console = Console()

USERS_FILE = "data/users.json"
CARS_FILE = "data/cars.json"
RENTALS_FILE = "data/rentals.json"

manager = DataManager()
auth = AuthService(manager, USERS_FILE)
rental_service = RentalService(manager, RENTALS_FILE, CARS_FILE)

require_auth = login_required(auth)

def register():
    console.print("\n--- Register ---")
    username = input("Enter username: ")
    password = input("Enter password: ")

    if not validate_required(username) or not validate_required(password):
        console.print("[red]Username and password are required.[/red]")
        return

    if auth.register(username, password):
        console.print("[green]User registered successfully.[/green]")
    else:
        console.print("[red]Username already exists.[/red]")

def login():
    console.print("\n--- Login ---")
    username = input("Enter username: ")
    password = input("Enter password: ")

    user = auth.login(username, password)
    if user:
        console.print(f"[green]Login successful. Welcome {user.username}![/green]")
        console.print(f"Role: {user.role}")
        return user

    console.print("[red]Invalid username or password.[/red]")
    return None

def list_cars():
    cars = manager.load_data(CARS_FILE)
    if not cars:
        console.print("[yellow]No cars found.[/yellow]")
        return

    table = Table(title="Available Cars")
    table.add_column("ID")
    table.add_column("Brand")
    table.add_column("Model")
    table.add_column("Year")
    table.add_column("Price/Day")
    table.add_column("Available")

    for car in cars:
        table.add_row(
            car["car_id"], car["brand"], car["model"],
            str(car["year"]), str(car["price_per_day"]), str(car["available"])
        )
    console.print(table)

@require_auth
def add_car():
    user = auth.current_user
    if user.role != "Admin":
        console.print("[red]Only an Admin can add cars.[/red]")
        return

    console.print("\n--- Add Car ---")
    car_id = input("Enter car ID: ")
    brand = input("Enter brand: ")
    model = input("Enter model: ")
    year = input("Enter year: ")
    price = input("Enter price per day: ")

    if not validate_required(car_id):
        console.print("[red]Car ID is required.[/red]")
        return

    cars = manager.load_data(CARS_FILE)
    if any(car["car_id"] == car_id for car in cars):
        console.print("[red]Car ID already exists.[/red]")
        return

    try:
        new_car = {
            "car_id": car_id,
            "brand": brand,
            "model": model,
            "year": int(year),
            "price_per_day": float(price),
            "available": True
        }
    except ValueError:
        console.print("[red]Year and price must be valid numbers.[/red]")
        return

    cars.append(new_car)
    manager.save_data(CARS_FILE, cars)
    console.print("[green]Car added successfully.[/green]")

@require_auth
def rent_car():
    user = auth.current_user
    console.print("\n--- Rent a Car ---")
    list_cars()

    car_id = input("Enter car ID: ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    if not validate_date(start_date) or not validate_date(end_date):
        console.print("[red]Invalid date format detected.[/red]")
        return

    rental = rental_service.create_rental(user.username, car_id, start_date, end_date)
    if rental:
        console.print("\n[green]Car rented successfully.[/green]")
        console.print(f"Rental ID: {rental.rental_id}")
        console.print(f"Total cost: {rental.total_cost()}")
    else:
        console.print("\n[red]Could not rent the car. Check availability or schedule overlaps.[/red]")

@require_auth
def list_rentals():
    user = auth.current_user
    rentals = manager.load_data(RENTALS_FILE)
    user_rentals = [r for r in rentals if r["username"] == user.username or user.role == "Admin"]

    if not user_rentals:
        console.print("[yellow]No rentals found.[/yellow]")
        return

    table = Table(title="Rentals")
    table.add_column("Rental ID")
    table.add_column("Username")
    table.add_column("Car ID")
    table.add_column("Start")
    table.add_column("End")
    table.add_column("Status")

    for r in user_rentals:
        table.add_row(r["rental_id"], r["username"], r["car_id"], r["start_date"], r["end_date"], r["status"])
    console.print(table)

@require_auth
def cancel_rental():
    user = auth.current_user
    console.print("\n--- Cancel Rental ---")
    list_rentals()

    rental_id = input("Enter rental ID to cancel: ")
    rentals = manager.load_data(RENTALS_FILE)
    
    rental_item = next((r for r in rentals if r["rental_id"] == rental_id), None)
    if not rental_item:
        console.print("[red]Rental record not found.[/red]")
        return

    if rental_item["username"] != user.username and user.role != "Admin":
        console.print("[red]You are not authorized to cancel this rental.[/red]")
        return

    if rental_service.cancel_rental(rental_id):
        console.print("[green]Rental cancelled successfully.[/green]")
    else:
        console.print("[red]Could not process cancellation at this time.[/red]")

def main():
    while True:
        console.print("    CAR RENTAL SYSTEM")
        console.print("================================")

        if auth.current_user:
            console.print(f"Logged in as: [cyan]{auth.current_user.username}[/cyan] ({auth.current_user.role})")

        console.print("\n1. Register\n2. Login\n3. List Cars\n4. Add Car (Admin)\n5. Rent a Car\n6. My Rentals\n7. Cancel Rental\n8. Logout\n9. Exit")
        choice = input("\nEnter your choice: ")

        if choice == "1": register()
        elif choice == "2": login()
        elif choice == "3": list_cars()
        elif choice == "4": add_car()
        elif choice == "5": rent_car()
        elif choice == "6": list_rentals()
        elif choice == "7": cancel_rental()
        elif choice == "8":
            auth.logout()
            console.print("[green]Logged out successfully.[/green]")
        elif choice == "9":
            console.print("Thank you for using the Car Rental System.")
            break
        else:
            console.print("[red]Invalid choice. Please select 1-9.[/red]")

if __name__ == "__main__":
    main()
