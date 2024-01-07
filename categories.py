import json

CATEGORIES_FILE = "data/categories.json"


class Category:
    """
    Represents one income or expense category.
    """

    def __init__(
        self, category_id: int, category_name: str, category_type: str
    ) -> None:
        """
        Initializes a new category.
        """
        self.category_id = category_id
        self.category_name = category_name
        self.category_type = category_type

    def convert_to_dict(self) -> dict:
        """
        Converts the category instance to a dictionary.
        """
        return {
            "Category_ID": self.category_id,
            "Category_Name": self.category_name,
            "Category_Type": self.category_type,
        }


class CategoryService:
    """
    Manages categories and their manipulation in a JSON file.
    """

    def __init__(self) -> None:
        """
        Initializes the class with a path to the JSON file.
        """
        self.filepath = CATEGORIES_FILE
        self.categories = {"Expense": {}, "Income": {}}
        self.load_or_initialize_categories_file()

    def load_or_initialize_categories_file(self) -> None:
        """
        Loads or initializes categories JSON file.
        """
        try:
            with open(CATEGORIES_FILE, "r") as file:
                self.categories = json.load(file)
        except FileNotFoundError:
            self.categories = {
                "Expense": {"0": "Uncategorized"},
                "Income": {"0": "Uncategorized"},
            }
            self.save_categories_to_file()

    def save_categories_to_file(self) -> None:
        """
        Saves the categories to the JSON file.
        """
        with open(CATEGORIES_FILE, "w") as file:
            json.dump(self.categories, file, indent=4)

    def get_new_category_id(self, category_type: str) -> int:
        """
        Generates a new category ID.
        """
        if self.categories[category_type]:
            return max(map(int, self.categories[category_type].keys())) + 1
        return 1

    def add_category(self, category_type: str, category_name: str) -> None:
        """
        Adds a new category with a unique ID.
        """
        new_id = self.get_new_category_id(category_type)
        category = Category(new_id, category_name, category_type)
        self.categories[category_type][str(new_id)] = category_name
        self.save_categories_to_file()
        return category

    def edit_category(
        self, category_type: str, category_id: int, new_category_name: str
    ) -> None:
        """
        Edits an existing category.
        """
        if str(category_id) in self.categories[category_type]:
            self.categories[category_type][str(category_id)] = new_category_name
            self.save_categories_to_file()

    def delete_category(self, category_type: str, category_id: int) -> None:
        """
        Deletes a category.
        """
        if str(category_id) in self.categories[category_type]:
            del self.categories[category_type][str(category_id)]
            self.save_categories_to_file()
