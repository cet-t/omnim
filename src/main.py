import asyncio
from dataclasses import dataclass
import random
from time import perf_counter
from typing import Any
import omnim.rng as rng
from omnim.rng import randints, randfloats, search
from omnim.time import benchmark
import omnim.mathr as mathr
from omnim.step import frange
import math


def bench(m):
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            start = perf_counter()
            for _ in range(m):
                func(*args, **kwargs)
            end = perf_counter()
            elapsed = (end - start) * 1000
            print(f"{func.__name__.ljust(len('omnim_xxx_')+15)}: {elapsed/m:.3f} ms")

        return inner_wrapper

    return wrapper


M = 10
N = 100_000_000


@bench(M)
def omnim_rng_randints(N):
    _ = randints(N, 0, 10)


@bench(M)
def omnim_rng_randfloats(N):
    _ = randfloats(N, 0, 10)


@bench(M)
def random_randint(N):
    _ = [random.randint(0, 10) for _ in range(N)]


@bench(M)
def random_uniform(N):
    _ = [random.uniform(0, 10) for _ in range(N)]


@dataclass
class Item:
    rate: str
    weight: float


@benchmark
def rng_test():
    print(f"{rng.HAS_RUST=}")

    omnim_rng_randints(N)
    omnim_rng_randfloats(N)
    # random_randint(N)
    # random_uniform(N)


@bench(M)
def omnim_mathr_sinx(N):
    for _ in range(N):
        _ = mathr.sin(0.1)


@bench(M)
def math_sinx(N):
    for _ in range(N):
        _ = math.sin(0.1)


@benchmark
def mathr_test():
    print(f"{mathr.HAS_RUST=}")

    omnim_mathr_sinx(N)
    math_sinx(N)


@benchmark
def main():
    items = [
        Item("R", 80),
        Item("SR", 20),
        Item("SSR", 0.1),
    ]
    weights = [item.weight for item in items]
    results = {
        0: 0,
        1: 0,
        2: 0,
    }

    for _ in range(N):
        results[search(*weights)] += 1

    print(
        "\n".join(
            [
                f"{item.rate}({100*(item.weight/sum(weights)):.2f}%): {100*(v/N):.3f}%"
                for (_, v), item in zip(results.items(), items)
            ]
        )
    )


if __name__ == "__main__":
    print(f"{N=:#,}")
    print(f"{M=}")

    # rng_test()
    mathr_test()
    # main()
