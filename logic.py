from random import randint
from datetime import datetime, timedelta
import requests

class Pokemon:
    pokemons = {}
    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):

        self.pokemon_trainer = pokemon_trainer   

        self.pokemon_number = randint(1,1000)
        self.img = self.get_img()
        self.name = self.get_name()
        self.hp = randint(200, 400)
        self.power = randint(30, 60)
        self.last_feed_time = datetime.now()

        Pokemon.pokemons[pokemon_trainer] = self

    # Метод для получения картинки покемона через API
    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return(data['sprites']['other']['official-artwork']['front_default'])
        else:
            return "https://static.wikia.nocookie.net/pokemon/images/0/0d/025Pikachu.png/revision/latest/scale-to-width-down/1000?cb=20181020165701&path-prefix=ru"
    
    # Метод для получения имени покемона через API
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['forms'][0]['name'])
        else:
            return "Pikachu"

    def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = randint(1, 5)
            if chance == 1:
                return "Покемон-волшебник применил щит в сражении"
        if enemy.hp > self.power: 
            enemy.hp -= self.power
            return f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}"
        else:
            enemy.hp = 0
            bonus_chance = randint(10, 50)
            self.hp += bonus_chance
            return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}! bonus earned @{bonus_chance}"

    # Метод класса для получения информации
    def info(self):
        return f"Имя твоего покеомона: {self.name}, \n HP: {self.hp}, \n Power {self.power}"

    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img

    def feed(self, feed_interval = 20, hp_increase = 10 ):
        current_time = datetime.now()  
        delta_time = timedelta(hours=feed_interval)  
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Здоровье покемона увеличено. Текущее здоровье: {self.hp}"
        else:
            return f"Следующее время кормления покемона: {self.last_feed_time + delta_time}"

class Wizard(Pokemon):
    def info(self):
        return "Your pokemon is a wizard \n\n" + super().info()

    def feed(self):
        return super().feed(hp_increase=20)

class Fighter(Pokemon):
    def info(self):
        return "Your pokemon is a fighter \n\n" + super().info()
    
    def attack(self, enemy):
        super_attack = randint(5, 15)
        self.power += super_attack
        result = super().attack(enemy)
        self.power -= super_attack
        return result + f"\nБоец применил супер-атаку силой:{super_attack} "

    def feed(self):
        return super().feed(feed_interval=10)
