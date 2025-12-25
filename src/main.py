import asyncio
import random
from threading import Thread
from time import perf_counter
from omnim.rng import has_rust, randints, randfloats
from omnim.time import benchmark
from omnim.math import floor


def bench(m):
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            start = perf_counter()
            for _ in range(m):
                func(*args, **kwargs)
            end = perf_counter()
            elapsed = (end - start) * 1000
            print(
                f"{func.__name__.ljust(len('omnim_rng_randfloats'))}: {elapsed/m:.3f} ms"
            )

        return inner_wrapper

    return wrapper


M = 3


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


@benchmark
async def main():
    print(f"{has_rust()=}")

    N = 100_000_000
    print(f"{N=:#,}")
    print(f"{M=}")

    omnim_rng_randints(N)
    omnim_rng_randfloats(N)
    random_randint(N)
    random_uniform(N)

    """
    N=100,000,000
    M=3
    omnim_rng_randints  : 495.968 ms
    omnim_rng_randfloats: 1530.959 ms
    random_randint      : 18524.586 ms
    random_uniform      : 9165.171 ms
    """


if __name__ == "__main__":
    asyncio.run(main())
