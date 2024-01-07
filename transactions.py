import pandas as pd

TRANSACTIONS_FILE = "data/transactions.csv"

class Transaction:
    """Represents one financial transaction."""

    def __init__(
        self,
        transaction_id: int,
        transaction_type: str,
        date: str,
        amount: float,
        category_name: str,
        from_account_id: int,
        from_account: str,
        to_account_id: int,
        to_account: str,
        note: str,
    ) -> None:
        """Initializes a new transaction"""
        self.transaction_id = transaction_id
        self.transaction_type = transaction_type
        self.date = date
        self.amount = amount
        self.category_name = category_name
        self.from_account_id = from_account_id
        self.from_account = from_account
        self.to_account_id = to_account_id
        self.to_account = to_account
        self.note = note

    def convert_to_dict(self) -> dict:
        """
        Converts the transaction instance to a dictionary suitable for DataFrame.
        """
        return {
            "Transaction_ID": self.transaction_id,
            "Type": self.transaction_type,
            "Date": self.date,
            "Amount": self.amount,
            "Category": self.category_name,
            "From_Account_ID": self.from_account_id,
            "From_Account": self.from_account,
            "To_Account_ID": self.to_account_id,
            "To_Account": self.to_account,
            "Note": self.note,
        }


class TransactionService:
    """
    Manages transactions and their manipulation in a CSV file.
    """
    def __init__(self) -> None:
        "Initializes the class with a path to the CSV file"
        self.filepath = TRANSACTIONS_FILE
        self.columns = [
            "Transaction_ID",
            "Type",
            "Date",
            "Amount",
            "Category",
            "From_Account_ID",
            "From_Account",
            "To_Account_ID",
            "To_Account",
            "Note",
        ]
        self.load_or_initialize_transactions_file()

    def load_or_initialize_transactions_file(self) -> None:
        """
        Loads the transactions CSV file or creates a new one if it doesn't exist
        """
        try:
            self.df = pd.read_csv(self.filepath)
            for col in ["From_Account_ID", "To_Account_ID"]:
                self.df[col] = pd.to_numeric(self.df[col], errors="coerce").astype("Int64")
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=self.columns)
            self.df.to_csv(self.filepath, index=False)

    def add_transaction(
        self,
        transaction_type: str,
        date: str,
        amount: float,
        from_account_id: int, 
        from_account: str,
        to_account_id: int,
        to_account: str,
        note: str,
        category_name: str = "Uncategorized"
    ) -> Transaction:
        """
        Adds a new transaction and saves it to the CSV file.
        """
        if not category_name:
            category_name = "Uncategorized"

        transaction = Transaction(
            transaction_id=self.get_next_transaction_id(),
            transaction_type=transaction_type,
            date=date,
            amount=amount,
            category_name=category_name,
            from_account_id=from_account_id,
            from_account=from_account,
            to_account_id=to_account_id,
            to_account=to_account,
            note=note,
        )
        new_transaction_df = pd.DataFrame([transaction.convert_to_dict()])
        self.df = pd.concat([self.df, new_transaction_df], ignore_index=True)
        self.sort_transactions()
        self.save_transaction_to_file()

    def sort_transactions(self) -> None:
        """
        Sorts the DataFrame by date with the newest transactions on top.
        """
        self.df["Date"] = pd.to_datetime(self.df["Date"], format="%d-%m-%Y")
        self.df.sort_values(by="Date", ascending=False, inplace=True)
        self.df["Date"] = self.df["Date"].dt.strftime("%d-%m-%Y")
        self.df.reset_index(drop=True, inplace=True)

    def save_transaction_to_file(self) -> None:
        """
        Saves the DataFrame of transactions to the CSV file.
        """
        self.df.to_csv(self.filepath, index=False)

    def get_next_transaction_id(self) -> int:
        """
        Gets the next available transaction ID.
        """
        if self.df.empty:
            return 1
        else:
            return self.df["Transaction_ID"].max() + 1
        
    def update_transactions_category(self, old_category_name: str, new_category_name: str) -> None:
        """
        Updates the category name for all transactions with the given old category name.
        """
        transactions_to_update = self.df["Category"] == old_category_name
        self.df.loc[transactions_to_update, "Category"] = new_category_name
        self.save_transaction_to_file()

    def uncategorize_transactions(self, category_name: str) -> None:
        """
        Sets the category to 'Uncategorized' for all transactions with the given category name.
        """
        transactions_to_uncategorize = self.df["Category"] == category_name
        self.df.loc[transactions_to_uncategorize, "Category"] = "Uncategorized"
        self.save_transaction_to_file()

    def update_account_name_in_transactions(self, account_id: int, new_name: str) -> None:
        """
        Updates the account name in transactions after an account name change.
        """
        self.df.loc[self.df["From_Account_ID"] == account_id, "From_Account"] = new_name
        self.df.loc[self.df["To_Account_ID"] == account_id, "To_Account"] = new_name
        self.save_transaction_to_file()