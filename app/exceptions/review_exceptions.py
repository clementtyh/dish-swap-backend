class InvalidReviewIDException(Exception):
    def __init__(self, id):
        self.id = id
        super().__init__(f"Review ID '{id}' is invalid")

class ReviewNotFoundException(Exception):
    def __init__(self, id):
        self.id = id
        super().__init__(f"User with review id '{id}' not found")

class UnauthorisedReviewModificationException(Exception):
    def __init__(self, review_id):
        self.review_id = review_id
        super().__init__(f"User is not authorised to modify/delete this review '{review_id}'")    
