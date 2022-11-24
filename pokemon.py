import math
import random
from typechart import attack_type_chart


class PokemonApiResponse:
    def __init__(self, some_object):
        self.origin = "pokemon_api"
        self.result = some_object


class Overview:
    def __init__(self, name, url):
        self.name = name
        self.url = url


class BaseStats:
    def __init__(self, hp, attack, defence, sp_attack, sp_defence, speed):
        self.hp = hp
        self.attack = attack
        self.defence = defence
        self.sp_attack = sp_attack
        self.sp_defence = sp_defence
        self.speed = speed


class Move:
    def __init__(self, name, damage_type, is_physical: bool, base_power, accuracy, priority):
        self.name = name
        self.damage_type = damage_type
        self.is_physical = is_physical
        self.base_power = base_power
        self.accuracy = accuracy
        self.priority = priority


class Pokemon:
    def __init__(self, name, base_stats: BaseStats, level, type1, type2, image_url):
        self.name = name
        self.base_stats = base_stats
        self.level = level
        self.type1 = type1
        self.type2 = type2
        self.damage_taken = 0
        self.image_url = image_url

    def get_hp(self):
        return math.floor(0.01 * 2 * self.base_stats.hp * self.level) + self.level + 10

    def get_attack(self):
        return math.floor(0.01 * 2 * self.base_stats.attack * self.level) + 5

    def get_defence(self):
        return math.floor(0.01 * 2 * self.base_stats.defence * self.level) + 5

    def get_sp_attack(self):
        return math.floor(0.01 * 2 * self.base_stats.sp_attack * self.level) + 5

    def get_sp_defence(self):
        return math.floor(0.01 * 2 * self.base_stats.sp_defence * self.level) + 5

    def get_speed(self):
        return math.floor(0.01 * 2 * self.base_stats.speed * self.level) + 5

    def calculate_type_effectiveness(self, damage_type):
        if self.type2 is None:
            return attack_type_chart[damage_type][self.type1]
        else:
            return attack_type_chart[damage_type][self.type1] * attack_type_chart[damage_type][self.type2]

    def calculate_damage_taken(self, enemy_pokemon: "Pokemon", move: Move):
        attack_stat = 0
        defence_stat = 0
        stab = 1
        effectiveness = self.calculate_type_effectiveness(move.damage_type)
        random_value = 0.85 + random.random() * 0.15
        print(random_value)
        if move.damage_type == enemy_pokemon.type1 or move.damage_type == enemy_pokemon.type2:
            stab = 1.5

        if move.is_physical:
            attack_stat = enemy_pokemon.get_attack()
            defence_stat = self.get_defence()
        else:
            attack_stat = enemy_pokemon.get_sp_attack()
            defence_stat = self.get_sp_defence()

        damage = ((2 * enemy_pokemon.level / 5 + 2) * move.base_power * attack_stat / defence_stat / 50 + 2) \
                 * effectiveness * stab * random_value

        return math.ceil(damage)
