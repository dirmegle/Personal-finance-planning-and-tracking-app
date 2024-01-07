import pandas as pd
from tabulate import tabulate
from rich.progress import Progress


class FinancialGoalsMode:
    """
    Allows user to set and track financial goals.
    """

    def __init__(self, transaction_service: any, category_service: any, account_service: any) -> None:
        """
        Initializes the class with service instances.
        """
        self.category_service = category_service
        self.account_service = account_service
        self.transaction_service = transaction_service 

    def display_financial_goals_mode_menu(self) -> None:
        """
        Shows the user the mode menu.
        Gets user input for further action.
        """

        self.display_financial_goals_table()

        print("Would you like to see details of one of your financial goals?")
        print("1. Yes")
        print("2. No")

        while True:
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                goal_id = self.get_valid_id()
                self.describe_goal_progress(goal_id)
                return
            elif choice == "2":
                return
            else:
                print("\n⚠️  Invalid input. Please enter a valid option.\n")

    def display_financial_goals_table(self) -> None:
        """
        Displays the financial goals table, with "Yes" in the Is_Goal column
        """
        accounts_df = self.account_service.df[self.account_service.df["Is_Goal"].str.lower() == "yes"]
        columns_to_display = ["Account_ID", "Name", "Balance", "Goal_Amount", "Note"]
        headers = ["ID", "Name", "Saved Amount", "Goal Amount", "Note"]

        if accounts_df.empty:
            print("\nYou currently have no financial goals. Set some by going to Settings.😉")
        else:
            accounts = accounts_df[columns_to_display].values.tolist()
            print("\nFinancial Goals:")
            print(tabulate(accounts, headers=headers, tablefmt="grid"))

    def get_valid_id(self) -> int:
        """
        Gets ID of financial goal account for progress representation.
        """
        while True:
            try:
                goal_id = input("\nEnter the ID of the financial goal: ").strip()
                if not goal_id.isdigit():
                    print("\n⚠️  The ID should be a number. Please try again.")
                    continue

                goal_id = int(goal_id)
                if goal_id in self.account_service.df["Account_ID"].values and \
                self.account_service.df[self.account_service.df["Account_ID"] == goal_id]["Is_Goal"].str.lower().eq("yes").any():
                    return goal_id
                else:
                    print("\n⚠️  Invalid ID. Please enter a valid financial goal ID.")
            except ValueError:
                print("\n⚠️  Invalid input. Please enter a number.")

    def describe_goal_progress(self, account_id: int) -> None:
        """
        Displays visual representation towards the goal of the user.
        Also, shows account-related transactions.
        """
        account_details = self.account_service.df.loc[self.account_service.df["Account_ID"] == account_id]
        account_name = account_details["Name"].values[0]
        goal_amount = account_details["Goal_Amount"].values[0]
        goal_balance = account_details["Balance"].values[0]
        
        print(f"\nYour current progress towards the {account_name} goal:")
        print(f"Goal Amount: ${goal_amount:,.2f}")
        print(f"Current Balance: ${goal_balance:,.2f}")

        self.display_progress_bar(goal_amount, goal_balance)

        self.display_account_related_transactions(account_id, account_name)

    def display_progress_bar(self, goal_amount, goal_balance) -> None:
        """
        Displays the progress bar using the rich library
        """
        progress_percentage = (goal_balance / goal_amount) * 100 if goal_amount else 0

        with Progress() as progress:
            task1 = progress.add_task("[green]Progress", total=100)
            progress.update(task1, completed=progress_percentage)
            progress.stop()

    def display_account_related_transactions(self, account_id: int, account_name: str) -> None:
        """
        Displays all transactions relating to the financial goal account.
        """
        transactions_df = self.transaction_service.df.copy()
        transactions_df = transactions_df[((transactions_df["From_Account_ID"] == account_id) | (transactions_df["To_Account_ID"] == account_id))]
        self.format_transactions(transactions_df)

        if not transactions_df.empty:
            transactions_df.insert(0, "Item No.", range(1, len(transactions_df) + 1))
            print(f"\nTransactions related to the {account_name} goal:")
            print(tabulate(
                transactions_df[["Item No.", "Type", "Date", "Amount", "Category", "Note"]],
                headers="keys",
                tablefmt="psql",
                showindex=False,
            ))

    def format_transactions(self, transactions_df: pd.DataFrame) -> None:
        """
        Formats the transactions by handling empty notes.
        """
        transactions_df["Note"] = transactions_df["Note"].fillna("")

    


