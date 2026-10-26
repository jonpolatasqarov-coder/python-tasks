class Character:
    def __init__(self, name, health, strength, defense):
        self.name = name
        self.health = health
        self.max_health = health
        self.strength = strength
        self.defense = defense

    def is_alive(self):
        return self.health > 0



    def take_damage(self, damage):
        actual_damage = max(0, damage - self.defense)
        self.health = max(0, self.health - actual_damage)
        return actual_damage



    def attack(self, target):
        damage = self.strength - 5
        return target.take_damage(damage)