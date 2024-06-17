import textwrap
import os
import time
import re
from abc import ABC, abstractmethod
from datetime import datetime


class Client:
    def __init__(self, address):
        self.address = address
        self.accounts = []

    def perform_transaction(self, account, transaction):
        transaction.record(account)

    def add_account(self, account):
        self.accounts.append(account)


class Individual(Client):
    def __init__(self, name, birth_date, cpf, address):
        super().__init__(address)
        self.name = name
        self.birth_date = birth_date
        self.cpf = cpf


class Account:
    def __init__(self, number, client):
        self._balance = 0
        self._number = number
        self._branch = "0001"
        self._client = client
        self._history = History()

    @classmethod
    def new_account(cls, client, number):
        return cls(number, client)

    @property
    def balance(self):
        return self._balance

    @property
    def number(self):
        return self._number

    @property
    def branch(self):
        return self._branch

    @property
    def client(self):
        return self._client

    @property
    def history(self):
        return self._history

    def withdraw(self, amount):
        balance = self.balance
        exceeded_balance = amount > balance

        if exceeded_balance:
            print("\nOperation failed! You do not have enough balance. ")

        elif amount > 0:
            self._balance -= amount
            print("\n====== Withdrawal successful! ======")
            return True

        else:
            print("\nOperation failed! The amount entered is invalid. ")

        return False

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print("\n====== Deposit successful! ======")
        else:
            print("\nOperation failed! The amount entered is invalid. ")
            return False

        return True


class CheckingAccount(Account):
    def __init__(self, number, client, limit=500, withdrawal_limit=3):
        super().__init__(number, client)
        self._limit = limit
        self._withdrawal_limit = withdrawal_limit

    def withdraw(self, amount):
        number_of_withdrawals = len(
            [
                transaction
                for transaction in self.history.transactions
                if transaction["type"] == Withdrawal.__name__
            ]
        )

        exceeded_limit = amount > self._limit
        exceeded_withdrawals = number_of_withdrawals >= self._withdrawal_limit

        if exceeded_limit:
            print("\nOperation failed! The withdrawal amount exceeds the limit. ")

        elif exceeded_withdrawals:
            print("\nOperation failed! Maximum number of withdrawals exceeded. ")

        else:
            return super().withdraw(amount)

        return False

    def __str__(self):
        return f"""
            Agency: {self.branch}
            Account: {self.number}
            Owner: {self.client.name}
        """


