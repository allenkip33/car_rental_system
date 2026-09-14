from datetime import date
from models.rental import Rental

class RentalService:
    def __init__(self, data_manager, rentals_file, cars_file):
        self.data_manager = data_manager
        self.rentals_file = rentals_file
        self.cars_file = cars_file

    def dates_overlap(self, start1_str, end1_str, start2_str, end2_str):
        s1 = date.fromisoformat(start1_str)
        e1 = date.fromisoformat(end1_str)
        s2 = date.fromisoformat(start2_str)
        e2 = date.fromisoformat(end2_str)
        return s1 < e2 and e1 > s2

    def create_rental(self, username, car_id, start_date, end_date):
        cars = self.data_manager.load_data(self.cars_file)
        rentals = self.data_manager.load_data(self.rentals_file)

        car = next((item for item in cars if item["car_id"] == car_id), None)
        if car is None or not car["available"]:
            return None

        for r_dict in rentals:
            if r_dict["car_id"] == car_id and r_dict["status"] == "Active":
                if self.dates_overlap(start_date, end_date, r_dict["start_date"], r_dict["end_date"]):
                    return None

        rental_id = f"R{len(rentals) + 1}"
        
        rental_obj = Rental(
            rental_id,
            username,
            car_id,
            start_date,
            end_date,
            car["price_per_day"]
        )

        rentals.append(rental_obj.to_dict())
        car["available"] = False

        self.data_manager.save_data(self.rentals_file, rentals)
        self.data_manager.save_data(self.cars_file, cars)

        return rental_obj

    def cancel_rental(self, rental_id):
        rentals = self.data_manager.load_data(self.rentals_file)
        cars = self.data_manager.load_data(self.cars_file)

        for rental in rentals:
            if rental["rental_id"] == rental_id:
                if rental["status"] == "Cancelled":
                    return False

                rental["status"] = "Cancelled"
                
                for car in cars:
                    if car["car_id"] == rental["car_id"]:
                        car["available"] = True

                self.data_manager.save_data(self.rentals_file, rentals)
                self.data_manager.save_data(self.cars_file, cars)
                return True

        return False