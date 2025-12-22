import asyncio
from dataclasses import dataclass
from datetime import date, datetime
import random
from omnim.step import frange, step
from omnim.rng import rng, has_rust, uniforms, randints, rnexts, runiforms


@dataclass
class User:
    name: str
    registered_at: date


async def main():
    print(f"{has_rust()=}")

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
    _ = rnexts(N, 0, 10)
    elapsed = datetime.now() - start
    print(f"omnim.rng.nexts     : {elapsed.total_seconds()*1000:.3f} ms")

    start = datetime.now()
    _ = runiforms(N, 0, 10)
    elapsed = datetime.now() - start
    print(f"omnim.rng.runiform  : {elapsed.total_seconds()*1000:.3f} ms")

    xorshift = rng(seed=0, mode="xorshift")
    start = datetime.now()
    for _ in step(N):
        _ = xorshift.next_int(0, 10)
    elapsed = datetime.now() - start
    print(f"omnim.rng.xorshift  : {elapsed.total_seconds()*1000:.3f} ms")

    pcg = rng(seed=0, mode="pcg")
    start = datetime.now()
    for _ in step(N):
        _ = pcg.next_int(0, 10)
    elapsed = datetime.now() - start
    print(f"omnim.rng.pcg       : {elapsed.total_seconds()*1000:.3f} ms")

    py = random.Random(0)
    start = datetime.now()
    for _ in step(N):
        _ = py.randint(0, 10)
    elapsed = datetime.now() - start
    print(f"random.randint      : {elapsed.total_seconds()*1000:.3f} ms")


if __name__ == "__main__":
    asyncio.run(main())
