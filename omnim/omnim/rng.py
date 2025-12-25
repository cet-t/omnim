from enum import Enum
from typing import Final, Optional, TypeVar
from os import urandom
from numba import njit
from numpy import uint64, int64

try:
    from . import omnim_rng_rust

    HAS_RUST = True
except ImportError:
    HAS_RUST = False

T = TypeVar("T")


class rng_mode(Enum):
    xorshift = 0
    pcg32 = 1


def has_rust() -> bool:
    return HAS_RUST


def random_device() -> int:
    return int.from_bytes(urandom(8), "big")


@njit
def _xorshift64_next(state: int) -> int:
    x = state
    x ^= (x << 13) & 0xFFFFFFFFFFFFFFFF
    x ^= (x >> 7) & 0xFFFFFFFFFFFFFFFF
    x ^= (x << 17) & 0xFFFFFFFFFFFFFFFF
    return x


@njit
def _pcg32_next(state: int, inc: int):
    oldstate = uint64(state)
    new_state = oldstate * uint64(6364136223846793005) + uint64(inc)

    shifted = uint64(((oldstate >> 18) ^ oldstate) >> 27)
    rot = oldstate >> 59
    output = (shifted >> rot) | (shifted << (uint64(-rot) & uint64(31)))

    return int64(new_state), int64(output & uint64(0xFFFFFFFF))


class _xorshift64:
    def __init__(self, seed: int):
        self.state: int = seed & 0xFFFFFFFFFFFFFFFF or 0xDEADBEEF
        self.max: Final = 0xFFFFFFFFFFFFFFFF

    def next(self) -> int:
        self.state = _xorshift64_next(self.state)
        return self.state


class _pcg32:
    def __init__(self, seed: int):
        self.state = (seed + 0xDA3E39CB94B95BDB) & 0xFFFFFFFFFFFFFFFF
        self.inc = (seed | 1) & 0xFFFFFFFFFFFFFFFF
        self.max: Final = 0xFFFFFFFF

    def next(self) -> int:
        self.state, result = _pcg32_next(int(self.state), self.inc)
        return int(result)


class rng_basic:
    def __init__(self, *, seed=0, mode=rng_mode.xorshift):
        if seed == 0:
            seed = random_device()

        match mode:
            case rng_mode.xorshift:
                self.__generator = _xorshift64(seed)
            case rng_mode.pcg32:
                self.__generator = _pcg32(seed)
            case _:
                raise TypeError('mode must be "xorshift" or "pcg"')

    def _next(self) -> int:
        return self.__generator.next()

    def random_int(self, min_value: int, max_value: int) -> int:
        return self._next() % (max_value - min_value + 1) + min_value

    def random_float(self, min_value: float, max_value: float) -> float:
        return self._next() / self.__generator.max * (max_value - min_value) + min_value

    def random_ints(self, count: int, min_value: int, max_value: int) -> list[int]:
        range_size = max_value - min_value + 1
        return [(self._next() % range_size + min_value) for _ in range(count)]

    def random_floats(
        self, count: int, min_value: float, max_value: float
    ) -> list[float]:
        max_val = self.__generator.max
        diff = max_value - min_value
        return [(self._next() / max_val * diff + min_value) for _ in range(count)]

    def random_choice(self, seq: list[T]):
        if not seq:
            raise IndexError("Cannot choose from an empty sequence")
        return seq[self.random_int(0, len(seq) - 1)]


class rng_rust:
    def __init__(self, seed=0, mode=rng_mode.xorshift):
        if seed == 0:
            seed = random_device()

        match mode:
            case rng_mode.xorshift:
                self.__generator = omnim_rng_rust.Xorshift64(seed)
            case rng_mode.pcg32:
                self.__generator = omnim_rng_rust.Pcg32(seed)

    def next_int(self) -> int:
        return self.__generator.next_int()

    def next_float(self) -> int:
        return self.__generator.next_float()

    def next_ints(self, count: int) -> list[int]:
        return self.__generator.next_ints(count)

    def next_floats(self, count: int) -> list[float]:
        return self.__generator.next_floats(count)

    def random_int(self, min_value: int, max_value: int) -> int:
        return self.__generator.random_int(min_value, max_value)

    def random_float(self, min_value: float, max_value: float) -> float:
        return self.__generator.random_float(min_value, max_value)

    def random_ints(self, count: int, min_value: int, max_value: int) -> list[int]:
        return self.__generator.random_ints(count, min_value, max_value)

    def random_floats(
        self, count: int, min_value: float, max_value: float
    ) -> list[float]:
        return self.__generator.random_floats(count, min_value, max_value)

    def random_choice(self, seq: list[T]):
        if not seq:
            raise ValueError("Cannot choose from an empty sequence")
        return seq[self.random_int(0, len(seq) - 1)]


if has_rust():
    _rg = rng_rust(seed=0, mode=rng_mode.pcg32)
else:
    _rg = rng_basic(seed=0, mode=rng_mode.pcg32)

randint = _rg.random_int
randints = _rg.random_ints
randfloat = _rg.random_float
randfloats = _rg.random_floats
choice = _rg.random_choice


if __name__ == "__main__":
    print(f"{has_rust()=}")
