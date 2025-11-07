from objects.menu import new_menu as menu
from services.arcade import Arcade

executing = True

employee_data = [
    {   # cashier
        'name': 'Joe Biden',
        'id': 1,
    },
    {   # chef
        'name': 'Gordon Ramsay',
        'id': 2,
    }
]

arcade = Arcade()
arcade.new_employee('Cashier', employee_data[0]),
arcade.new_employee('Chef', employee_data[1])

employee_dialog_options = arcade.employees.copy()
employee_dialog_options.append('Back')

machine_data = [
    {   # platformer
        'name': 'Super Maria Sisters',
        'credit_cost': 5,
        'stages': 10,
        'loss_chance_per_stage': 0.2,
        'rewards_per_stage': 10,
        'mult_per_stage': 1.05,
    }, 
    {   # street fighter
        'name': 'Washington DC Simulator',
        'credit_cost': 2,
        'reward': 50,
        'hit_chance': 0.5,
        'get_hit_chance': 0.5,
        'client_damage': 10,
        'npc_damage': 10,
    }, 
    {   # shooter
        'name': 'Call of War',
        'credit_cost': 5,
        'stages': 10,
        'loss_chance_per_stage': 0.2,
        'rewards_per_stage': 10,
        'mult_per_stage': 1.05,
    },
]

arcade.new_machine('Platformer', machine_data[0]),
arcade.new_machine('Street Fighter', machine_data[1]),
arcade.new_machine('Shooter', machine_data[2]),

machine_dialog_options = arcade.machines.copy()
machine_dialog_options.append('Back')

starting_credits = int(menu('Welcome to the UIE arcade, how many credits would you like to start with?', [
    '10',
    '20',
    '50',
    '100',
    '250',
], 'green', 'raw'))

client = arcade.new_client({'name': 'david', 'starting_credits': starting_credits})

while executing:
    base_choice = menu('What would you like to do?',[
        'Visit the machines',
        'Talk to an employee',
        'View my stats',
        'View my food',
        'View my items',
        'Leave the arcade',
    ])
    if base_choice == 0:
        machine_idx = menu('Which game would you like to play?', machine_dialog_options)
        if machine_idx < len(arcade.machines):
            arcade.machines[machine_idx].play(client)
    elif base_choice == 1:
        employee_idx = menu('Which employee would you like to speak to?', employee_dialog_options)
        if employee_idx < len(arcade.employees):
            arcade.employees[employee_idx].interact(client)
    elif base_choice == 2:
        client.view_stats()
    elif base_choice == 3:
        client.view_food()
    elif base_choice == 4:
        client.view_inventory()
    elif base_choice == 5:
        executing = False
        print(f'Thanks for visiting! Your ending stats:\nCredits: {client.credit_balance}\nTickets: {client.ticket_balance}\nGames Played: {client.games_played}')