class Role:
    def __init__(self, name: str, order: int) -> None:
        self.name = name
        self.order = order

    def __repr__(self) -> str:
        # return f"Role(name={self.name}, order={self.order})"
        return ""