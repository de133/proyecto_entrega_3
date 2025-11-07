import uuid, random, time, os
from .menu import new_menu as menu
from .menu import new_text_display as text_display
from .people import Client

class Machine:
    def __init__(self, args):
        self.uid = uuid.uuid4()
        self.game = args['name']
        self.credit_cost = args['credit_cost']
        self.genre = None

    def on_finish(self, client: Client):
        client.increment_games_played()
        client.adjust_credits(-self.credit_cost)

    def __str__(self):
        return f'{self.game} - {self.genre} ({self.credit_cost} credits)'

class Platformer(Machine):
    def __init__(self, args):
        super().__init__(args)
        self.stages = args['stages']
        self.loss_chance_per_stage = args['loss_chance_per_stage']
        self.reward_per_stage = args['rewards_per_stage']
        self.mult_per_stage = args['mult_per_stage']
        self.genre = 'Platformer'

    def play_stage(self, client: Client):
        current_loss_chance = self.loss_chance_per_stage / client.get_current_bonus_strength('win_chance_bonus_multiplier')
        if random.random() < current_loss_chance:
            return False
        return True
    
    def play(self, client: Client):
        reward = 0
        stages_beat = 0
        if self.credit_cost > client.credit_balance:
            menu(f'This machine ({self.game}) has a credit cost of {self.credit_cost}, while you only have {client.credit_balance} credits.', ['Return to the arcade lobby'], 'green')
            return False
        
        stage_logs = []
        for i in range(self.stages):
            win = self.play_stage(client)
            if not win:
                break
            stage_logs.append(f'You beat stage {i+1}')
            temp = []
            for stage_log in stage_logs:
                temp.append(stage_log)
            temp.append('Press any key to continue...')
            text_display(temp)
            stages_beat += 1
            reward += (self.reward_per_stage * max(1, i*self.mult_per_stage))

        reward = round(reward)
        self.on_finish(client)
        client.adjust_tickets(reward)
        menu(f'You beat {stages_beat} stages before failing a jump on stage {stages_beat+1}. You have recieved {reward} tickets.', ['Return to the arcade lobby'], 'green')
        
class StreetFighter(Machine):
    def __init__(self, args):
        super().__init__(args)
        self.reward = args['reward']
        self.miss_chance = args['hit_chance']
        self.get_missed_chance = args['get_hit_chance']
        self.client_health = 100
        self.npc_health = 100
        self.client_damage = args['client_damage']
        self.npc_damage = args['npc_damage']
        self.genre = 'Street Fighter'

    def update_battle_menu(self, damage_logs: list, health_values: list):
        if len(damage_logs) > 9:
            for _ in range(len(damage_logs)-9):
                damage_logs.pop(0)
        temp = []
        temp.insert(0, f'YOU: {health_values[1]} HP | ENEMY: {health_values[0]} HP')
        for damage_log in damage_logs:
            temp.append(damage_log)
        temp.append('Press any key to continue...')
        text_display(temp)

    def try_hit(self, client: Client, health_values: list, damage_logs: list):
        current_hit_chance = self.miss_chance / client.get_current_bonus_strength('win_chance_bonus_multiplier')
        if random.random() < current_hit_chance:
            damage_logs.append('The opponent dodged your attack!')
        else:
            dmg = self.client_damage * client.get_current_bonus_strength('damage_multiplier_bonus')
            damage_logs.append(f'You hit the enemy for {dmg} damage')
            health_values[0] -= dmg
        
        self.update_battle_menu(damage_logs, health_values)
        return health_values

    def get_hit(self, client: Client, health_values: list, damage_logs: list):
        current_get_hit_chance = self.get_missed_chance / client.get_current_bonus_strength('dodge_chance_bonus')
        if random.random() < current_get_hit_chance:
            damage_logs.append('You dodged your opponents attack!')
        else:
            dmg = self.npc_damage * client.get_current_bonus_strength('damage_taken_multiplier_bonus')
            damage_logs.append(f'You got hit for {dmg} damage')
            health_values[1] -= dmg

        self.update_battle_menu(damage_logs, health_values)
        return health_values

    def play(self, client: Client):
        if self.credit_cost > client.credit_balance:
            menu(f'This machine ({self.game}) has a credit cost of {self.credit_cost}, while you only have {client.credit_balance} credits.', ['Return to the arcade lobby'], 'green')
            return False
        
        damage_logs = []
        health_values = [self.client_health, self.npc_health]
        while True:
            health_values = self.try_hit(client, health_values, damage_logs)
            if health_values[0] <= 0:
                break
            health_values = self.get_hit(client, health_values, damage_logs)
            if health_values[1] <= 0:
                break

            #print(health_values[0], health_values[1])
        
        self.on_finish(client)
        client.adjust_tickets(self.reward)
        if health_values[0] <= 0:
            menu(f'You won! You have recieved {self.reward} tickets.', ['Return to the arcade lobby'], 'green')
        elif health_values[1] <= 0:
            menu(f'You Lost.', ['Return to the arcade lobby'], 'green')
        
class Shooter(Machine):
    def __init__(self, args):
        super().__init__(args)
        self.stages = args['stages']
        self.loss_chance_per_stage = args['loss_chance_per_stage']
        self.reward_per_stage = args['rewards_per_stage']
        self.mult_per_stage = args['mult_per_stage']
        self.genre = 'Shooter'

    def play_stage(self, client: Client):
        current_loss_chance = self.loss_chance_per_stage / client.get_current_bonus_strength('win_chance_bonus_multiplier')
        if random.random() < current_loss_chance:
            return False
        return True
    
    def play(self, client: Client):
        reward = 0
        stages_beat = 0
        if self.credit_cost > client.credit_balance:
            menu(f'This machine ({self.game}) has a credit cost of {self.credit_cost}, while you only have {client.credit_balance} credits.', ['Return to the arcade lobby'], 'green')
            return False
        
        stage_logs = []
        for i in range(self.stages):
            win = self.play_stage(client)
            if not win:
                break
            stage_logs.append(f'You beat stage {i+1}')
            temp = []
            for stage_log in stage_logs:
                temp.append(stage_log)
            temp.append('Press any key to continue...')
            text_display(temp)
            stages_beat += 1
            reward += (self.reward_per_stage * max(1, i*self.mult_per_stage))

        reward = round(reward)
        self.on_finish(client)
        client.adjust_tickets(reward)
        menu(f'You beat {stages_beat} stages before a zombie mauled you to death on stage {stages_beat+1}. You have recieved {reward} tickets.', ['Return to the arcade lobby'], 'green')