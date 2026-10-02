import json
import logging
from book import Book
from user import User
from datetime import date, timedelta

logging.basicConfig(
    filename="library.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class Library:
    def __init__(self):
        self.books = []
        self.users = []

    def add_book(self, book):
        self.books.append(book)

    def add_user(self, user):
        self.users.append(user)

    def borrow_book(self, user, book):
        if not book.is_available:
            print("Book is not available.")
            return

        book.is_available = False
        book.borrow_count += 1
        user.borrowed_books.append(book)

        logging.info(
            f"User '{user.name}' borrowed book '{book.title}'."
        )

        due_date = date.today() + timedelta(days=14)
        user.borrow_dates[book.book_id] = due_date.isoformat()

        print(f"Book borrowed. Return by {due_date}.")

    def return_book(self, user, book):
        if book not in user.borrowed_books:
            print("This book was not borrowed by the user.")
            return

        book.is_available = True
        user.borrowed_books.remove(book)
        user.borrow_dates.pop(book.book_id, None)

        logging.info(
            f"User '{user.name}' returned book '{book.title}'."
        )

        print("Book returned successfully.")

    def extend_book(self, user, book):
        if book not in user.borrowed_books:
            print("This book was not borrowed by the user.")
            return

        current_due_date = date.fromisoformat(
            user.borrow_dates[book.book_id]
        )

        new_due_date = current_due_date + timedelta(days=7)
        user.borrow_dates[book.book_id] = new_due_date.isoformat()

        logging.info(
            f"User '{user.name}' extended book '{book.title}' "
            f"until {new_due_date}."
        )

        print(f"Book rental period extended to {new_due_date}.")

    def save_data(self):
        with open("books.json", "w", encoding="utf-8") as file:
            json.dump(
                [book.__dict__ for book in self.books],
                file,
                indent=4
            )

        users_data = []

        for user in self.users:
            users_data.append({
                "user_id": user.user_id,
                "name": user.name,
                "email": user.email,
                "borrowed_books": [
                    book.book_id for book in user.borrowed_books
                ],
                "borrow_dates": user.borrow_dates
            })

        with open("users.json", "w", encoding="utf-8") as file:
            json.dump(users_data, file, indent=4)

    def load_data(self):
        with open("books.json", "r", encoding="utf-8") as file:
            books_data = json.load(file)

        with open("users.json", "r", encoding="utf-8") as file:
            users_data = json.load(file)

        for data in books_data:
            book = Book(
                data["book_id"],
                data["title"],
                data["author"],
                data["description"]
            )

            book.is_available = data["is_available"]
            book.borrow_count = data["borrow_count"]

            self.books.append(book)

        for data in users_data:
            user = User(
                data["user_id"],
                data["name"],
                data["email"]
            )

            user.borrow_dates = {
                int(book_id): due_date
                for book_id, due_date in data.get("borrow_dates", {}).items()
            }

            for book_id in data.get("borrowed_books", []):
                for book in self.books:
                    if book.book_id == book_id:
                        user.borrowed_books.append(book)
                        break

            self.users.append(user)

    def check_overdue_books(self):
        today = date.today()
        overdue_found = False

        for user in self.users:
            for book in user.borrowed_books:
                due_date = date.fromisoformat(
                    user.borrow_dates[book.book_id]
                )

                if today > due_date:
                    overdue_found = True

                    print(f"\nEMAIL SENT TO: {user.email}")
                    print("Subject: Book return overdue")
                    print(
                        f"Message: {book.title} is overdue. "
                        f"Please return the book."
                    )

                    logging.warning(
                        f"Overdue email sent to {user.email} "
                        f"for book '{book.title}'."
                    )

        if not overdue_found:
            print("No overdue books.")

    def most_read_book(self):
        if not self.books:
            print("No books available.")
            return

        book = max(self.books, key=lambda book: book.borrow_count)

        print(
            f"Most read book: {book.title} "
            f"({book.borrow_count} borrows)"
        )


    def least_borrowed_book(self):
        if not self.books:
            print("No books available.")
            return

        book = min(self.books, key=lambda book: book.borrow_count)

        print(
            f"Least borrowed book: {book.title} "
            f"({book.borrow_count} borrows)"
        ) 