import datetime
import re
from tabulate import tabulate

class TransactionsMode:
    """
    Allows user to record their transactions. 
    """

    def __init__(self, transaction_service: any, category_service: any, account_service: any) -> None:
        """
        Initializes TransactionsMode class.
        """
        self.transaction_service = transaction_service
        self.category_service = category_service
        self.account_service = account_service

    def display_transactions_mode_menu(self) -> None:
        """
        Displays transactions mode menu.
        """
        while True:
            print("\nTransactions:")
            print("1. Add income")
            print("2. Add expense")
            print("3. Add transfer")
            print("4. Go back to main menu")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_income()
            elif choice == "2":
                self.add_expense()
            elif choice == "3":
                self.add_transfer()
            elif choice == "4":
                return
            else:
                print("\n⚠️  Invalid input. Please enter a valid option.")

    def add_income(self) -> None:
        """
        Gets user inputs for adding income.
        Adds transaction to transaction file. 
        Updates account balance. 
        """

        print("\n💸 Adding your income:")

        try:
            date = self.get_date_input()
            amount = self.get_float_input()

            self.display_categories("Income")
            category = self.get_category_input("Income")

            self.display_accounts()
            to_account = self.get_account_input()

            note = input("\nEnter a note (optional): ")

            to_account_id = self.account_service.get_account_id_by_name(to_account)

            self.transaction_service.add_transaction(
                transaction_type="Income",
                date=date,
                amount=amount,
                category_name=category,
                from_account_id="",
                from_account="",
                to_account_id=to_account_id,
                to_account=to_account,
                note=note
            )

            self.account_service.update_account_balance(to_account, amount)

            print(f"\n✔️  Your income in the amount of {amount} on {date} has been added to {to_account} account under category '{category}'")
        except EOFError:
            print("\n\nOperation was cancelled. Returning to previous menu...\n")
            return

    def add_expense(self) -> None:
        """
        Gets user inputs for adding an expense.
        Adds transaction to transaction file.
        Updates account balance.
        """
        print("\n💸 Adding your expense:")

        try:
            date = self.get_date_input()
            amount = self.get_float_input()

            self.display_categories("Expense")
            category = self.get_category_input("Expense")

            self.display_accounts()
            from_account = self.get_account_input()

            note = input("\nEnter a note (optional): ")

            if self.account_service.check_if_balance_negative(from_account, -amount):
                if not self.check_if_to_proceed_with_negative_balance(from_account):
                    return
                
            from_account_id = self.account_service.get_account_id_by_name(from_account)

            self.transaction_service.add_transaction(
                transaction_type="Expense",
                date=date,
                amount=-amount,  
                category_name=category,
                from_account_id=from_account_id,
                from_account=from_account,
                to_account_id="",
                to_account="",
                note=note
            )

            self.account_service.update_account_balance(from_account, -amount)

            print(f"\n✔️  Your expense in the amount of {amount} on {date} has been deducted from {from_account} account under category '{category}'")
        except EOFError:
            print("\n\nOperation was cancelled. Returning to previous menu...")
            return

    def add_transfer(self) -> None:
        """
        Gets user inputs for adding a transfer.
        Adds transaction to transaction file.
        Updates account balances.
        """
        print("\n💸 Adding your transfer:")

        try:
            date = self.get_date_input()
            amount = self.get_float_input()

            self.display_accounts()

            print("\nChoose the account to transfer the funds from")
            from_account = self.get_account_input()

            to_account = None
            while True:
                print("\nChoose the account to transfer the funds to")
                to_account = self.get_account_input()

                if from_account == to_account:
                    print("\n⚠️  Cannot transfer to the same account. Please choose a different account.")
                else:
                    break

            if self.account_service.check_if_balance_negative(from_account, -amount):
                if not self.check_if_to_proceed_with_negative_balance(from_account):
                    return

            note = input("\nEnter a note (optional): ")

            from_account_id = self.account_service.get_account_id_by_name(from_account)
            to_account_id = self.account_service.get_account_id_by_name(to_account)

            self.transaction_service.add_transaction(
                transaction_type="Transfer Out",
                date=date,
                amount=-amount, 
                category_name="Transfer",
                from_account_id=from_account_id,
                from_account=from_account,
                to_account_id="", 
                to_account="",
                note=note
            )

            self.transaction_service.add_transaction(
                transaction_type="Transfer In",
                date=date,
                amount=amount,
                category_name="Transfer",
                from_account_id="", 
                from_account="",
                to_account_id=to_account_id,
                to_account=to_account,
                note=note
            )

            self.account_service.update_account_balance(from_account, -amount)
            self.account_service.update_account_balance(to_account, amount)

            print(f"\n✔️  Your transfer from {from_account} account to {to_account} account in the amount of {amount} has been executed successfully.")
        except EOFError:
            print("\n\nOperation was cancelled. Returning to previous menu...")
            return
        
    def get_date_input(self) -> str:
        """
        Helper method that gets date, verifies input.
        Allows user to press "enter" to select current date. 
        """
        current_date = datetime.date.today().strftime("%d-%m-%Y")
        print(f"\nCurrent date is {current_date}. Press 'enter' to select it or enter a new one in DD-MM-YYYY format.")
        date_input = input("Enter date: ").strip() or current_date
        
        while True:
            try:
                date_input = re.sub(r"[\./\s]", "-", date_input)
                date = datetime.datetime.strptime(date_input, "%d-%m-%Y")
                return date.strftime("%d-%m-%Y")
            except ValueError:
                print("\n⚠️  Invalid date format. Please enter the date in DD-MM-YYYY format.")
                date_input = input("Enter date: ").strip()
        
    def get_float_input(self) -> float:
        """
        Helper method that gets a float input, verifies it.
        """
        while True:
            amount_input = input("\nEnter amount: ").strip().replace(",", ".")
            parts = amount_input.split(".")
            try:
                amount = float(amount_input)
                if amount <= 0:
                    raise ValueError("\n⚠️  Amount should be provided in format xx.xx.")
                elif len(parts) > 1 and len(parts[1]) > 2:
                    raise ValueError("\n⚠️  Amount must not have more than two decimal places.")
                else:
                    return amount
            except ValueError:
                 print(f"\n⚠️  Invalid input. Please enter a valid amount with up to two decimal places.")
                
    def display_categories(self, category_type) -> None:
        """
        Helper method that displays categories of a specific type.
        """
        print(f"\nAvailable {category_type} categories:")
        
        filtered_categories = {
            id: name for id, name in self.category_service.categories[category_type].items() if id != "0"
        }

        categories = [
            [id, name]
            for id, name in filtered_categories.items()
        ]

        print(tabulate(categories, headers=["ID", "Name"], tablefmt="grid"))

    def get_category_input(self, category_type: str) -> str:
        """
        Helper method that gets category input, verifies it.
        Allows the user to press enter to select "Uncategorized".
        """
        prompt = f"\nSelect an {category_type} category ID from the provided list or press 'enter' to leave transaction uncategorized: "
        while True:
            category_id = input(prompt).strip()
            if category_id == "":
                return "Uncategorized"
            elif category_id in self.category_service.categories[category_type] and category_id != "0":
                return self.category_service.categories[category_type][category_id]
            else:
                print("\n⚠️  Invalid category ID. Please select from the available categories.")

    def display_accounts(self) -> None:
        """
        Helper method that displays accounts.
        """
        print("\nAvailable accounts:")

        accounts_df = self.account_service.df
        columns_to_display = ["Account_ID", "Name", "Balance"]
        headers = ["ID", "Name", "Balance"]

        accounts = accounts_df[columns_to_display].values.tolist()
        print(tabulate(accounts, headers=headers, tablefmt="grid"))

    def get_account_input(self) -> None:
        """
        Helper method that gets account input, verifies input.
        """
        while True:
            account_id = input("\nEnter the account ID: ").strip()
            if self.account_service.df["Account_ID"].eq(int(account_id)).any():
                return self.account_service.df.loc[
                    self.account_service.df["Account_ID"] == int(account_id), "Name"
                ].values[0]
            else:
                print("\n⚠️  Invalid account ID. Please select from the available accounts.")

    def check_if_to_proceed_with_negative_balance(self, from_account: str ) -> bool:
        print(f"\nThis expense will result in a negative balance in your {from_account} account. Are you sure you want to proceed?")
        print("1. Yes")
        print("2. No")
        
        while True:
            user_choice = input("Select your option: ")

            if user_choice == "1":
                return True 
            elif user_choice == "2":
                return False
            else: 
                print("\n⚠️  Invalid input. Please enter a valid option.\n")
