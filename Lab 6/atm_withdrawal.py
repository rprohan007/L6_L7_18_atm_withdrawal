DAILY_LIMIT = {"savings": 25000, "current": 50000}


def withdraw(balance, amount, account_type, own_bank):
    if account_type not in DAILY_LIMIT:
        raise ValueError("unknown account")
    if amount <= 0 or amount % 100 != 0:
        raise ValueError("invalid amount")
    if amount > DAILY_LIMIT[account_type]:
        return "limit exceeded"
    fee = 0
    if not own_bank:
        fee = 20
        if amount > 10000:
            fee += 10
    if amount + fee > balance:
        return "insufficient funds"
    return balance - amount - fee


def pin_check(entered, actual, attempts):
    if attempts >= 3:
        return "card blocked"
    if entered == actual:
        return "ok"
    if attempts == 2:
        return "card blocked"
    return "retry"


def note_breakup(amount):
    if amount % 100 != 0:
        raise ValueError("invalid amount")
    notes_500 = amount // 500
    remaining = amount % 500
    if remaining >= 200:
        notes_200 = remaining // 200
        remaining = remaining % 200
    else:
        notes_200 = 0
    return notes_500, notes_200, remaining // 100