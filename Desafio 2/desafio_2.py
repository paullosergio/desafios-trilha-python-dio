import os
import re
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
        print("Extract".center(50, "-"))
        [print(transaction) for transaction in extract]
        print("".center(50, "-"))
    else:
        print("\nNo movements were carried out.")
    print(f"Balance: R$ {balance: .2f}")


def create_user(users):
    """
    Creates a new user and adds them to the list of existing users.

    Args:
        users (list): A list of existing users.

    Returns:
        list: Updated list of users with the new user added.
    """

    name = input("Enter the name of the user: ")
    cpf = input("Enter the cpf of the user (Only numbers): ")

    if not re.fullmatch(r"\d{11}", cpf):
        print("\nInvalid CPF!")
        return users

    if cpf in [user["cpf"] for user in users]:
        print("\nCPF already registered.")
        return users

    birth_date = input("Enter the date of birth (Ex: 01/01/2000): ")
    if not re.fullmatch(r"((\d{1,2})/(\d{1,2})/(\d{2,4}))", birth_date):
        print("\nInvalid Birth Date.")
        return users

    address = input(
        "Enter the address of the user: (Ex: Street - Neighborhood - City/State): "
    )
    users.append(
        {"name": name, "cpf": cpf, "birth_date": birth_date, "address": address}
    )
    print("\nUser added.")
    return users


def create_account(accounts, users):
    """
    Creates a new account for a user based on their CPF.

    Args:
        accounts (list): A list of existing accounts.
        users (list): A list of existing users.

    Returns:
        list: Updated list of accounts with the new account added.
    """

    cpf = input("Enter the CPF of the user to create an account: ")
    if cpf not in [user["cpf"] for user in users]:
        print("\nCPF not found in users.")
        return accounts
    accounts.append(
        {
            "Agency": "0001",
            "Account": len(accounts) + 1,
            "User": [user["name"] for user in users if cpf == user["cpf"]][0],
        }
    )
    print("\nAccount created.")
    return accounts


def main():
    """
    Main function to run a banking system simulation with options for deposit,
    withdrawal, account creation, and user creation.

    Returns:
        None
    """

    menu = """
    Select the desired option:
    [0] Deposit
    [1] Withdraw
    [2] Extract
    [3] Create User
    [4] Create Account
    [5] List Users
    [6] List Accounts
    [Q] Quit

    => """

    balance = 0
    funds = 500
    withdraws = 0
    extract = []
    users = []
    accounts = []

    while True:
        os.system("clear")
        option = input(menu)

        if option == "0":
            balance, extract = deposit(balance, extract)
        elif option == "1":
            if withdraws >= 3:
                print("Daily withdrawal limit reached.")
            else:
                balance, extract, withdraws = withdraw(
                    balance=balance, extract=extract, funds=funds, withdraws=withdraws
                )
        elif option == "2":
            show_extract(balance, extract=extract)
        elif option == "3":
            users = create_user(users)
        elif option == "4":
            accounts = create_account(accounts, users)
        elif option == "5":
            if users:
                print("Users".center(50, "-"))
                for user in users:
                    for key, value in user.items():
                        print(f"{key.title()}: {value}")
                    print("".center(50, "-"))

            else:
                print("\nThere is no users added.")
        elif option == "6":
            if accounts:
                print("Accounts".center(50, "-"))
                for account in accounts:
                    for key, value in account.items():
                        print(f"{key.title()}: {value}")
                    print("".center(50, "-"))
            else:
                print("\nThere is no accounts added.")

        elif option in "qQ":
            break
        else:
            print("\nInvalid operation, please select the desired operation again.")

        time.sleep(3)


if __name__ == "__main__":
    main()
