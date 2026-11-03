import pytest
from atm_withdrawal import withdraw, pin_check, note_breakup

# Example test cases (kept from existing code):
def test_simple_withdrawal():
    assert withdraw(5000, 1000, "savings", True) == 4000

def test_correct_pin():
    assert pin_check(1234, 1234, 0) == "ok"


# Additional test cases to achieve 90-100% Code and Branch Coverage:

def test_withdraw_edge_cases_and_exceptions():
    # Unknown account exception
    with pytest.raises(ValueError, match="unknown account"):
        withdraw(5000, 1000, "invalid_account", True)

    # Invalid amount: amount <= 0
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, 0, "savings", True)
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, -100, "savings", True)

    # Invalid amount: not a multiple of 100
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, 150, "savings", True)

    # Limit exceeded for savings (> 25000) and current (> 50000)
    assert withdraw(40000, 30000, "savings", True) == "limit exceeded"
    assert withdraw(60000, 55000, "current", True) == "limit exceeded"

    # External bank fee handling (own_bank = False): amount <= 10000 (fee = 20)
    # 5000 - 1000 - 20 = 3980
    assert withdraw(5000, 1000, "savings", False) == 3980

    # External bank fee handling (own_bank = False): amount > 10000 (fee = 20 + 10 = 30)
    # 20000 - 12000 - 30 = 7970
    assert withdraw(20000, 12000, "current", False) == 7970

    # Insufficient funds (amount + fee > balance)
    assert withdraw(500, 1000, "savings", True) == "insufficient funds"


def test_pin_check_branches():
    # Attempts >= 3 blocks card immediately
    assert pin_check(1234, 1234, 3) == "card blocked"
    assert pin_check(1234, 1234, 4) == "card blocked"

    # Incorrect pin with attempts == 2 blocks card
    assert pin_check(1111, 1234, 2) == "card blocked"

    # Incorrect pin with attempts < 2 returns retry
    assert pin_check(1111, 1234, 0) == "retry"
    assert pin_check(1111, 1234, 1) == "retry"


def test_note_breakup_branches():
    # Invalid amount not multiple of 100 raises ValueError
    with pytest.raises(ValueError, match="invalid amount"):
        note_breakup(150)

    # Breakup with remaining >= 200 (hits True branch for notes_200)
    # 800 -> 1x500, remaining 300 (>=200 -> 1x200), remaining 100 (-> 1x100)
    assert note_breakup(800) == (1, 1, 1)

    # Breakup with remaining < 200 (hits else branch where notes_200 = 0)
    # 600 -> 1x500, remaining 100 (<200 -> 0x200), remaining 100 (-> 1x100)
    assert note_breakup(600) == (1, 0, 1)