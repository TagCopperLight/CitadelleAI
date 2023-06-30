class Bank:
    def __init__(self) -> None:
        self.value = 30

    def withdraw(self, amount: int) -> int:
        initial_value = self.value
        self.value = max(0, self.value - amount)
        
        return initial_value - self.value
    
    def deposit(self, amount: int) -> int:
        self.value += amount
        
        return amount

    def __repr__(self) -> str:
        return f"Bank(value={self.value})"