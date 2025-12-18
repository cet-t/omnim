import asyncio
import unittest
from datetime import datetime
from omnim.task import wait_until, wait_any, with_timeout, interval


class TestOmnimAsync(unittest.IsolatedAsyncioTestCase):

    async def test_wait_until_performance(self):
        flag = False

        async def set_flag_after(sec):
            await asyncio.sleep(sec)
            nonlocal flag
            flag = True

        asyncio.create_task(set_flag_after(0.2))

        start = asyncio.get_running_loop().time()
        await wait_until(lambda: flag, timeout=1.0)
        end = asyncio.get_running_loop().time()

        print(f"\n[Async] wait_until 待機時間: {end - start:.4f}秒")
        self.assertTrue(flag)
        self.assertLess(end - start, 0.5)

    async def test_wait_any_with_coroutines(self):
        """wait_any が『生のコルーチン』を受け取って爆速で反応するか？"""

        async def fast_task():
            await asyncio.sleep(0.1)
            return "fast"

        async def slow_task():
            await asyncio.sleep(0.5)
            return "slow"

        start = asyncio.get_running_loop().time()
        done, pending = await wait_any(fast_task(), slow_task())
        end = asyncio.get_running_loop().time()

        print(f"[Async] wait_any 反応時間: {end - start:.4f}秒")
        self.assertEqual(len(done), 1)
        self.assertLess(end - start, 0.2)

    async def test_timeout_error(self):
        async def eternal_task():
            await asyncio.sleep(10)

        with self.assertRaises(asyncio.TimeoutError):
            await with_timeout(eternal_task(), 0.1)

    async def test_interval_change(self):
        interval(10)

        counter = 0

        def check():
            nonlocal counter
            counter += 1
            return counter >= 5

        start = asyncio.get_running_loop().time()
        await wait_until(check)
        end = asyncio.get_running_loop().time()

        print(f"[Async] interval(10ms) での5回チェック時間: {end - start:.4f}秒")
        self.assertLess(end - start, 0.1)


if __name__ == "__main__":
    unittest.main()
