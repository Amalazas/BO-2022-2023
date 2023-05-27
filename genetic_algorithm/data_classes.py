from bitarray import bitarray


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


class Package:
    def __init__(self, index: int, weight: float, volume: float, position: Point, priority: int) -> None:
        self.index = index
        self.weight = weight
        self.volume = volume
        self.position = position
        self.priority = priority

    def __str__(self) -> str:
        return f"Package {self.index} with weight {self.weight} and volume {self.volume} at {self.position} with priority {self.priority}"


class PermSolution:
    def __init__(self, choice: bitarray, perm: list[int]) -> None:
        self.choice = choice
        self.perm = perm

    def __str__(self) -> str:
        return f"{self.choice}, {self.perm}"


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
