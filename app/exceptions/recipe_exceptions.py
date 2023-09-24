class InvalidRecipeIDException(Exception):
    def __init__(self, id):
        self.id = id
        super().__init__(f"Recipe ID '{id}' is invalid")

class RecipeNotFoundException(Exception):
    def __init__(self, id):
        self.id = id
        super().__init__(f"User with id '{id}' not found")