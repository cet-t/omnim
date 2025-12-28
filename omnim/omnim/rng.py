from abc import ABCMeta
from enum import Enum
from typing import Final, TypeVar
from os import urandom
from numba import njit
from numpy import uint64, int64

try:
    from . import omnim_rng_rust  # type: ignore

    HAS_RUST = True
except ImportError:
    HAS_RUST = False

T = TypeVar("T")


class rng_mode(Enum):
    xorshift = 0
    pcg32 = 1


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


class bst_basic:
    def __init__(self, *, seed=0, mode=rng_mode.xorshift) -> None:
        if seed == 0:
            seed = random_device()
        self.__source = rng_basic(seed=seed, mode=mode)

    def search(self, *weights: float) -> int:
        if (length := len(weights)) < 1:
            return -1

        total_weights = 0.0
        accumulate_weights = list[float]()
        for weight in weights:
            total_weights += weight
            accumulate_weights.append(total_weights)

        r = self.__source.random_float(0, total_weights)
        bottom = 0
        top = length - 1
        while bottom < top:
            middle = int((bottom + top) / 2)
            if r > accumulate_weights[middle]:
                bottom = middle + 1
            else:
                if r >= (accumulate_weights[middle - 1] if middle > 0 else 0.0):
                    return middle
                top = middle
        return top


class bst_rust:
    def __init__(self, *, seed=0, mode=rng_mode.xorshift) -> None:
        if seed == 0:
            seed = random_device()
        self.__source = omnim_rng_rust.BinarySearch(seed)

    def search(self, *weights: float) -> int:
        return self.__source.search(list(weights))


if HAS_RUST:
    _rng = rng_rust(seed=0, mode=rng_mode.pcg32)
    _bst = bst_rust(seed=0)
else:
    _rng = rng_basic(seed=0, mode=rng_mode.pcg32)
    _bst = bst_basic(seed=0)

randint = _rng.random_int
randints = _rng.random_ints
randfloat = _rng.random_float
randfloats = _rng.random_floats
choice = _rng.random_choice
search = _bst.search


if __name__ == "__main__":
    print(f"{HAS_RUST=}")
