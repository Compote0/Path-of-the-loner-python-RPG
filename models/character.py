class Character:
    def __init__(self, name: str, hp: float, attack: float):
        self.name = name
        self.hp = hp
        self.attack = attack

    def attack_enemy(self, enemy):
        damage = self.attack
        enemy.hp -= damage
        print(f"{self.name} attacks {enemy.name} for {damage} damage.")
