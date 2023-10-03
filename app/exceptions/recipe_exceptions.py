class InvalidRecipeIDException(Exception):
    def __init__(self, id):
        self.id = id
        super().__init__(f"Recipe ID '{id}' is invalid")

class RecipeNotFoundException(Exception):
    def __init__(self, id):
        self.id = id
        super().__init__(f"Recipe with id '{id}' not found")

class RecipeAlreadyExistsException(Exception):
    def __init__(self, name):
        self.name = name
        super().__init__(f"Recipe with the given name '{name}' already exists")

class InvalidRecipeOperationException(Exception):
    def __init__(self, id):
        self.id = id
        super().__init__(f"Operation on recipe with '{id}' is invalid")