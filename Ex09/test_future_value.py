"""
Pytest test suite for future_value.py

Tests cover:
- Normal cases for calculate_future_value()
- Edge cases (0 interest, 0 years, 0 payment)
- Floating-point precision behavior
- Large year values for loop stability
- Negative inputs (no exception, mathematically correct output)
- main() loop behavior via mocked input() and print()
"""

import pytest
from unittest.mock import patch, call
from future_value import calculate_future_value, main


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _fv(payment, years, rate):
    """Pure-Python reference implementation for expected values."""
    months = years * 12
    monthly_rate = rate / 12 / 100
    fv = 0.0
    for _ in range(months):
        fv = (fv + payment) * (1 + monthly_rate)
    return fv


# ---------------------------------------------------------------------------
# 1. Normal cases
# ---------------------------------------------------------------------------

class TestCalculateFutureValueNormal:

    def test_standard_investment(self):
        """$100/month for 10 years at 6% annual interest."""
        result = calculate_future_value(100, 10, 6)
        expected = _fv(100, 10, 6)
        assert result == pytest.approx(expected, rel=1e-9)

    def test_higher_payment(self):
        """$500/month for 5 years at 4% annual interest."""
        result = calculate_future_value(500, 5, 4)
        expected = _fv(500, 5, 4)
        assert result == pytest.approx(expected, rel=1e-9)

    def test_one_year(self):
        """Single year of $200/month at 5% annual interest."""
        result = calculate_future_value(200, 1, 5)
        expected = _fv(200, 1, 5)
        assert result == pytest.approx(expected, rel=1e-9)

    def test_high_interest_rate(self):
        """$50/month for 3 years at 12% annual interest."""
        result = calculate_future_value(50, 3, 12)
        expected = _fv(50, 3, 12)
        assert result == pytest.approx(expected, rel=1e-9)

    def test_fractional_payment(self):
        """Non-integer monthly payment of $99.99."""
        result = calculate_future_value(99.99, 2, 5)
        expected = _fv(99.99, 2, 5)
        assert result == pytest.approx(expected, rel=1e-9)

    def test_fractional_interest_rate(self):
        """Fractional annual interest rate of 3.75%."""
        result = calculate_future_value(150, 7, 3.75)
        expected = _fv(150, 7, 3.75)
        assert result == pytest.approx(expected, rel=1e-9)


# ---------------------------------------------------------------------------
# 2. Edge cases
# ---------------------------------------------------------------------------

class TestCalculateFutureValueEdgeCases:

    def test_zero_interest_rate(self):
        """0% interest: future value equals total payments made."""
        result = calculate_future_value(100, 5, 0)
        # With 0% interest each month: fv grows only by payment
        expected = _fv(100, 5, 0)
        assert result == pytest.approx(expected, rel=1e-9)
        # Sanity: should equal 100 * 60
        assert result == pytest.approx(100 * 60, rel=1e-9)

    def test_zero_years(self):
        """0 years means 0 months — future value should be 0."""
        result = calculate_future_value(100, 0, 6)
        assert result == 0

    def test_zero_payment(self):
        """$0/month payment — future value stays 0 regardless of rate."""
        result = calculate_future_value(0, 10, 8)
        assert result == pytest.approx(0.0, abs=1e-12)

    def test_zero_all(self):
        """All inputs zero — result must be 0."""
        result = calculate_future_value(0, 0, 0)
        assert result == 0


# ---------------------------------------------------------------------------
# 3. Floating-point precision behavior
# ---------------------------------------------------------------------------

class TestFloatingPointPrecision:

    def test_result_is_float(self):
        """Return value should be a float."""
        result = calculate_future_value(100, 1, 5)
        assert isinstance(result, float)

    def test_precision_small_rate(self):
        """Very small interest rate (0.001%) should not cause precision loss."""
        result = calculate_future_value(100, 10, 0.001)
        expected = _fv(100, 10, 0.001)
        assert result == pytest.approx(expected, rel=1e-9)

    def test_precision_large_payment(self):
        """Large payment amount ($1,000,000) should remain accurate."""
        result = calculate_future_value(1_000_000, 5, 7)
        expected = _fv(1_000_000, 5, 7)
        assert result == pytest.approx(expected, rel=1e-9)

    def test_deterministic(self):
        """Same inputs always produce the same output."""
        r1 = calculate_future_value(250, 8, 4.5)
        r2 = calculate_future_value(250, 8, 4.5)
        assert r1 == r2


# ---------------------------------------------------------------------------
# 4. Large year values — loop stability
# ---------------------------------------------------------------------------

class TestLargeYearValues:

    def test_50_years(self):
        """50-year investment should complete without error."""
        result = calculate_future_value(100, 50, 7)
        expected = _fv(100, 50, 7)
        assert result == pytest.approx(expected, rel=1e-9)

    def test_100_years(self):
        """100-year investment (1200 months) should remain stable."""
        result = calculate_future_value(10, 100, 5)
        expected = _fv(10, 100, 5)
        assert result == pytest.approx(expected, rel=1e-9)

    def test_200_years(self):
        """Extreme 200-year horizon — verifies no overflow or instability."""
        result = calculate_future_value(1, 200, 3)
        expected = _fv(1, 200, 3)
        assert result == pytest.approx(expected, rel=1e-6)


