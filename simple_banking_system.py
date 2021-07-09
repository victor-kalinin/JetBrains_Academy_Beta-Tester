# Everything goes digital these days, and so does money. Today, most people
# have credit cards, which save us time, energy and nerves. From not having to carry
# a wallet full of cash to consumer protection, cards make our lives easier in many
# ways. In this project, you will develop a simple banking system with database.

import sqlite3
from random import randint


class BankingSystem:
    MII = '4'
    IIN = '00000'
    ACCOUNT_LENGTH = 9
    PIN_LENGTH = 4
    db_file = 'card.s3db'

    def __init__(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS card (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        number TEXT,
                                        pin TEXT,
                                        balance INTEGER DEFAULT 0);''')
        self.conn.commit()
        self.menu = {1: {1: ("Create an account", self.create_account),
                         2: ("Log into account", self.login_account),
                         0: ("Exit", self.exit)},
                     2: {1: ("Balance", self.show_balance),
                         2: ("Add income", self.add_income),
                         3: ("Do transfer", self.do_transfer),
                         4: ("Close account", self.close_account),
                         5: ("Log out", self.logout_account),
                         0: ("Exit", self.exit)}}
        self.initial_state()

    def initial_state(self):
        self.card_number = None
        self.card_pin = None
        self.balance = 0
        self.menu_level = 1

    @staticmethod
    def generate_number(len_number):
        number = []
        for _ in range(len_number):
            number.append(str(randint(0, 9)))
        return "".join(number)

    @staticmethod
    def luhn_digit(card_number):
        temp_number = 0
        if len(card_number) == 15:
            for counter, value in enumerate(card_number):
                value = int(value)
                if counter % 2 == 0:
                    value *= 2
                temp_number += value - 9 if value > 9 else value
            temp_number %= 10
            return card_number + str(10 - temp_number if temp_number > 0 else 0)

    def print_menu(self):
        for key, value in self.menu[self.menu_level].items():
            print(f'{key}) {value[0]}')
        self.process_input(int(input('>')))

    def process_input(self, user_input):
        self.menu[self.menu_level][user_input][1]()

    def create_account(self):
        card_number = self.luhn_digit(self.MII + self.IIN + self.generate_number(self.ACCOUNT_LENGTH))
        card_pin = self.generate_number(self.PIN_LENGTH)
        self.cur.execute(f"SELECT number FROM card WHERE number = ?;", (card_number,))
        if self.cur.fetchone() is None:
            self.cur.execute("INSERT INTO card(number, pin) VALUES(?, ?);", (card_number, card_pin))
            self.conn.commit()
            print(f'\nYour card has been created\n'
                  f'Your card number:\n{card_number}\n'
                  f'Your card PIN:\n{card_pin}\n')

    def has_login(self):
        return self.card_number is not None

    def login_account(self):
        print('\nEnter your card number:')
        user_card = input('>')
        print('Enter your PIN:')
        user_pin = input('>')
        result_sql = self.cur.execute("""SELECT number, pin, balance FROM card
                                                     WHERE number = ?;""", (user_card,)).fetchone()
        if result_sql is not None and result_sql[1] == user_pin:
            self.card_number = user_card
            self.balance = result_sql[2]
            self.menu_level = 2
            print("\nYou have successfully logged in!\n")
        else:
            print("\nWrong card number or PIN!\n")
            self.initial_state()

    def show_balance(self):
        print(f"\nBalance: {self.balance}\n")

    def add_income(self):
        print("\nEnter income:")
        self.balance += int(input(">"))
        self.cur.execute("UPDATE card SET balance = ? WHERE number = ?;",(self.balance, self.card_number))
        self.conn.commit()
        print("\nIncome was added!\n")

    def do_transfer(self):
        print('\nTransfer\nEnter card number:')
        transfer_card = input('>')
        # Verify card number
        if transfer_card != self.luhn_digit(transfer_card[:-1]):
            print('Probably you made a mistake in the card number.Please try again!')
            return
        # Card availability check
        result_sql = self.conn.execute("SELECT * FROM card WHERE number = ?;", (transfer_card,)).fetchone()
        if result_sql is None:
            print("Such a card does not exist.")
            return
        # Money availability check
        print("Enter how much money you want to transfer:")
        transfer_money = int(input('>'))
        if self.balance - transfer_money < 0:
            print("Not enough money!")
            return
        else:
            transfer_balance = self.cur.execute("""SELECT balance FROM card
                                                    WHERE number = ?;""", (transfer_card,)).fetchone()[0]
            self.balance -= transfer_money
            self.cur.execute("""UPDATE card SET balance = ?
                                 WHERE number = ?;""", (self.balance, self.card_number))
            self.cur.execute("""UPDATE card SET balance = ?
                                 WHERE number = ?;""", (transfer_balance + transfer_money, transfer_card))
            self.conn.commit()
            print('Success!')

    def close_account(self):
        self.cur.execute("DELETE FROM card WHERE number = ?;", (self.card_number,))
        self.conn.commit()
        print("\nThe account has been closed!\n")
        self.initial_state()

    def logout_account(self):
        print("\nYou have successfully logged out!\n")
        self.initial_state()

    def exit(self):
        print('\nBye!')
        self.menu_level = 0


if __name__ == '__main__':
    my_bank = BankingSystem()

    while my_bank.menu_level != 0:
        my_bank.print_menu()
