import numpy as np
from typing import List, Tuple, Dict
import random


class Data:
    def __init__(self):
        pass

    def init_from_file(self, file_name: str):
        with open(file_name) as file:
            self.num_rows, self.num_columns, self.num_drones, \
            self.num_turns, self.max_payload = map(int, file.readline().split(" "))
            self.num_products = int(file.readline())
            self.product_weights = list(map(int, file.readline().split(" ")))
            print(self.__dict__.items())


def main():
    data = Data()
    data.init_from_file("busy_day.in")


if __name__ == '__main__':
    main()
