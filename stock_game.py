"""A game in which you, the trader, have seven days to make as much money as you can buying and selling stocks."""

import math
import random

import columbo

NUMBER_OF_DAYS = 7
STOCKS = (('ford', 5, 13), ('apple', 100, 212))
STARTING_MONEY = 100


def _calculate_buy_options(answers: columbo.Answers):
    if answers.get('stock_in_portfolio'):
        return [str(i) for i in range(1, answers['stock_in_portfolio'] + 1)]
    else:
        max_quantity = math.floor(answers['money']/answers['stock_price'])
        return [str(i) for i in range(1, max_quantity + 1)]


which_action = columbo.Choice(
    "action",
    "What would you like to do?",
    default="buy",
    options=["buy", "sell", "view", "done"]
)
which_stock = columbo.Choice(
    "stock_name",
    "Which stock?",
    default=STOCKS[0][0],
    options=[stock[0] for stock in STOCKS]
)
how_much_stock = columbo.Choice(
    "stock_quantity",
    "How much?",
    default='1',
    options=_calculate_buy_options
)


def _get_prices():
    prices = {i[0]: random.randint(i[1], i[2]) for i in STOCKS}
    return prices


def _is_last_day(day):
    return NUMBER_OF_DAYS - day == 1


def buy(money, stock_portfolio, prices):
    # todo: provide way to leave buying sequence once started
    stock_name = columbo.get_answers([which_stock])['stock_name']
    stock_price = prices[stock_name]

    if money < stock_price:
        message = 'You do not have enough money to buy this stock.'
        print(message)
        return money, stock_portfolio
    else:
        stock_quantity = int(columbo.get_answers([how_much_stock], answers={'stock_price': stock_price, 'money': money})['stock_quantity'])
        cost = stock_price * stock_quantity
        money -= cost
        stock_portfolio[stock_name] += stock_quantity
        return money, stock_portfolio


def sell(money, stock_portfolio, prices):
    # todo: provide way to leave selling sequence once started
    stock_name = columbo.get_answers([which_stock])['stock_name']
    stock_price = prices[stock_name]

    if not stock_portfolio[stock_name]:
        message = 'You do not have any of this stock.'
        print(message)
        return money, stock_portfolio
    else:
        stock_quantity = int(columbo.get_answers([how_much_stock], answers={'stock_in_portfolio': stock_portfolio[stock_name]})['stock_quantity'])
        cost = stock_price * stock_quantity
        money += cost
        stock_portfolio[stock_name] -= stock_quantity
        return money, stock_portfolio


def _print_output(money, stock_portfolio):
    print(f'Money: {money}')
    print(f'Your portfolio: {stock_portfolio}')


def _play_day(money, stock_portfolio):
    prices = _get_prices()
    print(f'Prices: {prices}')

    while True:
        _print_output(money, stock_portfolio)
        action = columbo.get_answers([which_action])['action']

        if action == 'buy':
            money, stock_portfolio = buy(money, stock_portfolio, prices)
        elif action == 'sell':
            money, stock_portfolio = sell(money, stock_portfolio, prices)
        elif action == 'view':
            # todo: handle this action
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