# ---------------------------------------------------------------------------
# 5. Negative inputs — no exception, mathematically correct output
# ---------------------------------------------------------------------------

class TestNegativeInputs:

    def test_negative_payment(self):
        """Negative monthly payment (withdrawal) should not raise."""
        result = calculate_future_value(-100, 5, 6)
        expected = _fv(-100, 5, 6)
        assert result == pytest.approx(expected, rel=1e-9)

    def test_negative_interest_rate(self):
        """Negative interest rate (deflation scenario) should not raise."""
        result = calculate_future_value(100, 5, -2)
        expected = _fv(100, 5, -2)
        assert result == pytest.approx(expected, rel=1e-9)

    def test_negative_years_gives_zero_iterations(self):
        """Negative years produces a negative months value; loop does not run."""
        result = calculate_future_value(100, -5, 6)
        # range of a negative number is empty — future_value stays 0
        assert result == 0


# ---------------------------------------------------------------------------
# 6. main() loop behavior via mocked input() and print()
# ---------------------------------------------------------------------------

class TestMainFunction:

    def test_main_single_valid_run_then_quit(self):
        """
        Simulate one valid calculation followed by 'n' to quit.
        Verifies that the future value is printed and 'Bye!' is shown.
        """
        inputs = iter(["100", "10", "6", "n"])
        expected_fv = calculate_future_value(100, 10, 6)

        with patch("builtins.input", side_effect=inputs), \
             patch("builtins.print") as mock_print:
            main()

        printed_text = " ".join(
            str(arg)
            for call_args in mock_print.call_args_list
            for arg in call_args[0]
        )
        assert f"{expected_fv:.2f}" in printed_text
        assert "Bye!" in printed_text

    def test_main_continue_then_quit(self):
        """
        Simulate two valid calculations: first enter 'y' to continue,
        then 'n' to quit. Verifies both future values are printed.
        """
        inputs = iter(["200", "5", "4", "y", "300", "3", "7", "n"])
        fv1 = calculate_future_value(200, 5, 4)
        fv2 = calculate_future_value(300, 3, 7)

        with patch("builtins.input", side_effect=inputs), \
             patch("builtins.print") as mock_print:
            main()

        printed_text = " ".join(
            str(arg)
            for call_args in mock_print.call_args_list
            for arg in call_args[0]
        )
        assert f"{fv1:.2f}" in printed_text
        assert f"{fv2:.2f}" in printed_text
        assert "Bye!" in printed_text

    def test_main_invalid_input_triggers_error_message(self):
        """
        Non-numeric input should trigger the ValueError message,
        then the loop retries and exits cleanly on valid input + 'n'.
        """
        inputs = iter(["abc", "100", "10", "6", "n"])

        with patch("builtins.input", side_effect=inputs), \
             patch("builtins.print") as mock_print:
            main()

        printed_text = " ".join(
            str(arg)
            for call_args in mock_print.call_args_list
            for arg in call_args[0]
        )
        assert "Invalid input" in printed_text

    def test_main_invalid_years_triggers_error_message(self):
        """
        Non-integer years input should trigger the ValueError message.
        """
        inputs = iter(["100", "ten", "100", "10", "6", "n"])

        with patch("builtins.input", side_effect=inputs), \
             patch("builtins.print") as mock_print:
            main()

        printed_text = " ".join(
            str(arg)
            for call_args in mock_print.call_args_list
            for arg in call_args[0]
        )
        assert "Invalid input" in printed_text

    def test_main_exits_on_n(self):
        """
        Entering 'n' after the first calculation must print 'Bye!' exactly once.
        """
        inputs = iter(["50", "2", "3", "n"])

        with patch("builtins.input", side_effect=inputs), \
             patch("builtins.print") as mock_print:
            main()

        bye_calls = [
            c for c in mock_print.call_args_list
            if c[0] and "Bye!" in str(c[0][0])
        ]
        assert len(bye_calls) == 1

    def test_main_does_not_exit_on_y(self):
        """
        Entering 'y' should NOT trigger 'Bye!' — loop must continue.
        Only the final 'n' should cause exit.
        """
        inputs = iter(["100", "1", "5", "y", "100", "1", "5", "n"])

        with patch("builtins.input", side_effect=inputs), \
             patch("builtins.print") as mock_print:
            main()

        # Count how many times 'Bye!' was printed
        bye_calls = [
            c for c in mock_print.call_args_list
            if c[0] and "Bye!" in str(c[0][0])
        ]
        assert len(bye_calls) == 1

    def test_main_prints_header(self):
        """main() should print the 'Future Value Calculator' header on start."""
        inputs = iter(["100", "1", "5", "n"])

        with patch("builtins.input", side_effect=inputs), \
             patch("builtins.print") as mock_print:
            main()

        printed_text = " ".join(
            str(arg)
            for call_args in mock_print.call_args_list
            for arg in call_args[0]
        )
        assert "Future Value Calculator" in printed_text
