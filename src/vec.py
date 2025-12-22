from dataclasses import dataclass
from math import acos, sqrt
from omnim.math import to_degrees
from typing import overload


@dataclass
class vector3:
    x: float = 0
    y: float = 0
    z: float = 0

    @staticmethod
    def zero() -> "vector3":
        return vector3()

    @staticmethod
    def one() -> "vector3":
        return vector3(1, 1, 1)

    @property
    def magnitude(self) -> float:
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    @property
    def normalized(self) -> "vector3":
        return self / self.magnitude

    def __eq__(self, a: "vector2 | vector3") -> bool:
        a = a if isinstance(a, vector3) else vector3(a.x, a.y)
        return self.x == a.x and self.y == a.y and self.z == a.z

    def __ne__(self, a: "vector2 | vector3") -> bool:
        return not self.__eq__(a)

    def __ge__(self, a: "vector2 | vector3") -> bool:
        a = a if isinstance(a, vector3) else vector3(a.x, a.y)
        return self.x >= a.x and self.y >= a.y and self.z >= a.z

    def __gt__(self, a: "vector2 | vector3") -> bool:
        a = a if isinstance(a, vector3) else vector3(a.x, a.y)
        return self.x > a.x and self.y > a.y and self.z > a.z

    def __le__(self, a: "vector2 | vector3") -> bool:
        a = a if isinstance(a, vector3) else vector3(a.x, a.y)
        return self.x <= a.x and self.y <= a.y and self.z <= a.z

    def __lt__(self, a: "vector2 | vector3") -> bool:
        a = a if isinstance(a, vector3) else vector3(a.x, a.y)
        return self.x < a.x and self.y < a.y and self.z < a.z

    def __pos__(self) -> "vector3":
        return self

    def __neg__(self) -> "vector3":
        return vector3(-self.x, -self.y, -self.z)

    def __add__(self, a: "vector2 | vector3") -> "vector3":
        if isinstance(a, vector3):
            return vector3(self.x + a.x, self.y + a.y, self.z + a.z)
        elif isinstance(a, vector2):
            return vector3(self.x + a.x, self.y + a.y, self.z)
        else:
            raise TypeError

    def __radd__(self, a: "vector2") -> "vector3":
        return vector3(a.x, a.y) + self

    def __iadd__(self, a: "vector2 | vector3") -> "vector3":
        _a = vector3(a.x, a.y) if isinstance(a, vector2) else a
        self.x += _a.x
        self.y += _a.y
        self.z += _a.z
        return self

    def __sub__(self, a: "vector2 | vector3") -> "vector3":
        _a = vector3(a.x, a.y) if isinstance(a, vector2) else a
        return self + vector3(-_a.x, -_a.y, -_a.z)

    def __rsub__(self, a: "vector2") -> "vector3":
        return vector3(a.x, a.y) - self

    def __isub__(self, a: "vector2 | vector3") -> "vector3":
        self += -a
        return self

    def __mul__(self, a: "vector2 | vector3 | int | float") -> "vector3":
        if isinstance(a, (int, float)):
            return vector3(self.x * a, self.y * a, self.z * a)
        elif isinstance(a, (vector3, vector2)):
            _a = vector3(a.x, a.y) if isinstance(a, vector2) else a
            return vector3(self.x * _a.x, self.y * _a.y, self.z * _a.z)
        else:
            raise TypeError

    def __rmul__(self, a: "vector2 | vector3 | int | float") -> "vector3":
        if isinstance(a, (int, float)):
            return vector3(a * self.x, a * self.y, a * self.z)
        elif isinstance(a, (vector3, vector2)):
            _a = vector3(a.x, a.y) if isinstance(a, vector2) else a
            return vector3(_a.x * self.x, _a.y * self.y, _a.z * self.z)
        else:
            raise TypeError

    def __imul__(self, a: "vector2 | vector3 | int | float") -> "vector3":
        _a = self * a
        self.x = _a.x
        self.y = _a.y
        self.z = _a.z
        return self

    def __pow__(self, a: "vector2 | vector3 | int | float") -> "vector3":
        if isinstance(a, (int, float)):
            return vector3(self.x**a, self.y**a, self.z**a)
        elif isinstance(a, (vector3, vector2)):
            _a = vector3(a.x, a.y) if isinstance(a, vector2) else a
            return vector3(self.x**_a.x, self.y**_a.y, self.z**_a.z)
        else:
            raise TypeError

    def __rpow__(self, a: "vector2 | vector3 | int | float") -> "vector3":
        if isinstance(a, (int, float)):
            return vector3(a**self.x, a**self.y, a**self.z)
        elif isinstance(a, (vector3, vector2)):
            _a = vector3(a.x, a.y) if isinstance(a, vector2) else a
            return vector3(_a.x**self.x, _a.y**self.y, _a.z**self.z)
        else:
            raise TypeError

    def __ipow__(self, a: "vector2 | vector3 | int | float") -> "vector3":
        _a = self**a
        self.x = _a.x
        self.y = _a.y
        self.z = _a.z
        return self

    def __truediv__(self, a: "vector2 | vector3 | int | float") -> "vector3":
        if isinstance(a, (int, float)):
            return vector3(self.x / a, self.y / a, self.z / a)
        elif isinstance(a, (vector3, vector2)):
            _a = vector3(a.x, a.y) if isinstance(a, vector2) else a
            return vector3(self.x / _a.x, self.y / _a.y, self.z / _a.z)
        else:
            raise TypeError

    def __itruediv__(self, a: "vector2 | vector3 | int | float") -> "vector3":
        _a = self / (a)
        self.x = _a.x
        self.y = _a.y
        self.z = _a.z
        return self

    def __floordiv__(self, a: "vector2 | vector3 | int | float") -> "vector3":
        if isinstance(a, (int, float)):
            return vector3(self.x // a, self.y // a, self.z // a)
        elif isinstance(a, (vector3, vector2)):
            _a = vector3(a.x, a.y) if isinstance(a, vector2) else a
            return vector3(self.x // _a.x, self.y // _a.y, self.z // _a.z)
        else:
            raise TypeError

    def __ifloordiv__(self, a: "vector2 | vector3 | int | float") -> "vector3":
        _a = self // a
        self.x = _a.x
        self.y = _a.y
        self.z = _a.z
        return self

    def __getitem__(self, k: int) -> float:
        return (self.x, self.y, self.z)[k % 3]

    def __setitem__(self, k: int, v: float) -> float:
        match k % 3:
            case 0:
                self.x = v
            case 1:
                self.y = v
            case 2:
                self.z = v
        return v

    def __str__(self) -> str:
        return f"({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"


@dataclass
class vector2:
    x: float = 0
    y: float = 0

    @staticmethod
    def zero() -> "vector2":
        return vector2()

    @staticmethod
    def one() -> "vector2":
        return vector2(1, 1)

    @property
    def magnitude(self) -> float:
        return sqrt(self.x**2 + self.y**2)

    @property
    def normalized(self) -> "vector2":
        return self / self.magnitude

    def __eq__(self, a: "vector2 | vector3") -> bool:
        a = a if isinstance(a, vector3) else vector3(a.x, a.y)
        return self.x == a.x and self.y == a.y and self.z == a.z

    def __ne__(self, a: "vector2 | vector3") -> bool:
        return not self.__eq__(a)

    def __ge__(self, a: "vector2 | vector3") -> bool:
        a = a if isinstance(a, vector3) else vector3(a.x, a.y)
        return self.x >= a.x and self.y >= a.y and self.z >= a.z

    def __gt__(self, a: "vector2 | vector3") -> bool:
        a = a if isinstance(a, vector3) else vector3(a.x, a.y)
        return self.x > a.x and self.y > a.y and self.z > a.z

    def __le__(self, a: "vector2 | vector3") -> bool:
        a = a if isinstance(a, vector3) else vector3(a.x, a.y)
        return self.x <= a.x and self.y <= a.y and self.z <= a.z

    def __lt__(self, a: "vector2 | vector3") -> bool:
        a = a if isinstance(a, vector3) else vector3(a.x, a.y)
        return self.x < a.x and self.y < a.y and self.z < a.z

    def __pos__(self) -> "vector2":
        return self

    def __neg__(self) -> "vector2":
        return vector2(-self.x, -self.y)

    def __add__(self, a: "vector2") -> "vector2":
        return vector2(self.x + a.x, self.y + a.y)

    def __radd__(self, a: "vector2") -> "vector2":
        return a + self

    def __iadd__(self, a: "vector2") -> "vector2":
        self.x += a.x
        self.y += a.y
        self.z += a.z
        return self

    def __sub__(self, a: "vector2") -> "vector2":
        return self + -a

    def __rsub__(self, a: "vector2") -> "vector2":
        return a - self

    def __isub__(self, a: "vector2") -> "vector2":
        self += -a
        return self

    def __mul__(self, a: "vector2 | int | float") -> "vector2":
        if isinstance(a, (int, float)):
            return vector2(self.x * a, self.y * a)
        elif isinstance(a, vector2):
            return vector2(self.x * a.x, self.y * a.y)
        else:
            raise TypeError

    def __rmul__(self, a: "vector2 | int | float") -> "vector2":
        if isinstance(a, (int, float)):
            return vector2(a * self.x, a * self.y)
        elif isinstance(a, vector2):
            return a * self
        else:
            raise TypeError

    def __imul__(self, a: "vector2 | int | float") -> "vector2":
        a = self * a
        self.x = a.x
        self.y = a.y
        self.z = a.z
        return self

    def __pow__(self, a: "vector2 | int | float") -> "vector2":
        if isinstance(a, (int, float)):
            return vector2(self.x**a, self.y**a)
        elif isinstance(a, vector2):
            return vector2(self.x**a.x, self.y**a.y)
        else:
            raise TypeError

    def __rpow__(self, a: "vector2 | int | float") -> "vector2":
        if isinstance(a, (int, float)):
            return vector2(a**self.x, a**self.y)
        elif isinstance(a, vector2):
            return vector2(a.x**self.x, a.y**self.y)
        else:
            raise TypeError

    def __ipow__(self, a: "vector2 | int | float") -> "vector2":
        a = self**a
        self.x = a.x
        self.y = a.y
        return self

    def __truediv__(self, a: "vector2 | int | float") -> "vector2":
        if isinstance(a, (int, float)):
            return vector2(self.x / a, self.y / a)
        elif isinstance(a, vector2):
            return vector2(self.x / a.x, self.y / a.y)
        else:
            raise TypeError

    def __itruediv__(self, a: "vector2 | int | float") -> "vector2":
        a = self / a
        self.x = a.x
        self.y = a.y
        return self

    def __floordiv__(self, a: "vector2 | int | float") -> "vector2":
        if isinstance(a, (int, float)):
            return vector2(self.x // a, self.y // a)
        elif isinstance(a, vector2):
            return vector2(self.x // a.x, self.y // a.y)
        else:
            raise TypeError

    def __ifloordiv__(self, a: "vector2 | int | float") -> "vector2":
        a = self // a
        self.x = a.x
        self.y = a.y
        self.z = a.z
        return self

    def __getitem__(self, k: int) -> float:
        return (self.x, self.y)[k % 2]

    def __setitem__(self, k: int, v: float) -> float:
        match k % 2:
            case 0:
                self.x = v
            case 1:
                self.y = v
        return v

    def __str__(self) -> str:
        return f"({self.x:.3f}, {self.y:.3f})"

    def __repr__(self) -> str:
        return self.__str__()


@overload
def dot(a: vector3, b: vector3) -> float: ...
@overload
def dot(a: vector2, b: vector2) -> float: ...
@overload
def dot(a: vector2, b: vector3) -> float: ...
@overload
def dot(a: vector3, b: vector2) -> float: ...
def dot(a: vector3 | vector2, b: vector3 | vector2) -> float:
    a = a if isinstance(a, vector3) else vector3(a.x, a.y)
    b = b if isinstance(b, vector3) else vector3(b.x, b.y)
    return a.x * b.x + a.y * b.y + a.z * b.z


def cross(a: vector3, b: vector3) -> vector3:
    return vector3(
        a.y * b.z - a.z * b.y,
        a.z * b.x - a.x * b.z,
        a.x * b.y - a.y * b.x,
    )


@overload
def angle(a: vector3, b: vector3) -> float: ...
@overload
def angle(a: vector2, b: vector2) -> float: ...
@overload
def angle(a: vector2, b: vector3) -> float: ...
@overload
def angle(a: vector3, b: vector2) -> float: ...
def angle(a, b) -> float:
    a = a if isinstance(a, vector3) else vector3(a.x, a.y)
    if (am := a.magnitude) < 1e-3:
        return 0
    b = b if isinstance(b, vector3) else vector3(b.x, b.y)
    if (bm := b.magnitude) < 1e-3:
        return 0
    return acos(dot(a, b) / am / bm)


def sum(*a: vector3 | vector2):
    total = vector3()
    for e in a:
        total += e
    return total


def centroid(*a: vector2 | vector3):
    if not a:
        return vector2()
    sum = vector3()
    for e in a:
        sum += e
    return sum / len(a)


if __name__ == "__main__":
    a2 = vector2(1, -2)
    b2 = vector2(-4, 9)
    print(f"{a2=}")
    print(f"{b2=}")
    print(f"{a2==b2=}")
    print(f"{a2!=b2=}")
    print(f"{a2+b2=}")
    print(f"{a2-b2=}")
    print(f"{a2*b2=}")
    print(f"{a2/b2=}")
    print(f"{a2**b2=}")
    print(f"{a2//b2=}")
    print(f"{a2[0]=}, {a2[1]=}, {a2[2]=}")
    print(f"{b2[0]=}, {b2[1]=}, {b2[2]=}")
    print(f"{to_degrees(angle(a2, b2))=}")

    print("---")

    a3 = vector3(3, -3, 8)
    b3 = vector3(2, 1, -1)
    print(f"{a3=}")
    print(f"{b3=}")
    print(f"{a3==b3=}")
    print(f"{a3!=b3=}")
    print(f"{a3+b3=}")
    print(f"{a3-b3=}")
    print(f"{a3*b3=}")
    print(f"{a3/b3=}")
    print(f"{a3**b3=}")
    print(f"{a3//b3=}")
    print(f"{a3[0]=}, {a3[1]=}, {a3[2]=}")
    print(f"{b3[0]=}, {b3[1]=}, {b3[2]=}")
    print(f"{to_degrees(angle(a3, b3))=}")