class History:
    def __init__(self):
        self._transactions = []

    @property
    def transactions(self):
        return self._transactions

    def add_transaction(self, transaction):
        self._transactions.append(
            {
                "type": transaction.__class__.__name__,
                "amount": transaction.amount,
                "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transaction(ABC):
    @property
    @abstractmethod
    def amount(self):
        pass

    @abstractmethod
    def record(self, account):
        pass


class Withdrawal(Transaction):
    def __init__(self, amount):
        self._amount = amount

    @property
    def amount(self):
        return self._amount

    def record(self, account):
        if account.withdraw(self.amount):
            account.history.add_transaction(self)


class Deposit(Transaction):
    def __init__(self, amount):
        self._amount = amount

    @property
    def amount(self):
        return self._amount

    def record(self, account):
        if account.deposit(self.amount):
            account.history.add_transaction(self)


def filter_client(cpf, clients):
    filtered_clients = [client for client in clients if client.cpf == cpf]
    return filtered_clients[0] if filtered_clients else None


def retrieve_client_account(client):
    if not client.accounts:
        print("\nClient does not have an account!")
        return
    try:
        if len(client.accounts) > 1:
            choose_account = int(input("Enter the account number: "))
            return next(
                (
                    account
                    for account in client.accounts
                    if account.number == choose_account
                ),
                None,
            )
        return client.accounts[0]
    except ValueError:
        print("Invalid number account.")
        return


def deposit(clients):
    cpf = input("Enter the client's cpf: ")
    if not valid_cpf(cpf):
        return
    client = filter_client(cpf, clients)

    if not client:
        print("\nClient not found! ")
        return

    try:
        amount = float(input("Enter the deposit amount: "))
    except ValueError:
        print("Invalid deposit amount.")
        return
    transaction = Deposit(amount)

    if account := retrieve_client_account(client):
        client.perform_transaction(account, transaction)
    else:
        return


def withdraw(clients):
    cpf = input("Enter the client's cpf: ")
    if not valid_cpf(cpf):
        return
    client = filter_client(cpf, clients)

    if not client:
        print("\nClient not found! ")
        return
    try:
        amount = float(input("Enter the withdrawal amount: "))
    except ValueError:
        print("Invalid withdraw amount.")
        return
    transaction = Withdrawal(amount)

    if account := retrieve_client_account(client):
        client.perform_transaction(account, transaction)
    else:
        return


def show_extract(clients):
    cpf = input("Enter the client's cpf: ")
    if not valid_cpf(cpf):
        return
    client = filter_client(cpf, clients)

    if not client:
        print("\nClient not found!")
        return

    account = retrieve_client_account(client)
    if not account:
        return

    print("\n================ Extract ================")
    transactions = account.history.transactions

    extract = ""
    if not transactions:
        extract = "No transactions have been made."
    else:
        for transaction in transactions:
            extract += f"\n{transaction['type']}:\t$ {transaction['amount']:.2f}\t  Date:\t{transaction['date']}"

    print(extract)
    print(f"\nBalance:\t$ {account.balance:.2f}")
    print("==========================================")


def create_client(clients):
    cpf = input("Enter the cpf (numbers only): ")
    if not valid_cpf(cpf):
        return
    client = filter_client(cpf, clients)

    if client:
        print("\nA client with this cpf already exists! ")
        return

    name = input("Enter the full name: ")
    birth_date = input("Enter the birth date (dd/mm/yyyy): ")
    if not re.fullmatch(r"((\d{1,2})/(\d{1,2})/(\d{2,4}))", birth_date):
        print("\nInvalid Birth Date.")
        return
    address = input(
        "Enter the address (street, number - neighborhood - city/state abbreviation): "
    )

    client = Individual(name=name, birth_date=birth_date, cpf=cpf, address=address)

    clients.append(client)

    print("\n===== Client created successfully! =====")


def create_account(account_number, clients, accounts):
    cpf = input("Enter the client's cpf: ")
    if not valid_cpf(cpf):
        return
    client = filter_client(cpf, clients)

    if not client:
        print("\nClient not found, account creation process ended! ")
        return

    account = CheckingAccount.new_account(client=client, number=account_number)
    accounts.append(account)
    client.accounts.append(account)

    print("\n===== Account created successfully! =====")


def list_accounts(accounts):
    for account in accounts:
        print("=" * 100)
        print(textwrap.dedent(str(account)))


def valid_cpf(cpf):
    if not re.fullmatch(r"\d{11}", cpf):
        print("\nInvalid CPF!")
        return
    return True


def menu():
    menu = """\n
    ================ MENU ================
    [0]\tDeposit
    [1]\tWithdraw
    [2]\tExtract
    [3]\tNew Client
    [4]\tNew Account
    [5]\tList Accounts 
    [q]\tQuit
    => """
    return input(textwrap.dedent(menu))


def main():
    clients = []
    accounts = []

    while True:
        os.system("clear")
        option = menu()

        if option == "0":
            deposit(clients)

        elif option == "1":
            withdraw(clients)

        elif option == "2":
            show_extract(clients)

        elif option == "3":
            create_client(clients)

        elif option == "4":
            account_number = len(accounts) + 1
            create_account(account_number, clients, accounts)

        elif option == "5":
            if accounts:
                list_accounts(accounts)
            else:
                print("\nNo accounts to show!")

        elif option == "q":
            break

        else:
            print("\nInvalid operation, please select the desired operation again. ")
        time.sleep(3)


main()
