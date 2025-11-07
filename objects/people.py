import time
from .menu import new_menu as menu
from .menu import new_text_display as text_display

class Person:
    def __init__(self, args):
        self.name = args['name']

class Client(Person):
    def __init__(self, args):
        super().__init__(args)
        self.credit_balance = args['starting_credits']
        self.ticket_balance = 0
        self.games_played = 0
        self.inventory = {}
        self.food = {}

    def alert_on_food_finished(self, item_name, cook_name):
        print(f"Your order of {item_name} has been completed by {cook_name}")
        return
    
    def add_item_to_inventory(self, item_name):
        if self.inventory.get(item_name):
            self.inventory[item_name] += 1
        else:
            self.inventory[item_name] = 1

    def add_food_to_inventory(self, food_name: str, food_stats: dict):
        if self.food.get(food_name):
            self.food[food_name]['quantity'] +=1
        else:
            d = {}
            food_stats_clone = food_stats.copy()
            d['quantity'] = 1
            d['stats'] = food_stats_clone
            self.food[food_name] = d

    def view_stats(self):
        text_display([f'Credits: {self.credit_balance}', f'Tickets: {self.ticket_balance}', f'Games Played: {self.games_played}', 'Press any key to return...'])

    def view_food(self):
        title = 'Food:\n'
        for food_name in self.food.keys():
            food_data = self.food[food_name]
            title += f'{food_data['quantity']}x {food_name}\n'
        menu(title, ['Back'])

    def view_inventory(self):
        title = 'Inventory:\n'
        for item_name in self.inventory.keys():
            item_quantity = self.inventory[item_name]
            title += f'{item_quantity}x {item_name}\n'
        menu(title, ['Back'])

    def get_current_bonus_strength(self, bonus_name: str):
        bonus_str = 1
        for food_name in self.food.keys():
            food = self.food[food_name]
            if bonus_name in food['stats']:
                bonus_str += food['stats'][bonus_name] * food['quantity']
        return bonus_str

    def increment_games_played(self):
        self.games_played += 1

    def adjust_tickets(self, amount):
        self.ticket_balance += amount

    def adjust_credits(self, amount):
        self.credit_balance += amount

class Employee(Person):
    def __init__(self, args):
        super().__init__(args)
        self.id = args['id']
        self.job = None

    def __str__(self):
        return f'{self.name} ({self.job})'

class Chef(Employee):
    def __init__(self, args: dict):
        super().__init__(args)
        self.items_for_sale = {
            'Hot Dog': {'cost': 10, 'stats':{'win_chance_bonus_multiplier': 1.1}},
            'Hamburger': {'cost': 25, 'stats':{'damage_multiplier_bonus': 1.1}},
            'Cheeseburger': {'cost': 25, 'stats':{'damage_taken_multiplier_bonus': 1.1}},
            'Fries': {'cost': 5, 'stats':{'dodge_chance_bonus': 1.1}},
            'Soda': {'cost': 5, 'stats':{'dodge_chance_bonus': 1.1}}
        }
        self.job = "Chef"
    
    def interact(self, customer: Client):
        items_tbl = []
        items_track = []
        for item_name in self.items_for_sale.keys():
            items_tbl.append(f'{item_name}: {self.items_for_sale[item_name]['cost']} Tickets')
            items_track.append(item_name)
        items_tbl.append('Cancel')
        result = menu("Here's what I have for sale", items_tbl, 'green')
        if len(items_track)-1 >= result:
            self.cook(items_track[result], customer)

    def cook(self, food_name: str, customer: Client):
        cost = self.items_for_sale[food_name]['cost']
        if customer.ticket_balance < cost:
            menu(f"You don't have enough tickets ({customer.ticket_balance}) to afford {food_name} ({cost})", ['Return to menu'], 'green')
            return False
        customer.adjust_tickets(-cost)
        customer.add_food_to_inventory(food_name, self.items_for_sale[food_name]['stats'])
    
class Cashier(Employee):
    def __init__(self, args: dict):
        super().__init__(args)
        self.items_for_sale = {
            'Small Plushie': {'cost': 50},
            'Medium Plushie': {'cost': 150},
            'Large Plushie': {'cost': 500},
            'X-Large Plushie': {'cost': 1000},
            'Small Candy Bag': {'cost': 25},
            'Large Candy Bag': {'cost': 100},
            'Arcade Shirt': {'cost': 100},
            'Arcade Shorts': {'cost': 100},
            'Arcade Jeans': {'cost': 200},
            'Arcade Sunglasses': {'cost': 50}
        }
        self.job = "Cashier"
    
    def interact(self, customer: Client):
        items_tbl = []
        items_track = []
        for item_name in self.items_for_sale.keys():
            items_tbl.append(f'{item_name}: {self.items_for_sale[item_name]['cost']} Tickets')
            items_track.append(item_name)
        items_tbl.append('Cancel')
        result = menu("Here's what I have for sale", items_tbl, 'green')
        if len(items_track)-1 >= result:
            self.purchase(items_track[result], customer)

    def purchase(self, item_name: str, customer: Client):
        cost = self.items_for_sale[item_name]['cost']
        if customer.ticket_balance < cost:
            menu(f"You don't have enough tickets ({customer.ticket_balance}) to afford {item_name} ({cost})", ['Return to menu'], 'green')
            return False
        customer.adjust_tickets(-cost)
        customer.add_item_to_inventory(item_name)
        
