class District:
    def __init__(self, id: int, name: str, cost: int, color: int) -> None:
        self.id = id
        self.name = name
        self.cost = cost
        self.color = color
    
    def __repr__(self) -> str:
        # return f"District(id={self.id}, name={self.name}, cost={self.cost}, color={self.color})"
        return f"District({self.id}, {self.name})"
        # return ""