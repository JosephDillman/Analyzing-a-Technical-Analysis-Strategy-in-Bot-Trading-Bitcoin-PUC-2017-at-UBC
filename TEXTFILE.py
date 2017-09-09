import ast

"""
ListOfFloat Natural Natural -> Float
The initial natural specifies the lower bound for a range,
the later natural specifies the upper bound for a range.
Both bounds are inclusive.
For all values with positions within the range,
yeild a simple average using those values."""

def simple_average(price_list, lower, upper):
	TEMPORARY = float(0)
	for i in range(lower, upper + 1):
		TEMPORARY += price_list[i]
	return(TEMPORARY / (upper - lower + 1))

"""
Float Float Float -> Float
For a given closing price, a divisor used in calculating the multiplier and
previous period exponential average, yeild an exponential average."""

# Change the function so that a multiplier can be given first hand?

def exponential_average(closing_price, time_period, previous_average):
	MULTIPLIER = 2 / (time_period + 1)
	EXPONENTIAL_AVERAGE = previous_average * (1 - MULTIPLIER) + closing_price * MULTIPLIER
	return(EXPONENTIAL_AVERAGE)

"""
ListOfFloat Natural-> ListOfFloat
For a given list of prices and time period, 
if the position in the list is less than the time period value,
yeild a simple average of all numbers upto and including that float,
else yeild an exponential average."""

def list_average(price_list, time_period):
	AVERAGE_LIST = list()
	LAST_AVERAGE = float()
	for position in range(len(price_list)):
		if position <= time_period:
			LAST_AVERAGE = simple_average(price_list, 0, position)
			AVERAGE_LIST.append(LAST_AVERAGE)
		else:
			LAST_AVERAGE = exponential_average(price_list[position], time_period, LAST_AVERAGE)
			AVERAGE_LIST.append(LAST_AVERAGE)
	return(AVERAGE_LIST)

##############################################################################################################################################

# ListOfFloat & Integer & Integer -> ListOfString
# For a given list of prices, bin value one and bin value two,
# yeild a list of actions where the actions
# are one of the following:
# - buy
# - sell
# - null

def action(price_list, short, long):
	ACTION_LIST = list()
	SHORT_AVERAGE = list_average(price_list, short)
	LONG_AVERAGE = list_average(price_list, long)
	for i in range(len(price_list)):
		ACTION_LIST.append(SHORT_AVERAGE[i] > LONG_AVERAGE[i])
	return(ACTION_LIST)

# ListOfBoolean -> ListOfString
# If the past boolean is the same as the current boolean, yeild an empty string
# If the present boolean is True and the past boolean is False, yeild 'Buy'
# else, yeild 'sell'

"""Reviewed"""

def action_list(boolean_list):
	ACTION_LIST = list()
	PAST_BOOLEAN = boolean_list[0]
	for boolean in boolean_list:
		if PAST_BOOLEAN == boolean:
			ACTION_LIST.append(None)
		elif boolean:
			ACTION_LIST.append(True)
			PAST_BOOLEAN = True
		else:
			ACTION_LIST.append(False)
			PAST_BOOLEAN = False
	return(ACTION_LIST)

##############################################################################################################################################

# Dictionaries

ACCOUNT_A1 = {'USD' : 100.00 , 'BTC' : 0.0}

"""
Account Currency Currency Float Float -> Account
For a given account, currency to be sold, currency to be bought,
amount of currency to be bought, price of currency to be bought,
and fee as a ratio to be deduced, yeild an account with the exchange cleared.
The price of the currency to be bought must be given in the currency to be sold."""

def exchange(account, sell, buy, amount, price, fee):
        account[sell] -= amount * price
        account[buy] += amount * (1 - fee)

"""
Float Action Account -> Account
Where the price of an underlying currency is given in the United States Dollar,
a signal to either buy, sell or maintain the current position and
an account to withdraw and deposit the currencies in question are given,
conduct the action specified and yeild the updated account.

When conducting the exchange, buy or sell as much as possible without yeilding a negative balance

Assume action is a boolean"""

def context_exchange(price, action, account):
	MAXIMUM_BTC = account['USD'] / price
	MAXIMUM_USD = account['BTC'] * price
	if action:
		exchange(account, 'USD', 'BTC', MAXIMUM_BTC, price, 0)
	elif not action:
		exchange(account, 'BTC', 'USD', MAXIMUM_USD, 1 / price, 0)
	else:
		pass
	return(account)

"""
Account ListOfBoolean ListOfPrice -> ListOfAccounts
Conduct the actions listed, yeild a list of accounts
reflecting the corresponding action and price.
If a price, action and account are in the same position within
a list, they each correspond to each other."""

def transaction_list_a(account, action_list, price_list):
	ACCOUNT_LIST = list()
	for i in range(len(action_list)):
		context_exchange(price_list[i], action_list[i], account)
		ACCOUNT_LIST.append(account.copy())
	return(ACCOUNT_LIST)

# Do not include accounts that have not changed

def transaction_list_s(account, action_list, price_list):
	ACCOUNT_LIST = list()
	for i in range(len(action_list)):
		if action_list[i] == None:
			pass
		else:
			context_exchange(price_list[i], action_list[i], account)
			ACCOUNT_LIST.append(account.copy())
	return(ACCOUNT_LIST)

##############################################################################################################################################

with open('/home/maximilian/Desktop/Exchange_Data', 'r') as TEXTFILE:
	EXCHANGE_STRING = TEXTFILE.read()
	
EXCHANGE_LIST = ast.literal_eval(EXCHANGE_STRING)
CLOSING_PRICE_LIST = [element['close'] for element in EXCHANGE_LIST]

##############################################################################################################################################	

BOOLEAN_LIST = action(CLOSING_PRICE_LIST, 5, 10)
ACTION_LIST = action_list(BOOLEAN_LIST)

TRANSACTION_LIST = transaction_list_a({'USD' : 100.00 , 'BTC' : 0.0}, ACTION_LIST, CLOSING_PRICE_LIST)

print(len(CLOSING_PRICE_LIST), len(TRANSACTION_LIST))

'''
def profit(transaction_list):
	PROFIT = float()
	for i in range(1, len(transaction_list)):
		if transaction_list[-i]['USD'] != 0:
			PROFIT = transaction_list[-i]['USD'] - 100
			break
		else:
			pass
	return(PROFIT)


	
for i in range(1, 51):
	for j in range(i):
		print(i, j, profit(transaction_list({'USD' : 100.00 , 'BTC' : 0.0}, action_list(action(CLOSING_PRICE_LIST, j, i)), CLOSING_PRICE_LIST)))

'''
