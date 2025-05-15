class Armor:
    def __init__(self, name: str, defense: float):
        self.name = name
        self.defense = defense

    def reduce_damage(self, damage: float) -> float:
        return max(damage - self.defense, 0)

    def to_dict(self):
        return {"name": self.name, "defense": self.defense, "type": "armor"}

    @staticmethod
    def from_dict(data):
        return Armor(name=data["name"], defense=data["defense"])
