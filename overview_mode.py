import pandas as pd
import plotext as plt
from tabulate import tabulate
from datetime import datetime, timedelta


class OverviewMode:
    """
    Provides an overview of financial data including accounts, expenses, and income.
    """

    def __init__(
        self, transaction_service: any, category_service: any, account_service: any
    ) -> None:
        """
        Initializes OverviewMode class.
        """
        self.transaction_service = transaction_service
        self.category_service = category_service
        self.account_service = account_service

    def display_overview_mode_menu(self) -> None:
        """
        Displays overview mode menu.
        """
        while True:
            print("\nOverview:")
            print("1. Accounts")
            print("2. Income")
            print("3. Expenses")
            print("4. Transfers")
            print("5. Categories")
            print("6. Total balance sheet")
            print("7. Go back to main menu")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.display_accounts_overview()
            elif choice == "2":
                self.display_income_overview()
            elif choice == "3":
                self.display_expense_overview()
            elif choice == "4":
                self.display_transfer_overview()
            elif choice == "5":
                self.display_category_overview()
            elif choice == "6":
                self.display_balance_sheet_overview()
            elif choice == "7":
                return
            else:
                print("\n⚠️  Invalid input. Please enter a valid option.\n")

    # Main behavior methods:
    def display_accounts_overview(self) -> None:
        """
        Displays the current account information.
        Allows user to choose to see detailed information on account.
        """
        try:
            accounts_df = self.account_service.df.copy()
            accounts_df = accounts_df.drop(columns=["Goal_Amount"])
            accounts_df["Note"] = accounts_df["Note"].fillna("")
            accounts_df.rename(
                columns={"Is_Goal": "Set as financial goal"}, inplace=True
            )

            print("\nCurrent accounts:")
            print(
                tabulate(accounts_df, headers="keys", tablefmt="psql", showindex=False)
            )

            while True:
                print("\nDo you want to see detailed information of an account?")
                print("1. Yes")
                print("2. Go back")

                choice = input("Enter your choice: ").strip()

                if choice == "1":
                    while True:
                        account_id = input("\nEnter account ID from the table above: ")
                        if (
                            account_id.isdigit()
                            and int(account_id) in accounts_df["Account_ID"].values
                        ):
                            self.display_single_account_details(int(account_id))
                            break
                        else:
                            print("\n⚠️  Invalid input. Please enter a valid option.")
                elif choice == "2":
                    return
                else:
                    print("\n⚠️  Invalid input. Please enter a valid option.\n")
        except EOFError:
            print("\n\nOperation was cancelled. Returning to previous menu...")
            return

    def display_single_account_details(self, account_id: int) -> None:
        """
        Displays transaction information for a specific account.
        """
        start_date, end_date = self.select_period()
        account_name = self.get_account_name(account_id)
        filtered_transactions = self.get_filtered_transactions_by_account(
            account_id, start_date, end_date
        )
        self.format_transactions(filtered_transactions)
        balance = filtered_transactions["Amount"].sum()
        self.print_transactions_for_single_account(
            account_name, filtered_transactions, start_date, end_date, balance
        )

    def display_income_overview(self) -> None:
        """
        Displays an overview of income transactions for a selected period.
        """
        try:
            start_date, end_date = self.select_period()
            income_transactions = self.get_filtered_transactions_by_type(
                "Income", start_date, end_date
            )
            income_transactions.reset_index(drop=True, inplace=True)
            income_transactions.index += 1

            income_transactions["Account"] = income_transactions["To_Account_ID"].map(
                self.account_service.df.set_index("Account_ID")["Name"]
            )

            self.format_transactions(income_transactions)

            if not income_transactions.empty:
                print(
                    f"\nIncome overview from {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}:"
                )
                print(
                    tabulate(
                        income_transactions[
                            ["Date", "Amount", "Category", "Account", "Note"]
                        ],
                        headers=[
                            "Item no.",
                            "Date",
                            "Amount",
                            "Category",
                            "Account",
                            "Note",
                        ],
                        tablefmt="psql",
                        showindex="always",
                    )
                )
                total_income = income_transactions["Amount"].sum()
                print(f"\nTotal income for the selected period: {total_income:.2f}")
                self.plot_category_distribution(income_transactions)
            else:
                print("\n⚠️  No income transactions found for the selected period.")
        except EOFError:
            print("\n\nOperation was cancelled. Returning to previous menu...")
            return

    def display_expense_overview(self) -> None:
        """
        Displays an overview of expense transactions for a selected period.
        """
        try:
            start_date, end_date = self.select_period()
            expense_transactions = self.get_filtered_transactions_by_type(
                "Expense", start_date, end_date
            )
            expense_transactions.reset_index(drop=True, inplace=True)
            expense_transactions.index += 1

            expense_transactions["Amount"] = expense_transactions["Amount"].abs()

            expense_transactions["Account"] = expense_transactions[
                "From_Account_ID"
            ].map(self.account_service.df.set_index("Account_ID")["Name"])

            self.format_transactions(expense_transactions)

            if not expense_transactions.empty:
                print(
                    f"\nExpense overview from {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}:"
                )
                print(
                    tabulate(
                        expense_transactions[
                            ["Date", "Amount", "Category", "Account", "Note"]
                        ],
                        headers=[
                            "Item no.",
                            "Date",
                            "Amount",
                            "Category",
                            "Account",
                            "Note",
                        ],
                        tablefmt="psql",
                        showindex="always",
                    )
                )
                total_expenses = expense_transactions["Amount"].sum()
                print(f"\nTotal expenses for the selected period: {total_expenses:.2f}")
                self.plot_category_distribution(expense_transactions)
            else:
                print("\n⚠️  No expense transactions found for the selected period.")
        except EOFError:
            print("\n\nOperation was cancelled. Returning to previous menu...")
            return

    def display_transfer_overview(self) -> None:
        """
        Displays all transfers between accounts during a selected period.
        """
        try:
            start_date, end_date = self.select_period()
            transfer_transactions = self.get_filtered_transactions_by_category(
                "Transfer", start_date, end_date
            )
            transfer_transactions.reset_index(drop=True, inplace=True)
            transfer_transactions.index += 1

            self.format_transactions(transfer_transactions)

            if not transfer_transactions.empty:
                print(
                    f"\nTransfer overview from {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}:"
                )
                print(
                    tabulate(
                        transfer_transactions[
                            ["Date", "Amount", "From_Account", "To_Account", "Note"]
                        ],
                        headers=[
                            "Item no.",
                            "Date",
                            "Amount",
                            "From Account",
                            "To Account",
                            "Note",
                        ],
                        tablefmt="psql",
                        showindex="always",
                    )
                )
                total_transfers = transfer_transactions[
                    transfer_transactions["Amount"] > 0
                ]["Amount"].sum()
                print(
                    f"\nTotal transfers for the selected period: {total_transfers:.2f}"
                )
            else:
                print("\n⚠️  No transfer transactions found for the selected period.")
        except EOFError:
            print("\n\nOperation was cancelled. Returning to previous menu...")
            return

    def display_category_overview(self) -> None:
        """
        Displays transactions for a specific category during a specified period.
        """

        try:
            while True:
                print("\nWhich categories would you like to review?")
                print("1. Income")
                print("2. Expense")
                print("3. Go back")

                choice = input("Enter your choice: ").strip()

                if choice == "1":
                    self.get_categories_by_type("Income")
                elif choice == "2":
                    self.get_categories_by_type("Expense")
                elif choice == "3":
                    return
                else:
                    print("\n⚠️  Invalid input. Please enter a valid option.\n")
        except EOFError:
            print("\n\nOperation was cancelled. Returning to previous menu...")
            return

    def display_balance_sheet_overview(self) -> None:
        """
        Displays total balance sheet for the selected period.
        """
        try:
            start_date, end_date = self.select_period()

            income_transactions = self.get_filtered_transactions_by_type(
                "Income", start_date, end_date
            )
            expense_transactions = self.get_filtered_transactions_by_type(
                "Expense", start_date, end_date
            )

            total_income = income_transactions["Amount"].sum()
            total_expenses = expense_transactions["Amount"].sum()

            total_balance = total_income + total_expenses

            print(
                f"\nBalance Sheet Overview from {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}:"
            )
            print(f"Total Income: {total_income:.2f}")
            print(f"Total Expenses: {total_expenses:.2f}")
            print(f"Total Balance: {total_balance:.2f}")

            all_transactions = pd.concat(
                [income_transactions, expense_transactions], ignore_index=True
            )
            all_transactions.sort_values(by="Date", inplace=True)
            all_transactions.reset_index(drop=True, inplace=True)
            all_transactions.index += 1

            self.format_transactions(all_transactions)

            if not all_transactions.empty:
                print(
                    tabulate(
                        all_transactions[
                            ["Date", "Type", "Amount", "Category", "Note"]
                        ],
                        headers=[
                            "Item no.",
                            "Date",
                            "Type",
                            "Amount",
                            "Category",
                            "Note",
                        ],
                        tablefmt="psql",
                        showindex="always",
                    )
                )
            else:
                print("\n⚠️  No transactions found for the selected period.")

        except EOFError:
            print("\n\nOperation was cancelled. Returning to previous menu...")
            return

    # Helper methods - most-commonly used:

    def select_period(self) -> tuple:
        """
        Allows the user to select a period for the overview.
        """
        today = datetime.today()

        while True:
            print("\nSelect the period for your overview:")
            print("1. This day")
            print("2. This week")
            print("3. This month")
            print("4. This year")
            print("5. Custom date")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                return today.date(), today.date()
            elif choice == "2":
                start_of_week = today - timedelta(days=today.weekday())
                return start_of_week.date(), today.date()
            elif choice == "3":
                start_of_month = today.replace(day=1)
                return start_of_month.date(), today.date()
            elif choice == "4":
                start_of_year = today.replace(month=1, day=1)
                return start_of_year.date(), today.date()
            elif choice == "5":
                start_date = self.convert_date(
                    input("\nEnter the start date (dd-mm-yyyy): ").strip()
                )
                end_date = self.convert_date(
                    input("Enter the end date (dd-mm-yyyy): ").strip()
                )
                try:
                    start_date = datetime.strptime(start_date, "%d-%m-%Y").date()
                    end_date = datetime.strptime(end_date, "%d-%m-%Y").date()
                    if start_date <= end_date:
                        return start_date, end_date
                    else:
                        print("\n⚠️  Start date must be before end date.")
                except ValueError:
                    print("\n⚠️  Invalid date format. Please use dd-mm-yyyy.")
            else:
                print("\n⚠️  Invalid choice. Please select a valid option.")

    def convert_date(self, date_str: str) -> str:
        """
        Converts date strings with different separators to the same format (DD-MM-YYYY)
        """
        for sep in ["/", ".", " "]:
            if sep in date_str:
                date_str = date_str.replace(sep, "-")
        return date_str

    def format_transactions(self, transactions_df: pd.DataFrame) -> None:
        """
        Formats the transactions DataFrame by handling empty notes and account cells.
        """
        transactions_df["Note"] = transactions_df["Note"].fillna("")
        transactions_df["From_Account"] = transactions_df["From_Account"].fillna("")
        transactions_df["To_Account"] = transactions_df["To_Account"].fillna("")

    # Helper methods - account-overview specific:

    def get_account_name(self, account_id: int) -> str:
        """
        Retrieves the account name for a given account ID.
        """
        return self.account_service.df.loc[
            self.account_service.df["Account_ID"] == account_id, "Name"
        ].values[0]

    def print_transactions_for_single_account(
        self,
        account_name: str,
        transactions_df: pd.DataFrame,
        start_date: datetime.date,
        end_date: datetime.date,
        balance: float,
    ) -> None:
        """
        Prints the transactions for a specific account and date range.
        """
        if not transactions_df.empty:
            transactions_df.insert(0, "Item No.", range(1, len(transactions_df) + 1))
            print(
                f"\nTransactions for '{account_name}' account from {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}:"
            )
            print(
                tabulate(
                    transactions_df[
                        ["Item No.", "Type", "Date", "Amount", "Category", "Note"]
                    ],
                    headers="keys",
                    tablefmt="psql",
                    showindex=False,
                )
            )
            print(f"\nAccount balance for the period: {balance:.2f}")
        else:
            print("\n⚠️  No transactions found for the selected period.")

    # Helper methods - category-overview specific:
    def get_categories_by_type(self, category_type: str) -> None:
        """
        Displays categories of a specific type and allows the user to select one to view transactions.
        """
        categories = self.category_service.categories[category_type]

        self.display_categories(category_type)

        while True:
            category_id = input(
                "\nEnter category ID to view detailed transactions: "
            ).strip()
            if category_id.isdigit() and category_id in categories:
                start_date, end_date = self.select_period()
                self.display_transactions_for_category(
                    category_type, category_id, start_date, end_date
                )
                break
            else:
                print("\n⚠️  Invalid input. Please enter a valid category ID.\n")

    def display_transactions_for_category(
        self,
        category_type: str,
        category_id: str,
        start_date: datetime.date,
        end_date: datetime.date,
    ) -> None:
        """
        Displays transactions for a specific category and date range.
        """

        category_name = self.category_service.categories[category_type][category_id]
        transactions_df = self.get_filtered_transactions_by_category(
            category_name, start_date, end_date
        )
        transactions_df.reset_index(drop=True, inplace=True)
        transactions_df.index += 1

        self.format_transactions(transactions_df)

        if not transactions_df.empty:
            print(
                f"\n{category_type} transactions for '{category_name}' category from {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}:"
            )
            print(
                tabulate(
                    transactions_df[["Date", "Amount", "Note"]],
                    headers=["Item no.", "Date", "Amount", "Note"],
                    tablefmt="psql",
                    showindex="always",
                )
            )
            total_amount = transactions_df["Amount"].sum()
            print(
                f"\nTotal {category_type.lower()} for the selected period: {total_amount:.2f}"
            )
        else:
            print(
                f"\n⚠️  No {category_type.lower()} transactions found for the selected period."
            )

    def display_categories(self, category_type) -> None:
        """
        Helper method that displays categories of a specific type.
        """
        print(f"\nAvailable {category_type} categories:")

        filtered_categories = {
            id: name
            for id, name in self.category_service.categories[category_type].items()
            if id != "0"
        }

        categories = [[id, name] for id, name in filtered_categories.items()]

        print(tabulate(categories, headers=["ID", "Name"], tablefmt="grid"))

    # Helper methods - get filtered transactions:

    def get_filtered_transactions_by_account(
        self, account_id: int, start_date: datetime.date, end_date: datetime.date
    ) -> pd.DataFrame:
        """
        Filters transactions for a specific account and date range.
        """
        transactions_df = self.transaction_service.df.copy()
        transactions_df["Date"] = pd.to_datetime(
            transactions_df["Date"], format="%d-%m-%Y"
        ).dt.date

        return transactions_df[
            (
                (transactions_df["From_Account_ID"] == account_id)
                | (transactions_df["To_Account_ID"] == account_id)
            )
            & (transactions_df["Date"] >= start_date)
            & (transactions_df["Date"] <= end_date)
        ]

    def get_filtered_transactions_by_category(
        self, category_name: str, start_date: datetime.date, end_date: datetime.date
    ) -> pd.DataFrame:
        """
        Filters transactions for a specific category and date range.
        """
        transactions_df = self.transaction_service.df.copy()
        transactions_df["Date"] = pd.to_datetime(
            transactions_df["Date"], format="%d-%m-%Y"
        ).dt.date

        return transactions_df[
            (transactions_df["Category"].str.lower() == category_name.lower())
            & (transactions_df["Date"] >= start_date)
            & (transactions_df["Date"] <= end_date)
        ]

    def get_filtered_transactions_by_type(
        self, transaction_type: str, start_date: datetime.date, end_date: datetime.date
    ) -> pd.DataFrame:
        """
        Filters transactions for a specific transaction type and date range.
        """
        transactions_df = self.transaction_service.df.copy()
        transactions_df["Date"] = pd.to_datetime(
            transactions_df["Date"], format="%d-%m-%Y"
        ).dt.date

        return transactions_df[
            (transactions_df["Type"].str.lower() == transaction_type.lower())
            & (transactions_df["Date"] >= start_date)
            & (transactions_df["Date"] <= end_date)
        ]

    # Helper methods - for representation and formatting

    def plot_category_distribution(self, transactions_df: pd.DataFrame) -> None:
        """
        Plots the distribution of transaction categories as a pie chart.
        """

        category_sum = transactions_df.groupby("Category")["Amount"].sum()
        category_sum = category_sum.sort_values()

        plt.simple_bar(category_sum.index, category_sum, title="Category Distribution")
        plt.show()
