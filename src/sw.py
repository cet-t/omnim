from datetime import datetime, timedelta
from typing import Callable, Iterator, Optional
from omnim.delegate import action

_ON_CONTROL = Callable[[], None]
_ON_LAP = Callable[[timedelta], None]


class stopwatch:
    def __init__(
        self,
        *,
        auto_start=False,
        on_start: Optional[_ON_CONTROL] = None,
        on_stop: Optional[_ON_CONTROL] = None,
        on_lap: Optional[_ON_LAP] = None,
    ) -> None:
        self.__is_running = False

        self.__start = self.__now
        self.__stop = self.__now

        self.__laps: list[timedelta] = []
        self.__last_lap = self.__now

        self.__on_start: action[()] = action(on_start) if on_start else action()
        self.__on_stop: action[()] = action(on_stop) if on_stop else action()
        self.__on_lap: action[timedelta] = action(on_lap) if on_lap else action()

        if auto_start:
            self.start()

    @property
    def __now(self) -> datetime:
        return datetime.now()

    @property
    def on_start(self) -> action[()]:
        return self.__on_start

    @property
    def on_stop(self) -> action[()]:
        return self.__on_stop

    @property
    def on_lap(self) -> action[timedelta]:
        return self.__on_lap

    @property
    def is_running(self) -> bool:
        return self.__is_running

    @property
    def elapsed(self) -> timedelta:
        if self.__is_running:
            return self.__now - self.__start
        return self.__stop - self.__start

    @property
    def laps(self) -> Iterator[timedelta]:
        for lap in self.__laps:
            yield lap

    def start(self) -> None:
        if not self.__is_running:
            now = self.__now
            self.__start = now
            self.__last_lap = now
            self.__is_running = True

            self.__on_start.invoke()

    def restart(self) -> None:
        self.stop()
        self.start()

    def stop(self) -> None:
        if self.__is_running:
            self.__stop = self.__now
            self.__is_running = False

            self.__on_stop.invoke()

    def lap(self) -> None:
        if not self.__is_running:
            return

        now = self.__now
        lap_time = now - self.__last_lap
        self.__last_lap = now
        self.__laps.append(lap_time)

        self.__on_lap.invoke(lap_time)

    def __str__(self) -> str:
        return str(self.elapsed)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} is_running={self.__is_running} elapsed={self.__str__()}>"
