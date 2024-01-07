from art import text2art
from transactions import TransactionService
from accounts import AccountService
from categories import CategoryService
from transactions_mode import TransactionsMode
from overview_mode import OverviewMode
from settings_mode import SettingsMode
from financials_goals_mode import FinancialGoalsMode

class ToolManager:
    """Encapsulates the main logic of the tool."""

    def __init__(self):
        """
        Initializes the ToolManager class.
        """
        transaction_service = TransactionService()
        category_service = CategoryService()
        account_service = AccountService()
        self.transactions_mode = TransactionsMode(transaction_service, category_service, account_service)
        self.overview_mode = OverviewMode(transaction_service, category_service, account_service)
        self.settings_mode = SettingsMode(transaction_service, category_service, account_service)
        self.financial_goals_mode = FinancialGoalsMode(transaction_service, category_service, account_service)

    def handle_navigation_of_main_menu(self) -> None:
        """
        Handles user choice for navigation.
        """
        while True:
            self.display_main_menu()

            choice = self.get_user_choice()

            goodbye_art = text2art("Goodbye!", font="small")

            if choice == 1:
                self.transactions_mode.display_transactions_mode_menu()
            elif choice == 2:
                self.overview_mode.display_overview_mode_menu()
            elif choice == 3:
                self.financial_goals_mode.display_financial_goals_mode_menu()
            elif choice == 4:
                self.settings_mode.display_settings_mode_menu()
            elif choice == 5:
                print("\nExiting the program...")
                print(goodbye_art)
                break
            else:
                print("\n⚠️Invalid input. Please try again.\n")

    def display_main_menu(self) -> None:
        """
        Displays the main menu choices for the user.
        """
        print("\nPlease select one of the following options:")
        print("1. Transactions")
        print("2. Overview")
        print("3. Financial Goals") 
        print("4. Settings") 
        print("5. Exit")

    def get_user_choice(self) -> int:
        """
        Gets and validates user choice for the main menu. 
        """
        while True:
            try:
                choice = int(input("Enter your choice: "))
                if choice in [1, 2, 3, 4, 5, 6]:
                    return choice
                else:
                    print("Invalid input. Please choose one of the indicated modes.")
            except ValueError:
                print("Please enter a valid number.")

