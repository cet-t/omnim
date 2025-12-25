import asyncio
import random
from time import perf_counter
from omnim.rng import has_rust, rng_basic, rng_rust, randints, randfloats
from omnim.time import benchmark
from omnim.expressions import nameof


@benchmark
async def main():
    print(f"{has_rust()=}")

    N = 100_000_000

    start = perf_counter()
    _ = randints(N, 0, 10)
    end = perf_counter()
    print(f"{nameof(rng_rust)}.{nameof(randints)}: {end-start} s")

    start = perf_counter()
    _ = randfloats(N, 0, 10)
    end = perf_counter()
    print(f"{nameof(rng_rust)}.{nameof(randfloats)}: {end-start} s")

    basic_ = rng_basic(seed=0)
    start = perf_counter()
    _ = basic_.next_ints(N, 0, 10)
    end = perf_counter()
    print(f"{nameof(rng_basic)}.{nameof(basic_.next_ints)}: {end-start} s")

    start = perf_counter()
    _ = basic_.next_floats(N, 0, 10)
    end = perf_counter()
    print(f"{nameof(rng_basic)}.{nameof(basic_.next_floats)}: {end-start} s")

    start = perf_counter()
    _ = [random.randint(0, 10) for _ in range(N)]
    end = perf_counter()
    print(f"{nameof(random)}.{nameof(random.randint)}: {end-start} s")

    start = perf_counter()
    _ = [random.uniform(0, 10) for _ in range(N)]
    end = perf_counter()
    print(f"{nameof(random)}.{nameof(random.uniform)}: {end-start} s")

    """
    has_rust()=True
    rng_rust.random_ints_pcg: 0.4551276999991387 s
    rng_rust.random_floats_pcg: 1.1894683999707922 s
    rng_basic.next_ints: 15.55909450002946 s
    rng_basic.next_floats: 24.70881590002682 s
    random.randint: 18.25079590000678 s
    random.uniform: 8.384195500053465 s
    [BENCHMARK(async)] main: 68931.4083000645 ms
    """


if __name__ == "__main__":
    asyncio.run(main())
