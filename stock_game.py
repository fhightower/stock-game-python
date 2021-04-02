"""A game in which you, the trader, have seven days to make as much money as you can buying and selling stocks."""

import math
import random

import columbo

NUMBER_OF_DAYS = 7
STOCKS = (('ford', 5, 13), ('apple', 100, 212))
STARTING_MONEY = 100


def _get_stock_name_options(answers: columbo.Answers):
    if answers['action'] == 'sell':
        return [stock[0] for stock in STOCKS]
    elif answers['action'] == 'buy':
        return [stock[0] for stock in STOCKS if answers['prices'][stock[0]] <= answers['money']]


def _get_stock_quantity_options(answers: columbo.Answers):
    if answers['action'] == 'sell':
        return [str(i) for i in range(1, answers['portfolio'][answers['stock_name']] + 1)]
    elif answers['action'] == 'buy':
        max_quantity = math.floor(answers['money'] / answers['prices'][answers['stock_name']])
        return [str(i) for i in range(1, max_quantity + 1)]


questions = [
    columbo.Choice(
        'action',
        'What would you like to do?',
        default='buy',
        options=['buy', 'sell', 'view', 'done'],
    ),
    columbo.Choice(
        'stock_name',
        'Which stock?',
        default=STOCKS[0][0],
        options=_get_stock_name_options,
        should_ask=lambda answers: answers['action'] == 'buy' or answers['action'] == 'sell',
    ),
    columbo.Choice(
        'how_much',
        'How much?',
        default='1',
        options=_get_stock_quantity_options,
        should_ask=lambda answers: answers['action'] == 'buy' or answers['action'] == 'sell',
    ),
]


def _get_prices():
    prices = {i[0]: random.randint(i[1], i[2]) for i in STOCKS}
    return prices


def _is_last_day(day):
    return NUMBER_OF_DAYS - day == 1


def buy(money, stock_portfolio, prices, answers: columbo.Answers):
    stock_price = prices[answers['stock_name']]
    stock_quantity = int(answers['how_much'])
    cost = stock_price * stock_quantity

    money -= cost
    stock_portfolio[answers['stock_name']] += stock_quantity

    return money, stock_portfolio


def sell(money, stock_portfolio, prices, answers: columbo.Answers):
    stock_price = prices[answers['stock_name']]
    stock_quantity = int(answers['how_much'])
    cost = stock_price * stock_quantity

    money += cost
    stock_portfolio[answers['stock_name']] -= stock_quantity

    return money, stock_portfolio


def _print_output(money, stock_portfolio, prices):
    print(f'\nMoney: {money}')
    print(f'Your portfolio: {stock_portfolio}')
    print(f'Prices: {prices}\n')


def _play_day(money, stock_portfolio):
    prices = _get_prices()

    while True:
        _print_output(money, stock_portfolio, prices)
        try:
            answers = columbo.get_answers(
                questions,
                answers={'money': money, 'portfolio': stock_portfolio, 'prices': prices},
            )
        except ValueError:  # a ValueError will be raised if the user wants to buy/sell stock he/she cannot
            continue

        if answers['action'] == 'buy':
            money, stock_portfolio = buy(money, stock_portfolio, prices, answers)
        elif answers['action'] == 'sell':
            money, stock_portfolio = sell(money, stock_portfolio, prices, answers)
        elif answers['action'] == 'view':
            pass
        else:
            # we're done!
            return money, stock_portfolio


def play():
    day = 0
    money = STARTING_MONEY
    stock_portfolio = {i[0]: 0 for i in STOCKS}

    while day < NUMBER_OF_DAYS:
        print(f'Day {day}')

        if _is_last_day(day):
            print(f'It is your last day... be sure to sell all of your stocks!')

        money, stock_portfolio = _play_day(money, stock_portfolio)

        if _is_last_day(day):
            message = f'You\'re done! You ended up with ${money} (+{money - STARTING_MONEY})'
            print(message)

        day += 1


if __name__ == '__main__':
    play()
