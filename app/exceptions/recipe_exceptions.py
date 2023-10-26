class InvalidRecipeIDException(Exception):
    def __init__(self, id):
        self.id = id
        super().__init__(f"Recipe ID '{id}' is invalid")

class RecipeNotFoundException(Exception):
    def __init__(self, id):
        self.id = id
        super().__init__(f"User with recipe id '{id}' not found")

class UnauthorisedRecipeModificationException(Exception):
    def __init__(self, recipe_name):
        self.recipe_name = recipe_name
        super().__init__(f"User is not authorised to modify/delete this recipe '{recipe_name}'")    