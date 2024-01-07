from tabulate import tabulate
from datetime import datetime


class SettingsMode:
    """
    Allows user to manage settings for categories and accounts.
    """

    def __init__(
        self, transaction_service: any, category_service: any, account_service: any
    ) -> None:
        """
        Initializes SettingsMode class.
        """
        self.category_service = category_service
        self.account_service = account_service
        self.transaction_service = transaction_service 

    def display_settings_mode_menu(self) -> None:
        """
        Displays settings menu.
        Gets user input.
        """
        while True:
            print("\nSettings:")
            print("1. Manage categories")
            print("2. Manage accounts")
            print("3. Manage financial goals")
            print("4. Go back to main menu")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.choose_category_type()
            elif choice == "2":
                self.manage_accounts()
            elif choice == "3":
                self.manage_financial_goals()
            elif choice == "4":
                return
            else:
                print("\n⚠️  Invalid input. Please enter a valid option.")

    def choose_category_type(self) -> None:
        """
        Manages categories.
        """
        try:
            while True:
                print("\nChoose category type:")
                print("1. Income")
                print("2. Expense")
                print("3. Go back")

                choice = input("Enter your choice: ").strip()

                if choice == "1":
                    self.manage_categories_by_type("Income")
                elif choice == "2":
                    self.manage_categories_by_type("Expense")
                elif choice == "3":
                    return
                else:
                    print("\n⚠️  Invalid input. Please enter a valid option.\n")
        except EOFError:
            print("\n\nOperation was cancelled. Returning to previous menu...")
            return

    def manage_categories_by_type(self, category_type: str) -> None:
        """
        Allows user to add, change or delete a category.
        Gets user input for the action.
        """
        try:
            while True:
                self.display_categories(category_type)

                print(f"\n{category_type} categories - choose what to do:")
                print("1. Add new category")
                print("2. Change category name")
                print("3. Delete category")
                print("4. Go back")

                choice = input("Enter your choice: ").strip()

                if choice == "1":
                    self.add_category(category_type)
                elif choice == "2":
                    self.change_category_name(category_type)
                elif choice == "3":
                    self.delete_category(category_type)
                elif choice == "4":
                    return
                else:
                    print("\n⚠️  Invalid input. Please enter a valid option.\n")
        except EOFError:
            print("\n\nOperation was cancelled. Returning to previous menu...")
            return
        
    def manage_accounts(self) -> None:
        """
        Allows user to add, rename or delete an account.
        """

        try:
            while True:
                self.display_accounts(include_goals=False)

                print(f"\nAccounts - choose what to do:")
                print("1. Add new account")
                print("2. Change account name")
                print("3. Delete account")
                print("4. Go back")

                choice = input("Enter your choice: ").strip()

                if choice == "1":
                    self.add_account()
                elif choice == "2":
                    self.change_regular_account_name()
                elif choice == "3":
                    self.delete_regular_account()
                elif choice == "4":
                    return
                else:
                    print("\n⚠️  Invalid input. Please enter a valid option.\n")
        except EOFError:
            print("\n\nOperation was cancelled. Returning to previous menu...")
            return
        
    def manage_financial_goals(self) -> None:
        """
        Allows user to add financial goals or to delete them.
        """

        try:
            while True:
                self.display_accounts(include_goals=True)
                print("\nFinancial goals - choose what to do:")
                print("1. Add new goals")
                print("2. Delete goals")
                print("3. Go back")

                choice = input("Enter your choice: ").strip()

                if choice == "1":
                    self.add_new_financial_goal_account()
                elif choice == "2":
                    self.delete_financial_goal_account()
                elif choice == "3":
                    return
                else:
                    print("\n⚠️  Invalid input. Please enter a valid option.\n")
        except EOFError:
            print("\n\nOperation was cancelled. Returning to previous menu...")
            return

    def display_categories(self, category_type: str) -> None:
        """
        Displays categories in a tabulated format.
        """

        print(f"\nCurrent {category_type} categories:")
        filtered_categories = {
            id: name for id, name in self.category_service.categories[category_type].items() if id != "0"
        }

        categories = [
            [id, name]
            for id, name in filtered_categories.items()
        ]

        print(tabulate(categories, headers=["ID", "Name"], tablefmt="grid"))

    def add_category(self, category_type: str) -> None:
        """
        Adds a new category.
        """
        while True:
            category_name = input("\nEnter the new category name: ").strip()
            if (
                category_name
                in self.category_service.categories[category_type].values()
            ):
                print(
                    f"\n⚠️  The category '{category_name.capitalize()}' already exists. Please enter a different name."
                )
            else:
                break

        new_category = self.category_service.add_category(category_type, category_name)
        print(
            f"\n✔️  Category '{new_category.category_name}' was added under '{category_type}' with ID {new_category.category_id}."
        )

    def change_category_name(self, category_type: str) -> None:
        """
        Changes a category's name.
        """
        category_id = input("\nEnter the ID of the category to change: ").strip()
        if (
            category_id.isdigit()
            and category_id in self.category_service.categories[category_type]
        ):
            old_name = self.category_service.categories[category_type][category_id]
            new_name = input("Enter the new name for the category: ").strip()
            if new_name in self.category_service.categories[category_type].values():
                print(
                    f"\n⚠️  The category name '{new_name}' already exists. Please choose a different name."
                )
            else:
                self.category_service.edit_category(
                    category_type, int(category_id), new_name
                )
                self.transaction_service.update_transactions_category(
                    old_name, new_name
                )
                print(
                    f"\n✔️  Category ID {category_id} name was changed from {old_name} to {new_name}."
                )
        else:
            print(
                f"\n⚠️  Category ID {category_id} does not exist within {category_type} categories."
            )

    def delete_category(self, category_type: str) -> None:
        """
        Deletes a category and updates transactions to "Uncategorized".
        """
        category_id = input("\nEnter the ID of the category to delete: ").strip()
        if (
            category_id.isdigit()
            and category_id in self.category_service.categories[category_type]
        ):
            category_name = self.category_service.categories[category_type][category_id]
            print(
                "\nAre you sure you want to delete the category? All existing transactions will become uncategorized."
            )
            print("1. Yes")
            print("2. No")
            confirmation = input("Enter your choice: ").strip()
            if confirmation == "1":
                self.category_service.delete_category(category_type, int(category_id))
                self.transaction_service.uncategorize_transactions(category_name)
                print(
                    f"\n✔️  Category ID {category_id} has been deleted and associated transactions are now uncategorized."
                )
            else:
                print("\n⚠️  Category deletion cancelled.")
        else:
            print(
                f"\n⚠️  Category ID '{category_id}' does not exist within {category_type} categories."
            )
        
    def delete_regular_account(self) -> None:
            """
            Deletes an account, transfers account balance to Main Account.
            """
            
            print("\n💡  Keep in mind that the Main account cannot be deleted.")

            account_id = input("\nEnter the ID of the account to delete: ").strip()

            if not account_id.isdigit() or not self.account_service.df["Account_ID"].eq(int(account_id)).any():
                print(f"\n⚠️  No account found with ID {account_id}.")
                return
            elif self.account_service.df.loc[self.account_service.df["Account_ID"] == int(account_id), 'Name'].str.lower().eq('main').any():
                print("\n⚠️  The Main account cannot be deleted.")
                return
            
            account_row = self.account_service.df[self.account_service.df["Account_ID"] == int(account_id)]
            account_name = account_row.iloc[0]["Name"]
            balance_to_transfer = account_row.iloc[0]["Balance"]

            if self.confirm_account_deletion(account_name, int(account_id), balance_to_transfer):
                self.transfer_balance_to_main(int(account_id), account_name, balance_to_transfer)
                self.account_service.delete_account(int(account_id))
                print(f"\n✔️  Account {account_name} was deleted successfully.")
            else:
                print("\n⚠️  Account deletion cancelled.")

    def change_regular_account_name(self) -> None:
        """
        Edits an existing category and updates the category name in transactions.
        """
        print("\n💡  Keep in mind that the Main account cannot be renamed.")

        account_id = input("\nEnter the ID of the account to rename: ").strip()

        if not account_id.isdigit() or not self.account_service.df["Account_ID"].eq(int(account_id)).any():
            print(f"\n⚠️  No account found with ID {account_id}.")
            return
        elif self.account_service.df.loc[self.account_service.df["Account_ID"] == int(account_id), "Name"].str.lower().eq("main").any():
            print("\n⚠️  The Main account cannot be renamed.")
            return
        
        new_name = input("\nEnter the new name for the account: ").strip()

        if self.account_service.df['Name'].str.lower().eq(new_name.lower()).any():
            print(f"An account with the name '{new_name}' already exists. Please try a different name.")
            return
        elif not new_name:
            print("No input has been provided. Please enter a name.")
            return
        
        self.account_service.edit_account_name(int(account_id), new_name)
        self.transaction_service.update_account_name_in_transactions(int(account_id), new_name)
        print(f"\n✔️  Account with ID {account_id} has been renamed to '{new_name}'.")

    def add_new_financial_goal_account(self) -> None:
        """
        Adds a new account as a financial goal.
        """
        name = self.get_account_name("\nEnter the name of your financial goal: ")

        current_saved_amount = self.get_float_number("\nEnter the amount you've saved up so far: ")
        goal_amount = self.get_float_number("\nEnter the amount you need: ")

        note = input("\nEnter a note for the account (optional): ").strip()

        goal_account = self.account_service.add_account(
            name=name,
            balance=current_saved_amount,
            is_goal="Yes",  
            goal_amount=goal_amount, 
            note=note
        )

        print(f"\n✔️  Financial goal {goal_account.name} has been added with a goal amount of {goal_amount}.")

    def delete_financial_goal_account(self) -> None:
        """
        Allows the user to delete financial goal accounts.
        """
        account_id = input("\nEnter the ID of the financial goal account to delete: ").strip()

        if not account_id.isdigit() or not self.account_service.df["Account_ID"].eq(int(account_id)).any():
            print(f"\n⚠️  No account found with ID {account_id}.")
            return
        
        account_row = self.account_service.df[self.account_service.df["Account_ID"] == int(account_id)]
        if account_row.empty or account_row.iloc[0]["Is_Goal"].lower() != "yes":
            print(f"\n⚠️  Account ID {account_id} is not a financial goal.")
            return

        account_name = account_row.iloc[0]["Name"]
        balance_to_transfer = account_row.iloc[0]["Balance"]

        if self.confirm_account_deletion(account_name, int(account_id), balance_to_transfer):
            self.transfer_balance_to_main(int(account_id), account_name, balance_to_transfer)
            self.account_service.delete_account(int(account_id))
            print(f"\n✔️  Financial goal {account_name} was deleted successfully.")
        else:
            print("\n⚠️  Goal deletion cancelled.")

    def display_accounts(self, include_goals: bool = False) -> None:
        """
        Displays accounts in a tabulated format.
        If include_goals is True, it also displays financial goal accounts with their goal amounts.
        """
        if include_goals:
            accounts_df = self.account_service.df[self.account_service.df["Is_Goal"].str.lower() == "yes"]
            columns_to_display = ["Account_ID", "Name", "Balance", "Goal_Amount", "Note"]
            headers = ["ID", "Name", "Saved Amount", "Goal Amount", "Note"]
        else:
            accounts_df = self.account_service.df[self.account_service.df["Is_Goal"].str.lower() == "no"]
            columns_to_display = ["Account_ID", "Name", "Balance"]
            headers = ["ID", "Name", "Balance"]

        if include_goals and accounts_df.empty:
            print("\nYou currently have no financial goals. Set some.😉")
        else:
            accounts = accounts_df[columns_to_display].values.tolist()
            print("\nCurrent Accounts:" if not include_goals else "\nCurrent Financial Goals:")
            print(tabulate(accounts, headers=headers, tablefmt="grid"))

    def add_account(self) -> None:
            """
            Adds a new account.
            """
            name = self.get_account_name("\nEnter the new account name: ")

            balance = self.get_float_number("\nEnter the initial balance for the account: ")

            note = input("\nEnter a note for the account (optional): ").strip()
            account = self.account_service.add_account(name, balance, "No", "", note)
            print(f"\n✔️  Account '{account.name}' has been added with balance {balance}.")

    
    def get_account_name(self, prompt: str) -> str:
        """
        Gets and validates account name.
        """
        while True:
            name = input(prompt).strip()
            if self.account_service.df["Name"].str.lower().eq(name.lower()).any():
                print(f"\n⚠️  An account with the name '{name}' already exists. Please try a different name.")
            elif not name:
                print("\n⚠️  No input has been provided. Please enter a name.")
            else:
                return name

    def get_float_number(self, prompt: str) -> float:
        """
        Gets and validates a float value.
        """
        while True:
            balance_input = input(prompt).strip().replace(",", ".")
            parts = balance_input.split(".")
            try:
                balance_input = float(balance_input)
                if balance_input < 0:
                    raise ValueError("\n⚠️  Amount should be provided in format xx.xx.")
                elif len(parts) > 1 and len(parts[1]) > 2:
                    raise ValueError("\n⚠️  Amount must not have more than two decimal places.")
                else:
                    return balance_input
            except ValueError:
                 print(f"\n⚠️  Invalid input. Please enter a valid amount with up to two decimal places.")

    
    def confirm_account_deletion(self, account_name: str, account_id: int, balance_to_transfer: float) -> bool:
        """
        Confirms with the user if they want to delete the account.
        """
        print(f"\nAccount {account_name} ID {account_id} has a balance of {balance_to_transfer}")
        print("By deleting this account, you will transfer this balance to the Main account.")
        print("Do you want to proceed?")
        print("1. Yes")
        print("2. No")

        while True:
            confirmation = input("Enter your choice: ").strip()
            if confirmation == "1":
                return True
            elif confirmation == "2":
                return
            else:
                print("\n⚠️  Invalid input. Please enter a valid option.\n")

    def transfer_balance_to_main(self, from_account_id: int, from_account_name: str, balance_to_transfer: float) -> None:
        """
        Transfers the balance from the deleted account to the Main account.
        """
        if balance_to_transfer > 0:
            main_account_id = self.account_service.get_account_id_by_name("Main")
            today = datetime.today().strftime("%d-%m-%Y")
            self.transaction_service.add_transaction(
                transaction_type="Transfer",
                date=today,
                amount=balance_to_transfer,
                from_account_id=from_account_id,
                from_account=from_account_name,
                to_account_id=main_account_id,
                to_account="Main",
                note="Transfer due to account deletion"
            )



