import unittest
from omnim.linq import linq, range


class linq_test(unittest.TestCase):

    def test_zip(self):
        names = ["Alice", "Bob", "Charlie"]
        scores = [100, 85, 90]

        result = linq(iter(names)).zip(scores, lambda n, s: f"{n}: {s}").first()

        self.assertEqual(result, "Alice: 100")
        print(f"[LINQ] zip: {result}")

    def test_join(self):
        users = [{"id": 1, "name": "omnim"}, {"id": 2, "name": "trrne"}]
        posts = [
            {"user_id": 1, "content": "Hello!"},
            {"user_id": 1, "content": "LINQ"},
            {"user_id": 2, "content": "0.2.0だー！"},
        ]

        result = linq(iter(users)).join(
            posts,
            outer_selector=lambda u: u["id"],
            inner_selector=lambda p: p["user_id"],
            result_selector=lambda u, p: f"{u['name']}: {p['content']}",
        )

        res_list = list(result)
        self.assertEqual(len(res_list), 3)
        self.assertIn("omnim: LINQ", res_list)
        print(f"[LINQ] join結果数: {len(res_list)}")

    def test_order_by(self):
        data = [5, 1, 8, 3, 9]

        ordered = list(linq(iter(data)).order_by(lambda x: x, descending=True))

        self.assertEqual(ordered, [9, 8, 5, 3, 1])
        print(f"[LINQ] order_by(desc): {ordered}")

    def test_complex_chain(self):
        result = (
            range(10, 10)
            .where(lambda x: x % 2 == 0)
            .order_by(lambda x: x, descending=True)
            .select(lambda x: f"No.{x}")
            .first()
        )

        self.assertEqual(result, "No.18")
        print(f"[LINQ] 複合チェーン結果: {result}")


if __name__ == "__main__":
    unittest.main()
