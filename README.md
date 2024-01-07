# Personal Finance Planning and Tracking Application

## Description
This Personal Finance Planning and Tracking Application is designed to assist the user in managing their finances more effectively. The goal was to create an easy-to-use tool that offers quick insights into user's financial habits, helps them notice certain patterns and act upon them.

The application is built in Python and provides features like transaction recording, financial overview, category and account  customization, and financial goal setting and tracking.

## Why is the program useful?
- **Detailed transaction management:** users can record transactions like income, expenses and transfers. Over time, this adds up to categorized spending and earning history that helps the user notice certain patterns.
- **Data-driven insights:** the program offers financial reporting based on accounts, categories and time periods. This allows the user to see the bigger picture when it comes to their financial situation and helps them make informed decisions.
- **Help in saving:** the application is meant to help the user to save money. From dedicated accounts for taxes to the feature that allows to set certain financial goals and track the progress - it should help the user be aware of the budget they have for spending and the funds they should set aside.
- **Accessibility and convenience:** As a locally run application, it provides easy access and privacy, allowing users to manage their finances anytime without the need for internet connectivity or third-party applications. 

## Usage
The program was designed to be as easy to navigate as possible, given that it's run in the terminal. Users can choose all actions with integer inputs, which are validated by the program.

If the user wishes to exit an operation without completing it, they can terminate with ctrl+d to get back to previous menu.

Before beginning to use the program, users should add income and expense categories to be able to classify their transactions.

## Program structure

### Main function
**Files:** main.py
- Serves as the entry point of the application. It initiates the application and manages the main flow.

### Tool Manager class
**Files:** tool_manager.py

- Acts as the central coordinator for various modes of the application

### Mode classes
**Files:** transactions_mode.py, overview_mode.py, financial_goals_mode.py, settings_mode.py
- TransactionsMode: Handles all transaction-related operations including adding income, expenses, and transfers.
- OverviewMode: Provides an overview of financial data such as account summaries, income, expenses, and category distributions.
- SettingsMode: Manages application settings including managing categories and accounts, and setting financial goals.
- FinancialGoalsMode: Allows users to set and track financial goals, displaying progress and related transactions.

### Service classes
**Files:** transactions.py, categories.py, accounts.py

- TransactionService: Manages transactions data, responsible for adding, editing, and retrieving transaction details.
- AccountService: Handles account-related data including creating, editing, and deleting accounts.
- CategoryService: Manages income and expense categories, allowing for addition, modification, and deletion.

### Data classes:
**Files:** transactions.py, categories.py, accounts.py
- Transaction, Account, Category Classes: Represent the data models for transactions, accounts, and categories, respectively. Each class includes methods for converting instances to dictionaries for data handling.


## Planned application improvements
- **More detailed period-based reports:** initially, the program was planned with more detailed period-based reports. For example, allow user to set a spending limit for a period and display warnings about being close to the limit. Also, display the percentage difference between income and expenses.
- **Presets:** a feature driven by personal need. The program should have a feature allowing the user to set transactions that occur regularly and add them automatically. An example:
  - User knows that every month, they need to pay x for mortgage, y for bills and z for other services. They can add such a preset and add it quickly, or even set it to be added automatically, if possible.
- **Income allocation calculator:** a feature that allows the user to quickly calculate how much money they should allocate to certain accounts based on their goals. For example, if they have a goal to allocate 20% of their income for investment, or if they know that they need to allocate a certain amount of their freelance income for taxes. Ideally, the mode would also have a feature to immediately do the transaction after calculation is done.
- **Graphical user interface:** It's planned to use Tkinter or other similar framework to build a graphical user interface.

## Planned code improvements
- Write unit tests for each class to ensure proper operations
- Refactor the code to reduce redundancies

