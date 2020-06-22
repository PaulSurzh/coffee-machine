import sys
import enum

class CoffeeCocktail:
    def __init__(self, water, milk, beans, cost):
        self.water = water
        self.milk = milk
        self.beans = beans
        self.cost = cost

class CoffeeMachine:
    cocktail_list = {
        "espresso": CoffeeCocktail(250, 0, 16, 4),
        "latte": CoffeeCocktail(350, 75, 20, 7),
        "cappuccino": CoffeeCocktail(200, 100, 12, 6)
    }
    
    class MachineState(enum.Enum):
        IDLE = 1
        BUYING = 2
        ADDING_WATER = 3
        ADDING_MILK = 4
        ADDING_BEANS = 5
        ADDING_CUPS = 6

    class MachineIsStopped(Exception):
        pass
    
    def __init__(self):
        self.water = 400
        self.milk = 540
        self.beans = 120
        self.cups = 9
        self.money = 550
        self.state = CoffeeMachine.MachineState.IDLE
        self.idle_prompt()

    def idle_prompt(self):
        print("Write action (buy, fill, take, remaining, exit):")
    
    def print_status(self):
        print("The coffee machine has:")
        print(f"{self.water} of water")
        print(f"{self.milk} of milk")
        print(f"{self.beans} of coffee beans")
        print(f"{self.cups} of disposable cups")
        print(f"${self.money} of money")
        print()

    def check_resources(self, cocktail):
        if self.water < cocktail.water:
            return "Sorry, not enough water!"
        elif self.milk < cocktail.milk:
            return "Sorry, not enough milk!"
        elif self.beans < cocktail.beans:
            return "Sorry, not enough coffee beans!"
        elif self.cups < 1:
            return "Sorry, not enough disposible cups!"

    def initiate_buying(self):
        print("What do you want to buy? 1 - espresso, 2 - latte,"
              " 3 - cappuccino, back - to main menu:")

        self.state = CoffeeMachine.MachineState.BUYING

    def buying(self, code):
        if code != "back":
            code = int(code)
            
            if code == 1:
                name = "espresso"
            elif code == 2:
                name = "latte"
            elif code == 3:
                name = "cappuccino"

            cocktail = CoffeeMachine.cocktail_list[name]

            msg = self.check_resources(cocktail)
            
            if msg is None:
                print("I have enough resources, making you a coffee!")
                self.water -= cocktail.water
                self.milk -= cocktail.milk
                self.beans -= cocktail.beans
                self.cups -= 1
                self.money += cocktail.cost
            else:
                print(msg)

        print()

        self.state = CoffeeMachine.MachineState.IDLE
        self.idle_prompt()

    def take(self):
        print(f"I gave you ${self.money}\n")
        self.money = 0

    def enter(self, txt):
        if self.state == CoffeeMachine.MachineState.IDLE:
            print()
            if txt == "buy":
               self.initiate_buying()
            elif txt == "fill":
                print("Write how many ml of water do you want to add:")
                self.state = CoffeeMachine.MachineState.ADDING_WATER
            elif txt == "take":
                self.take()
            elif txt == "remaining":
               self.print_status()
            elif txt == "exit":
               raise CoffeeMachine.MachineIsStopped()

            if self.state == CoffeeMachine.MachineState.IDLE:
                self.idle_prompt()
        elif self.state == CoffeeMachine.MachineState.BUYING:
            self.buying(txt)
        elif self.state == CoffeeMachine.MachineState.ADDING_WATER:
            self.water += int(txt)
            print("Write how many ml of milk do you want to add:")
            self.state = CoffeeMachine.MachineState.ADDING_MILK
        elif self.state == CoffeeMachine.MachineState.ADDING_MILK:
            self.milk += int(txt)
            print("Write how many grams of coffee beans do you want to add:")
            self.state = CoffeeMachine.MachineState.ADDING_BEANS
        elif self.state == CoffeeMachine.MachineState.ADDING_BEANS:
            self.beans += int(txt)
            print("Write how many disposable cups of coffee"
                  " do you want to add:")
            self.state = CoffeeMachine.MachineState.ADDING_CUPS
        elif self.state == CoffeeMachine.MachineState.ADDING_CUPS:
            self.cups += int(txt)
            print()
            self.state = CoffeeMachine.MachineState.IDLE
            self.idle_prompt()

def main():
    machine = CoffeeMachine()

    try:
        while True:
            text = input("> ")
            machine.enter(text)
    except CoffeeMachine.MachineIsStopped:
        pass

main()
