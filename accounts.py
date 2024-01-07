import pandas as pd

ACCOUNTS_FILE = "data/accounts.csv"


class Account:
    """
    Represents one financial account.
    """

    def __init__(
        self,
        account_id: int,
        name: str,
        balance: float,
        is_goal: str = "No",
        goal_amount: float = "",
        note: str = "",
    ) -> None:
        """
        Initializes a new account.
        """
        self.account_id = account_id
        self.name = name
        self.balance = balance
        self.is_goal = is_goal
        self.goal_amount = goal_amount
        self.note = note

    def convert_to_dict(self) -> dict:
        """
        Converts the account instance to a dictionary suitable for DataFrame.
        """
        return {
            "Account_ID": self.account_id,
            "Name": self.name,
            "Balance": self.balance,
            "Is_Goal": self.is_goal,
            "Goal_Amount": self.goal_amount,
            "Note": self.note,
        }


class AccountService:
    """
    Manages accounts and their manipulation in a CSV file.
    """

    def __init__(self) -> None:
        """
        Initializes the class with a path to the CSV file.
        """
        self.filepath = ACCOUNTS_FILE
        self.columns = [
            "Account_ID",
            "Name",
            "Balance",
            "Is_Goal",
            "Goal_Amount",
            "Note",
        ]
        self.load_or_initialize_accounts_file()

    def load_or_initialize_accounts_file(self) -> None:
        """
        Loads the accounts CSV file or creates a new one if it doesn't exist.
        """
        try:
            self.df = pd.read_csv(self.filepath)
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=self.columns)
            main_account = Account(
                account_id=self.get_new_account_id(), name="Main", balance=0.0
            )
            self.df = pd.concat(
                [self.df, pd.DataFrame([main_account.convert_to_dict()])],
                ignore_index=True,
            )
            self.df.to_csv(self.filepath, index=False)

    def save_accounts_to_file(self) -> None:
        """
        Saves the DataFrame of accounts to the CSV file.
        """
        self.df.to_csv(self.filepath, index=False)

    def get_new_account_id(self) -> int:
        """
        Generates a new account ID.
        """
        if self.df.empty:
            return 1
        else:
            return self.df["Account_ID"].max() + 1

    def add_account(
        self,
        name: str,
        balance: float,
        is_goal: str = "No",
        goal_amount: float = "",
        note: str = "",
    ) -> Account:
        """
        Adds a new account with a unique ID.
        """
        account = Account(
            account_id=self.get_new_account_id(),
            name=name,
            balance=balance,
            is_goal=is_goal,
            goal_amount=goal_amount,
            note=note,
        )
        new_account_df = pd.DataFrame([account.convert_to_dict()])
        self.df = pd.concat([self.df, new_account_df], ignore_index=True)
        self.save_accounts_to_file()
        return account

    def edit_account_name(self, account_id: int, new_name: str) -> None:
        """
        Edits an existing account's name.
        """
        self.df.loc[self.df["Account_ID"] == account_id, "Name"] = new_name
        self.save_accounts_to_file()

    def delete_account(self, account_id: int) -> None:
        """
        Deletes an account and transfers its balance to the Main account.
        """
        account_row = self.df[self.df["Account_ID"] == account_id]
        if not account_row.empty:
            if account_row.iloc[0]["Name"].lower() == "main":
                print("The Main account cannot be deleted.")
                return

            balance_to_transfer = account_row.iloc[0]["Balance"]

            self.df = self.df[self.df["Account_ID"] != account_id]

            main_account_index = self.df[self.df["Name"].str.lower() == "main"].index
            if not main_account_index.empty:
                self.df.at[main_account_index[0], "Balance"] += balance_to_transfer
            else:
                print("Main account not found. Balance transfer failed.")
            self.save_accounts_to_file()
        else:
            print(f"Account with ID '{account_id}' was not found.")

    def get_account_balance(self, account_name: str) -> float:
        """
        Retrieves the balance of an account by its name.
        Returns the balance if the account is found, otherwise None.
        """
        account_row = self.df[self.df["Name"].str.lower() == account_name.lower()]
        if not account_row.empty:
            return account_row.iloc[0]["Balance"]
        else:
            print(f"Account with name '{account_name}' was not found.")
            return None

    def update_account_balance(self, account_name: str, amount: float) -> None:
        """
        Updates the balance of an account by a given amount.
        If the amount is negative, it will deduct from the balance.
        """
        account_index = self.df[
            self.df["Name"].str.lower() == account_name.lower()
        ].index
        if not account_index.empty:
            self.df.at[account_index[0], "Balance"] += amount
            self.save_accounts_to_file()
        else:
            print(f"Account with name '{account_name}' was not found.")

    def check_if_balance_negative(self, account_name: str, amount: float) -> bool:
        """
        Checks if the account balance after a transaction would be negative.
        Returns True if the balance would be negative, False otherwise.
        """
        account_index = self.df[
            self.df["Name"].str.lower() == account_name.lower()
        ].index
        if not account_index.empty:
            current_balance = self.df.at[account_index[0], "Balance"]
            return current_balance + amount < 0
        else:
            print(f"Account with name '{account_name}' was not found.")
            return False

    def get_account_id_by_name(self, account_name: str) -> int:
        """
        Retrieves the account ID by its name.
        Returns the account ID if the account is found, otherwise None.
        """
        account_row = self.df[self.df["Name"].str.lower() == account_name.lower()]
        if not account_row.empty:
            return int(account_row.iloc[0]["Account_ID"])
        else:
            print(f"Account with name '{account_name}' was not found.")
            return None
