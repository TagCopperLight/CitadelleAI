def withdraw(bank: int, amount: int) -> tuple[int, int]:
    initial_value = bank
    bank = max(0, bank - amount)
    
    return bank, initial_value - bank

def deposit(bank: int, amount: int) -> int:
    return bank + amount