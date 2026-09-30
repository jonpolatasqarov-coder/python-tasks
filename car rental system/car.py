from vehicle import Vehicle

 
class Car(Vehicle):
    def rent(self, days):
        if days <= 0:
            print("Invalid number of rental days.")
            return False
        
        if not self.is_available:
            print(f"{self.name} is not available.")
            return False

        self.is_available = False
        self.rental_count += 1
        print(f"{self.name} rented for {days} day(s).")
        return True
    
    def return_vehicle(self):
        if self.is_available:
            print(f"{self.name} is already available.")
            return False
        
        self.is_available = True
        print(f"{self.name} has been returned.")
        return True

    def calculate_rent(self, days):
        total = self.price_per_day * days

        if self.rental_count > 3:
            total *= 0.8

        return total

