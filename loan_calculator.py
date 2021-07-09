# Personal finances are an important part of life. Sometimes you need some
# extra money and decide to take a loan, or you want to buy a house using a mortgage.
# To make an informed decision, you need to be able to calculate different financial
# parameters. Let’s make a program that can help us with that!

import math
import argparse


class _ArgumentParser(argparse.ArgumentParser):
    def _print_message(self, message, file=None):
        print('Incorrect parameters')

    def print_usage(self, file=None):
        pass


class LoanCalculator:
    def __init__(self, **kwargs):
        self.type = None
        self.payment = None
        self.principal = None
        self.periods = None
        self.interest = None
        self.full_loan = 0
        for item in kwargs:
            setattr(self, item, kwargs[item])

    def get_none_attr(self):
        return tuple(x for x, y in self.__dict__.items() if y is None)

    def calculate(self):
        calculations_dict = {'payment': self.select_payments,
                             'principal': self.principal_value,
                             'periods': self.number_of_payments}
        print(calculations_dict.get(*self.get_none_attr())())

    def add_overpayment(self, message):
        return f'{message}\nOverpayment = {self.full_loan - self.principal}'

    def number_of_payments(self):
        self.periods = math.ceil(math.log(self.payment / (self.payment - self.interest * self.principal),
                                          1 + self.interest))
        self.full_loan = self.periods * self.payment
        years, months = divmod(self.periods, 12)

        output_string = []
        if years > 0:
            output_string.append(f'It will take {years} year{"s" if years > 1 else ""}')
        if months > 0:
            output_string.append(f'and {months} month{"s" if months > 1 else ""}')
        output_string.append('to repay this loan!')
        return self.add_overpayment(' '.join(output_string))

    def select_payments(self):
        if self.type == 'annuity':
            return self.annuity_payment()
        else:
            return self.differential_payment()

    def annuity_payment(self):
        self.payment = math.ceil((self.principal * self.interest * pow(1 + self.interest, self.periods)) /
                                 (pow(1 + self.interest, self.periods) - 1))
        self.full_loan = self.payment * self.periods
        return self.add_overpayment(f'Your monthly payment = {self.payment}!')

    def differential_payment(self):
        output_info = ''
        for month in range(1, self.periods + 1):
            payment = math.ceil(self.principal / self.periods +
                                self.interest * (self.principal - (self.principal * (month - 1)) / self.periods))
            output_info += f'Month {month}: payment is {payment}\n'
            self.full_loan += payment
        return self.add_overpayment(output_info)

    def principal_value(self):
        exp_rate = pow(1 + self.interest, self.periods)
        self.principal = round(self.payment / ((self.interest * exp_rate) / (exp_rate - 1)))
        return self.add_overpayment(f'Your loan principal = {self.principal}!')


if __name__ == '__main__':
    parser = _ArgumentParser(description='Loan Calculator')
    parser.add_argument('--type', choices=['annuity', 'diff'], required=True)
    parser.add_argument('--payment', type=int)
    parser.add_argument('--principal', type=int)
    parser.add_argument('--periods', type=int)
    parser.add_argument('--interest', type=float, required=True)
    args = vars(parser.parse_args())
    args['interest'] /= 1200

    calc = LoanCalculator(**args)

    if calc.type == 'diff' and calc.payment is not None or len(calc.get_none_attr()) > 1:
        parser.error('')
    else:
        calc.calculate()
