import os
import time


def deposit(balance, extract):
    """
    Function to deposit a specified amount into an account balance.

    Args:
        balance (float): The current account balance.
        extract (list): A list to store transaction details.

    Returns:
        tuple: Updated account balance and transaction history list.

    Raises:
        ValueError: If the input amount is not a valid number.
    """

    try:
        value = float(input("Enter the amount to be deposited: "))
        if value > 0:
            balance += value
            extract.append(f"Deposit: R$ {value: .2f}")
            print("Deposit made successfully!")
        else:
            print("Invalid deposit amount.")
    except ValueError:
        print("Invalid deposit amount.")

    return balance, extract


def withdraw(balance, extract, funds, withdraws):
    """
    Function to withdraw a specified amount from an account balance.

    Args:
        balance (float): The current account balance.
        extract (list): A list to store transaction details.
        funds (float): The maximum amount that can be withdrawn.
        withdraws (int): The number of withdrawals made in a day.

    Returns:
        tuple: Updated account balance, transaction history list, and number of withdrawals.

    Raises:
        ValueError: If the input amount is not a valid number.
    """

    try:
        value = float(input("Enter the amount to be withdrawn: "))
        if balance < abs(value):
            print("Insufficient balance.")
        elif value > funds:
            print("Value amount must be R$ 500,00 or lower.")
        else:
            balance -= abs(value)
            extract.append(f"Withdraw: R$ {abs(value): .2f}")
            withdraws += 1
            print("Withdraw made successfully!")

    except ValueError:
        print("Invalid withdraw amount.")
    return balance, extract, withdraws


def show_extract(balance, extract):
    """
    Function to display the transaction history and current balance.

    Args:
        balance (float): The current account balance.
        extract (list): A list containing transaction details.

    Returns:
        None
    """

    if extract:
        print()
        print("Extrato".center(50, "-"))
        [print(transaction) for transaction in extract]
        print("".center(50, "-"))
    else:
        print("\nNo movements were carried out.")
    print(f"Balance: R$ {balance: .2f}")


MENU = """
Select the desired option:
[0] Deposit
[1] Withdraw
[2] Extract
[Q] Quit

=> """

balance = 0
extract = []
FUNDS = 500
withdraws = 0

while True:
    os.system('clear')
    option = input(MENU)

    if option == "0":
        balance, extract = deposit(balance, extract)
    elif option == "1":
        if withdraws >= 3:
            print("Daily withdrawal limit reached.")
        else:
            balance, extract, withdraws = withdraw(balance, extract, FUNDS, withdraws)
    elif option == "2":
        show_extract(balance, extract)
    elif option in "qQ":
        break
    else:
        print("Invalid operation, please select the desired operation again.")

    time.sleep(3)
