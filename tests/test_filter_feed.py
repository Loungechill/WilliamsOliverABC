import tempfile
import unittest
from pathlib import Path

from filter_feed import custom_label_for_purchases, load_purchase_stats


class CustomLabelTests(unittest.TestCase):
    def test_thresholds(self):
        self.assertEqual(custom_label_for_purchases(0), "3")
        self.assertEqual(custom_label_for_purchases(1), "2")
        self.assertEqual(custom_label_for_purchases(2), "2")
        self.assertEqual(custom_label_for_purchases(3), "1")


class PurchaseCsvTests(unittest.TestCase):
    def write_csv(self, contents: str) -> Path:
        temp = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
        path = Path(temp.name)
        temp.close()
        path.write_text(contents, encoding="utf-8")
        self.addCleanup(path.unlink, missing_ok=True)
        return path

    def test_ignores_non_offer_and_merges_equal_duplicates(self):
        path = self.write_csv(
            "Offer ID,Название товара или каталога,Покупки\n"
            "00000000001,Тестовый товар с достаточно длинным названием,2\n"
            "00000000001,Тестовый товар с достаточно длинным названием,2\n"
            "#N/A,Страница каталога без товарного Offer ID,0\n"
        )

        purchases, stats = load_purchase_stats(path)

        self.assertEqual(purchases, {"00000000001": 2})
        self.assertEqual(stats["purchase_csv_duplicate_rows_merged"], 1)
        self.assertEqual(stats["purchase_csv_non_offer_rows_ignored"], 1)

    def test_rejects_conflicting_duplicate(self):
        path = self.write_csv(
            "Offer ID,Название товара или каталога,Покупки\n"
            "00000000001,Тестовый товар с достаточно длинным названием,1\n"
            "00000000001,Тестовый товар с достаточно длинным названием,2\n"
        )

        with self.assertRaisesRegex(RuntimeError, "Conflicting purchases"):
            load_purchase_stats(path)


if __name__ == "__main__":
    unittest.main()

