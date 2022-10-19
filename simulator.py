from random import randint
from matplotlib import pyplot as plt
import collections

def roll_dice():
    '''random 2 dice roll'''
    die_1 = randint(1,6)
    die_2 = randint(1,6)
    roll_total = die_1 + die_2
    return roll_total


def plot_roll_frequency(results_list):
    '''plot frequency of dice rolls'''
    c = collections.Counter(results_list)
    c = sorted(c.items())
    roll_totals = [i[0] for i in c]
    freq = [i[1] for i in c]
    f, ax = plt.subplots()

    plt.bar(roll_totals, freq)
    plt.title("Roll total frequency")
    plt.xlabel("Roll Total")
    plt.ylabel("Frequency")
    ax.set_xticks(range(2, 13))

    plt.show()



#results_list = []
#for i in range(0,150):
#    results_list.append(roll_dice())

#plot_roll_frequency(results_list)

def come_out_roll():
    print("Come out roll")
    result = roll_dice()
    return result

def start_game(m, bets):
    return m, bets

def make_bet(bets, bet, amount):
    bets[bet] = amount
    return bets


balance, bets = start_game(100, {'pass_line': 0})

bets = make_bet(bets, 'pass_line', 10)

result = come_out_roll()
print(result)

if result in [7,11]:
    print("You win!")
    balance += bets['pass_line']
elif result in [2,3,12]:
    print("You lose")
    balance -= bets['pass_line']

else:
    point = result
    print("Point is ", point)
    round_continue = True
    while round_continue:
        roll = roll_dice()
        print("dice rolled", roll)
        if roll == 7:
            print("You lose")
            balance -= bets['pass_line']
            round_continue = False
        elif roll == point:
            print("You win")
            balance += bets['pass_line']
            round_continue = False
        else:
            continue




print("You have", balance)

