# What can be better than a cup of coffee during a break? A coffee that you
# don’t have to make yourself. It’s enough to press a couple of buttons on the machine
# and you get a cup of energy; but first, we should teach the machine how to do it.
# In this project, you will work on programming a coffee machine simulator. The machine
# works with typical products: coffee, milk, sugar, and plastic cups; if it runs out
# of something, it shows a notification. You can get three types of coffee: espresso,
# cappuccino, and latte.

class CoffeeMachine:
    def __init__(self):
        self.resources = dict().fromkeys(('water', 'milk', 'beans', 'cups', 'money'), 0)
        self.recipes = {'espresso': {'water': 250, 'beans': 16, 'money': 4},
                        'latte': {'water': 350, 'milk': 75, 'beans': 20, 'money': 7},
                        'cappuccino': {'water': 200, 'milk': 100, 'beans': 12, 'money': 6}}
        self.main_menu = {'buy': self.buy, 'fill': self.fill, 'take': self.take,
                          'remaining': self.display_state, 'exit': self.power_off}
        self.active = False

    def buy_menu(self):
        return dict(zip(list(map(lambda x: str(x + 1), range(len(self.recipes)))), self.recipes.keys()))

    def add_recipe(self, name, **kwargs):
        if kwargs:
            new_recipe = {key: value for key, value in kwargs.items() if key in self.resources.keys()}
            self.recipes[name] = new_recipe

    def display_state(self):
        print(f'\nThe coffee machine has:\n'
              f'{self.resources["water"]} of water\n'
              f'{self.resources["milk"]} of milk\n'
              f'{self.resources["beans"]} of coffee beans\n'
              f'{self.resources["cups"]} of disposable cups\n'
              f'{self.resources["money"]} of money')

    def valid_to_sell(self, recipe):
        used_resources = (self.resources[key] for key in recipe.keys())
        return bool(min(list(map(lambda x, y: x // y, used_resources, recipe.values()))))

    def buy(self):
        print('What do you want to buy?',
              ', '.join([f'{key} - {value}' for key, value in self.buy_menu().items()]),
              end=', back - to main menu:\n')
        selected_recipe = self.recipes.get(self.buy_menu().get(input()))
        if selected_recipe is not None:
            if self.valid_to_sell(selected_recipe):
                for key, value in selected_recipe.items():
                    if key != 'money':
                        value *= -1
                    self.resources[key] += value
                self.resources['cups'] -= 1
            else:
                print('I have enough resources, making you a coffee!')

    def fill(self, **kwargs):
        if kwargs:
            for key in self.resources.keys():
                self.resources[key] = kwargs.get(key, 0)
        else:
            self.resources['water'] += int(input('Write how many ml of water do you want to add:\n'))
            self.resources['milk'] += int(input('Write how many ml of milk do you want to add:\n'))
            self.resources['beans'] += int(input('Write how many grams of coffee beans do you want to add:\n'))
            self.resources['cups'] += int(input('Write how many disposable cups of coffee do you want to add:\n'))

    def take(self):
        print(f'I gave you ${self.resources["money"]}')
        self.resources["money"] = 0

    def power_on(self):
        self.active = True
        while self.active:
            user_input = input(f'\nWrite action ({", ".join(self.main_menu.keys())}):\n')
            if user_input in self.main_menu:
                self.main_menu[user_input]()

    def power_off(self):
        self.active = False


if __name__ == '__main__':
    coffee_machine = CoffeeMachine()
    coffee_machine.fill(money=550, water=400, milk=540, beans=120, cups=9)
    coffee_machine.power_on()
