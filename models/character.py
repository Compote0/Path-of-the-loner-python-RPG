class Character:
    def __init__(self, name: str, hp: float, attack: float):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.xp = 0
        self.level = 1
        self.weapon = None
        self.armor = None

    def attack_enemy(self, enemy):
        if self.weapon:
            damage = self.attack + self.weapon.power
        else:
            damage = self.attack

        if enemy.armor:
            damage -= enemy.armor.defense
            damage = max(damage, 0)  

        enemy.hp -= damage
        self.gain_xp(10)  
        print(f"{self.name} attacks {enemy.name} for {damage} damage.")

    def equip_weapon(self, weapon):
        self.weapon = weapon
        print(f"{self.name} equipped {weapon.name}.")

    def equip_armor(self, armor):
        self.armor = armor
        print(f"{self.name} equipped {armor.name}.")

    def gain_xp(self, amount):
        self.xp += amount
        if self.xp >= 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp -= 100
        self.hp += 10
        self.attack += 2
        print(f"{self.name} leveled up to level {self.level}!")