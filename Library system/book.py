class Book:
    def __init__(
        self,
        book_id,
        title,
        author,
        description,
        genre=None,
        keywords=None
    ):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.description = description
        self.genre = genre if genre is not None else []
        self.keywords = keywords if keywords is not None else []
        self.is_available = True
        self.borrow_count = 0