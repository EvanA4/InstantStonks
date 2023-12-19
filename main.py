"""
What we want:
1. console like interface
2. at least 1 randomly selecting portfolio
    - select own duration and start time for experiment
    - print statistics and matplotlib display of $/time
3. custom select number of random portfolios?
    - stats and plot
4. make own portfolio with custom duration and start time
    - stats and plot
"""

import yfinance as yf
from matplotlib import pyplot as plt
from datetime import date
from dateutil.relativedelta import relativedelta as rd
import pandas as pd
import random



class Portfolio:
    def __init__(self, name):
        self.name = name
        self.data = pd.DataFrame()
        self.invests = []
        self.input = 0



def rand(args):
    # error handle args
    if (len(args) != 4):
        print('Invalid arguments. Enter \"help\" for details.\n')
        return
    for arg in args[1:]:
        try:
            if (int(arg) < 1):
                print('Invalid arguments. Enter \"help\" for details.\n')
                return
        except:
            print('Invalid arguments. Enter \"help\" for details.\n')
            return

    # begin data analysis
    start_date = date.today() - rd(months=int(args[3]))
    ps = []
    plt.figure()
    
    f = open("stockList.txt")
    stocks = f.readlines()

    for i in range(int(args[1])): # for each portfolio...
        ps.append(Portfolio("p" + str(i)))
        
        for j in range(int(args[2])):
            stock = random.choice(stocks)[0:-1]
            ps[i].invests.append(stock)
            temp = yf.Ticker(stock).history(start=start_date.strftime("%Y-%m-%d"), interval="1d")
            ps[i].input += temp["Close"][0]
            temp["Close"] -= temp["Close"][0]
            if (j == 0):
                ps[i].data = temp["Close"]
            else:
                ps[i].data += temp["Close"]
        
        print("Portfolio Name:  ", ps[i].name)
        print("Total input:     %.2f" % ps[i].input)
        print("Invests:         ", end="")
        for j in range(len(ps[i].invests)):
            if (j != 0):
                print(", " + ps[i].invests[j], end="")
            else:
                print(ps[i].invests[j], end="")
        print()
        
        ps[i].data.plot(label=ps[i].name)
    print()
    
    plt.legend()
    plt.show()

if __name__ == "__main__":
    print( "\n" +
    "####################################################\n" +
    "#              Instant Stonk Terminal              #\n" +
    "####################################################\n" +
    "\nEnter \"help\" for a list of commands.\n\n"
    )

    while (True):
        # read command and split into args
        cmd = input('> ')
        args = cmd.split(' ')

        # execute command
        if (args[0] == 'help'):
            print('help                                                                - print this message')
            print('rand [# of portfolios] [# of invests] [# of months]                 - simulates portfolio(s) with randomly selected stock(s) for a number of months at the given start day')
            print('quit                                                                - exits the terminal')
            print()
        elif (args[0] == 'rand'):
            rand(args)
        elif (args[0] == 'quit'):
            quit()
        else:
            print('Unknown command.\n')