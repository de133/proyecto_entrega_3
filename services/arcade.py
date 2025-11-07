from objects import people
from objects import machines as machine

class Arcade():
    def __init__(self):
        self.clients = []
        self.machines = []
        self.employees = []

    def new_employee(self, employee_type: str, employee_data: dict):
        emp = None
        if employee_type == 'Cashier':
            emp = people.Cashier(employee_data)
        elif employee_type == 'Chef':
            emp = people.Chef(employee_data)
        else:
            ValueError(f'Employee of type {employee_type} not recognized')
        self.employees.append(emp)
        return machine

    def new_machine(self, machine_type: str, machine_data: dict):
        mch = None
        if machine_type == 'Platformer':
            mch = machine.Platformer(machine_data)
        elif machine_type == 'Street Fighter':
            mch = machine.StreetFighter(machine_data)
        elif machine_type == 'Shooter':
            mch = machine.Shooter(machine_data)
        else:
            ValueError(f'Machine of type {machine_type} not recognized')
        self.machines.append(mch)
        return machine

    def new_client(self, data):
        cl = people.Client(data)
        self.clients.append(cl)
        return cl