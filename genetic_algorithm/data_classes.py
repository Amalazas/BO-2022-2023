from bitarray import bitarray
import math


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = float(x)
        self.y = float(y)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __iter__(self):
        return iter((self.x, self.y))

    def __getitem__(self, index: int) -> float:
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Index out of range")

    def distance_to(self, other_point: "Point") -> float:
        return math.sqrt((self.x - other_point.x) ** 2 + (self.y - other_point.y) ** 2)


class Package:
    def __init__(
        self, index: int, weight: float, volume: float, position: Point, priority: int
    ) -> None:
        self.index = int(index)
        self.weight = float(weight)
        self.volume = float(volume)
        self.position = Point(*position)
        self.priority = int(priority)

    def __iter__(self):
        return iter(
            (self.index, self.weight, self.volume, self.position, self.priority)
        )

    def __str__(self) -> str:
        return f"Package {self.index} with weight {self.weight} and volume {self.volume} at {self.position} with priority {self.priority}"

    def __getitem__(self, index: int):
        if index == 0:
            return self.index
        elif index == 1:
            return self.weight
        elif index == 2:
            return self.volume
        elif index == 3:
            return self.position
        elif index == 4:
            return self.priority
        else:
            raise IndexError("Index out of range")

    def distance_to(self, other_package: "Package") -> float:
        return self.position.distance_to(other_package.position)


def convert_to_package_list(
    packages: list[tuple[int, float, float, tuple[float, float], int]]
) -> list[Package]:
    return [Package(*package) for package in packages]


class PermSolution:
    def __init__(self, choice: bitarray, perm: list[int]) -> None:
        self.choice = choice
        self.perm = perm
        self.age = 0
        self.was_aged = False

    def __str__(self) -> str:
        return f"{self.choice}, {self.perm}, {self.age}"


class MatSolution:
    def __init__(self, matrix: list[list[int]]) -> None:
        self.matrix = matrix

    def __str__(self) -> str:
        matrix_str = ""
        for row in self.matrix:
            for el in row:
                matrix_str += str(el) + " "
            matrix_str += "\n"
        return matrix_str
