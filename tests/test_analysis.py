
import unittest

import pandas as pd

from analysis import (
    get_total_expenses,
    get_average_expense,
    get_category_summary,
    get_monthly_summary,
    get_top_category,
    generate_financial_insights,
)


class TestSmartSpendAnalysis(unittest.TestCase):

    def setUp(self):
        self.expenses = pd.DataFrame({
            "date": [
                "2026-10-01",
                "2026-10-02",
                "2026-10-03",
            ],
            "category": [
                "Food",
                "Transport",
                "Food",
            ],
            "description": [
                "Lunch",
                "Bus fare",
                "Dinner",
            ],
            "amount": [120.0, 40.0, 140.0],
        })

    def test_total_expenses(self):
        self.assertEqual(
            get_total_expenses(self.expenses),
            300.0,
        )

    def test_average_expense(self):
        self.assertAlmostEqual(
            get_average_expense(self.expenses),
            100.0,
        )

    def test_category_summary(self):
        summary = get_category_summary(self.expenses)

        food = summary[summary["category"] == "Food"].iloc[0]
        transport = summary[
            summary["category"] == "Transport"
        ].iloc[0]

        self.assertEqual(food["amount"], 260.0)
        self.assertAlmostEqual(food["percentage"], 86.6667, places=3)
        self.assertEqual(transport["amount"], 40.0)

    def test_monthly_summary(self):
        summary = get_monthly_summary(self.expenses)

        self.assertEqual(len(summary), 1)
        self.assertEqual(summary.iloc[0]["month"], "2026-10")
        self.assertEqual(summary.iloc[0]["amount"], 300.0)

    def test_top_category(self):
        category, amount = get_top_category(self.expenses)

        self.assertEqual(category, "Food")
        self.assertEqual(amount, 260.0)

    def test_empty_dataset(self):
        empty = pd.DataFrame(
            columns=["date", "category", "description", "amount"]
        )

        self.assertEqual(get_total_expenses(empty), 0.0)
        self.assertEqual(get_average_expense(empty), 0.0)

        category, amount = get_top_category(empty)

        self.assertIsNone(category)
        self.assertEqual(amount, 0.0)

    def test_financial_insights(self):
        insights = generate_financial_insights(
            self.expenses,
            budget=500.0,
        )

        self.assertTrue(len(insights) > 0)

        combined = " ".join(insights)

        self.assertIn("Food", combined)
        self.assertIn("300.00", combined)
        self.assertIn("60.0%", combined)


if __name__ == "__main__":
    unittest.main()
