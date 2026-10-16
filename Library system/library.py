import json
import logging
from pathlib import Path
from datetime import date, timedelta

from book import Book
from user import User


logging.basicConfig(
    filename="library.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class Library:
    def __init__(self):
        self.books = []
        self.users = []

    # -------------------- ADD --------------------

    def add_book(self, book):
        self.books.append(book)



    def add_user(self, user):
        if not user.name.strip():
            print("Error: Name cannot be empty.")
            return False

        if not user.email.strip():
            print("Error: Email cannot be empty.")
            return False

        for existing_user in self.users:
            if existing_user.email.strip().casefold() == user.email.strip().casefold():
                print("Error: This email is already registered.")
                return False

        if self.find_user(user.user_id):
            print("Error: This user ID already exists.")
            return False

        self.users.append(user)
        logging.info("User '%s' added successfully.", user.name)
        return True



    def find_book(self, book_id):
        return next(
            (book for book in self.books
             if book.book_id == book_id),
            None
        )

    def find_user(self, user_id):
        return next(
            (user for user in self.users
             if user.user_id == user_id),
            None
        )

    # -------------------- BORROW --------------------

    def borrow_book(self, user, book, days=14):
        if user not in self.users:
            print("User not found.")
            return False

        if book not in self.books:
            print("Book not found.")
            return False

        if not book.is_available:
            print("Book is not available.")
            logging.warning(
                "User '%s' tried to borrow unavailable book '%s'.",
                user.name,
                book.title
            )
            return False

        if not isinstance(days, int) or not 1 <= days <= 14:
            print("Rental period must be between 1 and 14 days.")
            return False

        borrow_date = date.today()
        due_date = borrow_date + timedelta(days=days)

        book.is_available = False
        book.borrow_count += 1
        user.borrowed_books.append(book)

        user.borrow_start_dates[book.book_id] = (
            borrow_date.isoformat()
        )
        user.borrow_dates[book.book_id] = due_date.isoformat()

        logging.info(
            "User '%s' borrowed '%s' for %s days. Due: %s.",
            user.name,
            book.title,
            days,
            due_date.isoformat()
        )

        print(f"Book borrowed for {days} day(s).")
        print(f"Borrow date: {borrow_date.isoformat()}")
        print(f"Return by: {due_date.isoformat()}")

        return True

    # -------------------- RETURN --------------------

    def return_book(self, user, book):
        if user not in self.users:
            print("User not found.")
            return False

        if book not in user.borrowed_books:
            print("This book was not borrowed by the user.")
            return False

        return_date = date.today().isoformat()

        user.borrowed_books.remove(book)
        book.is_available = True

        user.borrow_dates.pop(book.book_id, None)
        user.borrow_start_dates.pop(book.book_id, None)

        logging.info(
            "User '%s' returned '%s' on %s.",
            user.name,
            book.title,
            return_date
        )

        print(f"Book '{book.title}' returned successfully.")
        return True

    # -------------------- EXTEND --------------------

    def extend_book(self, user, book, days):
        if user not in self.users:
            print("User not found.")
            return False

        if book not in user.borrowed_books:
            print("This book was not borrowed by the user.")
            return False

        if not isinstance(days, int) or days < 1:
            print("Extension must be at least 1 day.")
            return False

        start_text = user.borrow_start_dates.get(book.book_id)
        due_text = user.borrow_dates.get(book.book_id)

        if not start_text or not due_text:
            print("Rental date information is missing.")
            return False

        try:
            start_date = date.fromisoformat(start_text)
            current_due_date = date.fromisoformat(due_text)
        except ValueError:
            print("Rental date information is invalid.")
            logging.error(
                "Invalid rental dates for user '%s', book '%s'.",
                user.name,
                book.title
            )
            return False

        today = date.today()

        if current_due_date < today:
            print("Overdue books cannot be extended.")
            return False

        current_total_days = (current_due_date - start_date).days
        remaining_days = 14 - current_total_days

        if remaining_days <= 0:
            print("The maximum rental period of 14 days has been reached.")
            return False

        if days > remaining_days:
            print(f"You can extend this book by 1 to {remaining_days} days.")
            return False

        new_due_date = current_due_date + timedelta(days=days)
        user.borrow_dates[book.book_id] = new_due_date.isoformat()

        logging.info(
            "User '%s' extended '%s' by %s days. New due date: %s.",
            user.name,
            book.title,
            days,
            new_due_date.isoformat()
        )

        print(f"Book rental period extended by {days} day(s).")
        print(f"New return date: {new_due_date.isoformat()}")

        return True

    # -------------------- JSON HELPERS --------------------

    def _read_json_file(self, filename):
        path = Path(filename)

        try:
            with path.open("r", encoding="utf-8") as file:
                content = file.read().strip()

            if not content:
                logging.warning("%s is empty. Using an empty list.", filename)
                return []

            data = json.loads(content)

            if not isinstance(data, list):
                raise ValueError(
                    f"{filename} must contain a JSON list."
                )

            return data

        except FileNotFoundError:
            logging.warning(
                "%s not found. Using an empty list.", filename
            )
            return []

        except json.JSONDecodeError as error:
            logging.error("Invalid JSON in %s: %s", filename, error)
            raise ValueError(
                f"{filename} contains invalid JSON. "
                "Restore it from a backup or correct the file."
            ) from error

    # -------------------- SAVE DATA --------------------

    def save_data(self):
        books_data = [book.__dict__ for book in self.books]

        users_data = []

        for user in self.users:
            users_data.append({
                "user_id": user.user_id,
                "name": user.name,
                "email": user.email,
                "borrowed_books": [
                    book.book_id for book in user.borrowed_books
                ],
                "borrow_dates": user.borrow_dates,
                "borrow_start_dates": user.borrow_start_dates
            })

        try:
            with open("books.json", "w", encoding="utf-8") as file:
                json.dump(books_data, file, indent=4, ensure_ascii=False)

            with open("users.json", "w", encoding="utf-8") as file:
                json.dump(users_data, file, indent=4, ensure_ascii=False)

            logging.info("Library data saved successfully.")

        except OSError as error:
            logging.error("Could not save library data: %s", error)
            print(f"Error saving data: {error}")

    # -------------------- LOAD DATA --------------------

    def load_data(self):
        books_data = self._read_json_file("books.json")
        users_data = self._read_json_file("users.json")

        loaded_books = []
        loaded_users = []
        books_by_id = {}

        try:
            for data in books_data:

                book = Book(
                    data["book_id"],
                    data["title"],
                    data["author"],
                    data.get("description", ""),
                    genre=data.get("genre", []),
                    keywords=data.get("keywords", [])
                )

                book.is_available = data.get("is_available", True)
                book.borrow_count = data.get("borrow_count", 0)

                loaded_books.append(book)
                books_by_id[book.book_id] = book

            for data in users_data:
                user = User(
                    data["user_id"],
                    data["name"],
                    data["email"]
                )

                user.borrow_dates = {
                    int(book_id): due_date
                    for book_id, due_date
                    in data.get("borrow_dates", {}).items()
                }

                user.borrow_start_dates = {
                    int(book_id): start_date
                    for book_id, start_date
                    in data.get("borrow_start_dates", {}).items()
                }

                for book_id in data.get("borrowed_books", []):
                    book = books_by_id.get(book_id)

                    if book is None:
                        logging.warning(
                            "User '%s' references missing book ID %s.",
                            user.name,
                            book_id
                        )
                        continue

                    user.borrowed_books.append(book)

                loaded_users.append(user)

        except (KeyError, TypeError, ValueError) as error:
            logging.error("Invalid library data: %s", error)
            raise ValueError(
                "The JSON data has missing or invalid fields. "
                "Restore the files from a backup or correct them."
            ) from error

        self.books = loaded_books
        self.users = loaded_users

        # Ma'lumotlar orasidagi bandlikni tekshirish.
        borrowed_book_ids = {
            book.book_id
            for user in self.users
            for book in user.borrowed_books
        }

        for book in self.books:
            if book.book_id in borrowed_book_ids:
                book.is_available = False
            elif not any(
                book.book_id in user.borrow_dates
                for user in self.users
            ):
                # Faqat biror userga biriktirilmagan kitoblar
                # bo'yicha ziddiyatni log qilamiz.
                if not book.is_available:
                    logging.warning(
                        "Book '%s' is marked unavailable but "
                        "no user has borrowed it.",
                        book.title
                    )

        logging.info(
            "Loaded %s books and %s users.",
            len(self.books),
            len(self.users)
        )

    # -------------------- OVERDUE BOOKS --------------------

    def check_overdue_books(self):
        today = date.today()
        overdue_books = []

        for user in self.users:
            for book in user.borrowed_books:
                due_date_text = user.borrow_dates.get(book.book_id)

                if not due_date_text:
                    continue

                try:
                    due_date = date.fromisoformat(due_date_text)
                except ValueError:
                    logging.error(
                        "Invalid due date for user '%s', book '%s'.",
                        user.name,
                        book.title
                    )
                    continue

                if due_date < today:
                    overdue_days = (today - due_date).days
                    overdue_books.append(
                        (user, book, due_date, overdue_days)
                    )

        if not overdue_books:
            print("\nNo overdue books found.")
            return

        print("\n" + "=" * 100)
        print("OVERDUE BOOKS".center(100))
        print("=" * 100)

        print(
            f"{'USER':<20}"
            f"{'BOOK TITLE':<30}"
            f"{'DUE DATE':<15}"
            f"{'DAYS OVERDUE':<15}"
        )

        print("-" * 100)

        for user, book, due_date, overdue_days in overdue_books:
            print(
                f"{user.name:<20}"
                f"{book.title:<30}"
                f"{due_date.isoformat():<15}"
                f"{overdue_days:<15}"
            )

        print("=" * 100)
        print(f"Total overdue books: {len(overdue_books)}")

    # -------------------- STATISTICS --------------------







    def most_read_book(self):
        borrowed_books = [
            book for book in self.books
            if book.borrow_count > 0
        ]

        if len(borrowed_books) < 2:
            print("Not enough data to compare borrowed books.")
            return

        counts = [book.borrow_count for book in borrowed_books]

        if min(counts) == max(counts):
            print("All borrowed books have the same borrow count.")
            return

        highest_count = max(counts)

        for book in borrowed_books:
            if book.borrow_count == highest_count:
                print(
                    f"Most borrowed book: {book.title} "
                    f"({book.borrow_count} borrows)"
                )



    def least_borrowed_book(self):
        borrowed_books = [
            book for book in self.books
            if book.borrow_count > 0
        ]

        if len(borrowed_books) < 2:
            print("Not enough data to compare borrowed books.")
            return

        counts = [book.borrow_count for book in borrowed_books]

        if min(counts) == max(counts):
            print("All borrowed books have the same borrow count.")
            return

        lowest_count = min(counts)

        least_read = [
            book for book in borrowed_books
            if book.borrow_count == lowest_count
        ]

        unit = "borrow" if lowest_count == 1 else "borrows"
        print(f"Least borrowed books ({lowest_count} {unit}):")

        for book in least_read:
            print(f"- {book.title}")




