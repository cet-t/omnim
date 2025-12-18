import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Final
from uuid import uuid4
from omnim.reactive import ReactiveProperty
from omnim.delegate import action
from omnim.readonly import readonly


@dataclass
class Player:
    name: ReactiveProperty[str]
    uid: Final[int]
    last_logged_in: ReactiveProperty[datetime]
    item_count: ReactiveProperty[int]


async def main():
    players = [
        Player(
            ReactiveProperty(str(uuid4())),
            i,
            ReactiveProperty(datetime.now()),
            ReactiveProperty(0),
        )
        for i in range(1, 100, 2)
    ]

    for player in players:
        player.name.subscribe(lambda e: print(f"[{player.uid}] {e.pre} -> {e.new}"))
        player.last_logged_in.subscribe(
            lambda e: print(f"[{player.uid}] {e.pre} -> {e.new}")
        )
        player.item_count.subscribe(
            lambda e: print(f"[{player.uid}] {e.pre} -> {e.new}")
        )

    count = 0
    while count < 100:
        player = players[count % len(players)]
        player.item_count.value = count * 2

        count += 1
        await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(main())
