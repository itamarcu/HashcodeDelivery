import math
from typing import List, Dict

ProductCounts = Dict[int, int]


class Place:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Drone(Place):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.inventory: ProductCounts = {}
        self.cooldown_left = 0


class Warehouse(Place):
    def __init__(self, x, y, inventory: ProductCounts):
        super().__init__(x, y)
        self.inventory: ProductCounts = inventory
        """starting counts of each product in inventory"""
        self.active_inventory: ProductCounts = inventory.copy()
        """active counts of each product in inventory"""
        self.assigned_orders: Dict[Person, ProductCounts] = {}

    def __repr__(self):
        return f"x:{self.x}, y:{self.y}, inventory size {len(self.inventory)}"


class Person(Place):
    def __init__(self, x, y, wishlist: ProductCounts):
        super().__init__(x, y)
        self.wishlist: ProductCounts = wishlist
        """counts of each product in wishlist"""

    def __repr__(self):
        return f"x:{self.x}, y:{self.y}, wishlist size {len(self.wishlist)}"


class Data:
    def __init__(self, file_name: str):
        with open(file_name) as file:
            self.num_rows, self.num_columns, self.num_drones, \
            self.num_turns, self.max_payload = map(int, file.readline().split(" "))
            self.num_products = int(file.readline())
            self.product_weights = list(map(int, file.readline().split(" ")))
            self.num_warehouses = int(file.readline())
            self.warehouses: List[Warehouse] = []
            for _ in range(self.num_warehouses):
                x, y = map(int, file.readline().split(" "))
                inventory_counts = list(map(int, file.readline().split(" ")))
                inventory = {}
                for i in range(self.num_products):
                    if inventory_counts[i] > 0:
                        inventory[i] = inventory_counts[i]
                self.warehouses.append(Warehouse(x, y, inventory))
            self.num_people = int(file.readline())
            self.people: List[Person] = []
            for _ in range(self.num_people):
                x, y = map(int, file.readline().split(" "))
                wishlist_size = int(file.readline())
                uncompressed_wishlist = list(map(int, file.readline().split(" ")))
                wishlist_counts = [0 for _ in range(self.num_products)]
                for i in range(wishlist_size):
                    wishlist_counts[uncompressed_wishlist[i]] += 1
                wishlist = {}
                for i in range(self.num_products):
                    if wishlist_counts[i] > 0:
                        wishlist[i] = wishlist_counts[i]
                self.people.append(Person(x, y, wishlist))
            x0, y0 = self.warehouses[0].x, self.warehouses[0].y
            self.drones: List[Drone] = [Drone(x0, y0) for _ in range(self.num_drones)]


def distance_squared(place1: Place, place2: Place):
    return (place1.x - place2.x) ** 2 + (place1.y - place2.y) ** 2


def calc_key(person: Person, warehouse: Warehouse, data: Data):
    total = 0
    for (product, amount) in person.wishlist.items():
        total += min(amount, warehouse.inventory.get(product, 0))
    naglas = total // data.max_payload
    percentage = total / sum(person.wishlist.values())
    if percentage == 0:
        return math.inf
    return distance_squared(person, warehouse) * naglas / percentage


def main():
    data = Data("mother_of_all_warehouses.in")

    data.warehouses.sort(key=lambda warehouse: sum(warehouse.inventory), reverse=True)
    for warehouse in data.warehouses:
        data.people.sort(key=lambda person: calc_key(person, warehouse, data))
        for person in data.people:
            assigned_order: ProductCounts = {}
            for i in person.wishlist.keys():
                product_in_order = min(person.wishlist.get(i, 0), warehouse.active_inventory.get(i, 0))
                if product_in_order == 0:
                    continue
                assigned_order[i] = product_in_order
                warehouse.active_inventory[i] -= product_in_order
            if len(assigned_order) == 0:
                continue
            warehouse.assigned_orders[person] = assigned_order

    # game time

    print("DONE")


if __name__ == '__main__':
    main()
