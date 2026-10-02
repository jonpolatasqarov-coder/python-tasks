class Book:
    def __init__(self, book_id, title, author, description):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.description = description
        self.is_available = True
        self.borrow_count = 0
        