import time
from typing import Callable, Final, Literal, Optional, TypeVar
from os import urandom
from numba import njit
from numpy import uint64, int64

try:
    from . import omnim_rng_rust

    HAS_RUST = True
except ImportError:
    HAS_RUST = False

T = TypeVar("T")


def has_rust():
    return HAS_RUST


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
    def __init__(
        self,
        *,
        seed: Optional[int] = None,
        mode: Literal["xorshift", "pcg"] = "xorshift",
    ):
        import time

        if seed is None:
            seed = int(time.time() * 1000)

        match mode:
            case "xorshift":
                self.__generator = _xorshift64(seed)
            case "pcg":
                self.__generator = _pcg32(seed)
            case _:
                raise TypeError('mode must be "xorshift" or "pcg"')

    def _next(self) -> int:
        return self.__generator.next()

    def next_int(self, min_value: int, max_value: int) -> int:
        return self._next() % (max_value - min_value + 1) + min_value

    def next_float(self, min_value: float, max_value: float) -> float:
        return self._next() / self.__generator.max * (max_value - min_value) + min_value

    def next_ints(self, count: int, min_value: int, max_value: int) -> list[int]:
        range_size = max_value - min_value + 1
        return [(self._next() % range_size + min_value) for _ in range(count)]

    def next_floats(
        self, count: int, min_value: float, max_value: float
    ) -> list[float]:
        max_val = self.__generator.max
        diff = max_value - min_value
        return [(self._next() / max_val * diff + min_value) for _ in range(count)]

    def choice(self, seq: list[T]):
        if not seq:
            raise IndexError("Cannot choose from an empty sequence")
        return seq[self.next_int(0, len(seq) - 1)]


if HAS_RUST:

    class rng_rust:
        def __init__(self, seed=0):
            if seed == 0:
                seed = time.perf_counter_ns()

            self.__xorshift = omnim_rng_rust.Xorshift64(seed)
            self.__pcg = omnim_rng_rust.Pcg32(seed)

        def next_int_xorshift(self) -> int:
            return self.__xorshift.next_int()

        def next_float_xorshift(self) -> int:
            return self.__xorshift.next_float()

        def next_ints_xorshift(self, count: int) -> list[int]:
            return self.__xorshift.next_ints(count)

        def next_floats_xorshift(self, count: int) -> list[float]:
            return self.__xorshift.next_floats(count)

        def random_int_xorshift(self, min_value: int, max_value: int) -> int:
            return self.__xorshift.random_int(min_value, max_value)

        def random_float_xorshift(self, min_value: float, max_value: float) -> float:
            return self.__xorshift.random_float(min_value, max_value)

        def random_ints_xorshift(
            self, count: int, min_value: int, max_value: int
        ) -> list[int]:
            return self.__xorshift.random_ints(count, min_value, max_value)

        def random_floats_xorshift(
            self, count: int, min_value: float, max_value: float
        ) -> list[float]:
            return self.__xorshift.random_floats(count, min_value, max_value)

        def next_int_pcg(self) -> int:
            return self.__pcg.next_int()

        def next_float_pcg(self) -> int:
            return self.__pcg.next_float()

        def next_ints_pcg(self, count: int) -> list[int]:
            return self.__pcg.next_ints(count)

        def next_floats_pcg(self, count: int) -> list[float]:
            return self.__pcg.next_floats(count)

        def random_int_pcg(self, min_value: int, max_value: int) -> int:
            return self.__pcg.random_int(min_value, max_value)

        def random_float_pcg(self, min_value: float, max_value: float) -> float:
            return self.__pcg.random_float(min_value, max_value)

        def random_ints_pcg(
            self, count: int, min_value: int, max_value: int
        ) -> list[int]:
            return self.__pcg.random_ints(count, min_value, max_value)

        def random_floats_pcg(
            self, count: int, min_value: float, max_value: float
        ) -> list[float]:
            return self.__pcg.random_floats(count, min_value, max_value)

        def random_choice(self, seq: list[T]):
            if not seq:
                raise IndexError("Cannot choose from an empty sequence")
            return seq[self.random_int_pcg(0, len(seq) - 1)]


if has_rust():
    _rg = rng_rust()
    randint = _rg.random_int_pcg
    randints = _rg.random_ints_pcg
    randfloat = _rg.random_float_pcg
    randfloats = _rg.random_floats_pcg
    choice = _rg.random_choice


if __name__ == "__main__":
    print(f"{has_rust()=}")
