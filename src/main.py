import asyncio
from dataclasses import dataclass
from datetime import date, datetime
import random
from omnim.step import frange, step
from omnim.rng import rng, has_rust, uniforms, randints
from omnim.time import stopwatch, benchmark


@dataclass
class User:
    name: str
    registered_at: date


@benchmark
async def main():
    print(f"{has_rust()=}")

    with stopwatch() as sw:
        N = 100_000_000

        start = datetime.now()
        _ = uniforms(N, 0, 10)
        elapsed = datetime.now() - start
        print(f"omnim.rng.uniforms  : {elapsed.total_seconds()*1000:.3f} ms")

        start = datetime.now()
        _ = randints(N, 0, 10)
        elapsed = datetime.now() - start
        print(f"omnim.rng.randints  : {elapsed.total_seconds()*1000:.3f} ms")

        start = datetime.now()
        for _ in step(N):
            _ = random.randint(0, 10)
        elapsed = datetime.now() - start
        print(f"random.randint      : {elapsed.total_seconds()*1000:.3f} ms")

        print(f"{sw.elapsed=}")


if __name__ == "__main__":
    asyncio.run(main())
