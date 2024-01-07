from tool_manager import ToolManager
from rich.console import Console
from art import text2art


def main():
    """
    Acts like an entry point for the entire application.
    """
    welcome_art = text2art("Welcome", font="small")
    print(welcome_art)

    print_welcome_message_and_instructions()

    manager = ToolManager()
    manager.handle_navigation_of_main_menu()


def print_welcome_message_and_instructions() -> None:
    """
    Prints out short welcome message.
    Informs user how to use the app.
    """
    console = Console()
    console.rule()
    print("This is your personal finance planning and tracking app.")
    print("Navigate the application using integer inputs.")
    print(
        "If you ever need to exit an operation without completing it, press ctrl + d."
    )
    console.rule()

if __name__ == "__main__":
    main()
