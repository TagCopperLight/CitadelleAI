class Role:
    def __init__(self, order: int, name: str) -> None:
        self.order = order
        self.name = name

    def __repr__(self) -> str:
        # return f"Role(name={self.name}, order={self.order})"
        return ""