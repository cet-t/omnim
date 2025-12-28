import builtins
from typing import Final, TypeVar

_builtins_min = builtins.min
_builtins_max = builtins.max

T_NUM = TypeVar("T_NUM", int, float)

pi: Final = 3.14159265358979323846
e: Final = 2.718281828459045235360287471352
eps: Final = 1 - (((4 / 3) - 1) + ((4 / 3) - 1) + ((4 / 3) - 1))
i: Final = 1j


golden_ratio: Final = (1 + 5**0.5) / 2

rad_to_deg: Final = 180 / pi
deg_to_rad: Final = pi / 180

nan: Final = float("nan")


def to_degrees(x: float) -> float:
    return x * rad_to_deg


def to_radians(x: float) -> float:
    return x * deg_to_rad


def factor(n: int) -> int:
    if n == 0:
        return 1
    return n * factor(n - 1)


def min(*xs: T_NUM) -> T_NUM:
    return _builtins_min(*xs)


def max(*xs: T_NUM) -> T_NUM:
    return _builtins_max(*xs)


def clamp(x: T_NUM, min_value: T_NUM, max_value: T_NUM) -> T_NUM:
    if x < min_value:
        return min_value
    elif x > max_value:
        return max_value
    return x


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def sign(x: T_NUM) -> int:
    if x == 0:
        return 0
    elif x > 0:
        return 1
    else:
        return -1


def abs(a: T_NUM) -> T_NUM:
    return -a if a < 0 else a


def floor(x: T_NUM, d=0) -> T_NUM:
    def _inner_floor(x: T_NUM) -> T_NUM:
        return type(x)(x - (x % 1))

    if d != 0:
        p = 10**d
        return type(x)(_inner_floor(x * p) / p)

    return _inner_floor(x)


def floori(x: T_NUM) -> int:
    return int(floor(x))


def round(x: T_NUM, d: int = 0) -> T_NUM:
    d = 10**d
    return type(x)(floor(x * d + 0.5) / d)


def sqrt(x: T_NUM, *, term=10):
    # x_n+1=1/2(x_n+A/x_n)
    x_ = float(x)
    result = x_

    for n in range(abs(term)):
        result = (result + x_ / result) / 2

    return result


def sin(x: float):
    return ((e ** (i * x) - e ** (-i * x)) / (2 * i)).real


def cos(x: float):
    return ((e ** (i * x) + e ** (-i * x)) / 2).real


def tan(x: float):
    return sin(x) / max(cos(x), eps)


def arcsin(y: float):
    if abs(y) > 1:
        return nan

    y_ = y
    numerator = 1
    denominator = 2

    for n in range(1, 10):
        power = 2 * n + 1
        term = (numerator / denominator) * (y**power / power)
        y_ += term

        numerator *= 2 * n + 1
        denominator *= 2 * n + 2

    return y_


def arccos(x: float):
    return pi / 2 - arcsin(x)


def arctan(x: float):
    return arcsin(x / sqrt(1 + x**2))


def arctan2(y: float, x: float):
    if x > 0:
        return arctan(y / x)
    elif x < 0 and y >= 0:
        return arctan(y / x) + pi
    elif x < 0 and y < 0:
        return arctan(y / x) - pi
    elif x == 0 and y > 0:
        return pi / 2
    elif x == 0 and y < 0:
        return -pi / 2
    else:
        return 0


def is_prime(n: int) -> bool:
    if n == 2:
        return True
    elif n < 2 or n % 2 == 0:
        return False

    for i in range(3, floori(sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def fibonacci(n: int):
    return int((golden_ratio**n - (-golden_ratio) ** -n) / sqrt(5))


if __name__ == "__main__":
    x = to_radians(90)
    print(f"{x=}")
    print(f"{sin(x)=:.2f}")
    print(f"{cos(x)=:.2f}", end="\n\n")

    theta = 0.5
    print(f"{theta=}")
    print(f"{arcsin(theta)=:.2f}")
    print(f"{arccos(theta)*rad_to_deg=:.2f}", end="\n\n")

    print(f"{sqrt(2)=}")
    print(f"{sqrt(256)=}")
