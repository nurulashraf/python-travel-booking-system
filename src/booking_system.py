class Destination:
    def __init__(self, name, transport_cost, base_accommodation_cost):
        self.name = name
        self.transport_cost = transport_cost
        self.base_accommodation_cost = base_accommodation_cost

    def calculate_base_cost(self):
        return self.transport_cost + self.base_accommodation_cost

    def get_transport_cost(self):
        return self.transport_cost

    def get_accommodation_cost(self):
        return self.base_accommodation_cost

    def set_transport_cost(self, new_cost):
        if new_cost > 0:
            self.transport_cost = new_cost
            return True
        return False

    def set_accommodation_cost(self, new_cost):
        if new_cost > 0:
            self.base_accommodation_cost = new_cost
            return True
        return False

    def format_costs_for_display(self, exchange_rate):
        return f"Destination: {self.name}\n" \
               f"Transport Cost: ${self.transport_cost:.2f} (MYR {self.transport_cost * exchange_rate:.2f})\n" \
               f"Accommodation Cost: ${self.base_accommodation_cost:.2f} (MYR {self.base_accommodation_cost * exchange_rate:.2f})\n" \
               f"Total Base Cost: ${self.calculate_base_cost():.2f} (MYR {self.calculate_base_cost() * exchange_rate:.2f})"

class Person:
    def __init__(self, transport_multiplier, accommodation_multiplier):
        self.transport_multiplier = transport_multiplier
        self.accommodation_multiplier = accommodation_multiplier

    def calculate_transport_cost(self, base_cost):
        return base_cost * self.transport_multiplier

    def calculate_accommodation_cost(self, base_cost, discount=0):
        return base_cost * self.accommodation_multiplier * (1 - discount)

class Adult(Person):
    def __init__(self):
        super().__init__(1.0, 1.0)

class Child(Person):
    def __init__(self):
        super().__init__(0.5, 0.6)

class Family:
    def __init__(self, name, destination, adults, children):
        self.name = name
        self.destination = destination
        self.members = [Adult() for i in range(adults)] + [Child() for i in range(children)]
        self.num_adults = adults
        self.num_children = children
        self.next_family = None

    def calculate_transportation_cost(self):
        base_cost = self.destination.get_transport_cost()
        return sum(member.calculate_transport_cost(base_cost) for member in self.members)

    def calculate_accommodation_cost(self):
        base_cost = self.destination.get_accommodation_cost()

        if self.num_adults == 1:
            adult_discount = 0
        elif self.num_adults == 2:
            adult_discount = 0.15
        else:
            adult_discount = 0.25

        total_cost = 0
        for member in self.members:
            if isinstance(member, Adult):
                total_cost += member.calculate_accommodation_cost(base_cost, adult_discount)
            else:
                total_cost += member.calculate_accommodation_cost(base_cost)
        return total_cost

    def calculate_total_cost(self):
        return self.calculate_transportation_cost() + self.calculate_accommodation_cost()

    def display_summary(self, exchange_rate):
        transport_cost_myr = self.calculate_transportation_cost() * exchange_rate
        accommodation_cost_myr = self.calculate_accommodation_cost() * exchange_rate
        total_cost_myr = self.calculate_total_cost() * exchange_rate

        print(f"Total Cost of {self.name} Family: MYR {total_cost_myr:,.2f}")

class BookingSystem:
    def __init__(self):
        self.destinations = {
            1: Destination("Grand Canyon", 200, 1500),
            2: Destination("Yellowstone National Park", 180, 1700),
            3: Destination("Glacier National Park", 220, 1600),

        }
        self.exchange_rate = 4.2
        self.first_family = None
        self.current_family = None

    def create_family(self, name, destination, adults, children):
        new_family = Family(name, destination, adults, children)

        if not self.first_family:
            self.first_family = new_family
        else:
            self.current_family.next_family = new_family

        self.current_family = new_family
        return new_family

    def display_destinations(self):
        print("\nAvailable Destinations:")
        print("-" * 50)
        for option, destination in self.destinations.items():
            print(f"\n-Option {option}:-")
            print(destination.format_costs_for_display(self.exchange_rate))
        print("-" * 50)

    def display_all_summaries(self):
        if not self.first_family:
            print("\nNo bookings made.")
            return

        print("\n=== Bookings Summary ===\n")
        current = self.first_family
        while current:
            current.display_summary(self.exchange_rate)
            current = current.next_family

def main():
    booking_system = BookingSystem()
    print("- Welcome to SkyHigh Adventures Travel Agency -")
    booking_system.display_destinations()

    while True:
        family_name = input("\nEnter family name (or 'quit' to finish booking): ")
        if family_name.lower() == 'quit':
            break

        while True:
            destination_option = int(input("Enter destination option (1-3): "))
            if destination_option in booking_system.destinations:
                break
            else:
                print("Invalid destination. Please choose 1, 2, or 3.")

        while True:
            num_adults = int(input("Enter number of adults: "))
            if num_adults > 0:
                break
            else:
                print("Number of adults must be greater than 0.")

        while True:
            num_children = int(input("Enter number of children: "))
            if num_children >= 0:
                break
            else:
                print("Number of children cannot be negative.")

        booking_system.create_family(
            family_name,
            booking_system.destinations[destination_option],
            num_adults,
            num_children,

        )
        print("\n[Booking Recorded!]")

    booking_system.display_all_summaries()

main()
