from user import User


class Admin(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)

    def add_book(self, library, book):
        library.add_book(book)
        print(f"Book '{book.title}' added successfully.")

    def add_user(self, library, user):
        if library.add_user(user):
            print(f"User '{user.name}' added successfully.")
            return True

        return False

    def remove_user(self, library, user):
        if user not in library.users:
            print("User not found.")
            return False

        if user.borrowed_books:
            print(f"User '{user.name}' has borrowed books:")

            for book in user.borrowed_books:
                print(f"- {book.title}")

            question = (
                "Return all books and remove this user? (yes/no): "
            )
        else:
            question = f"Remove user '{user.name}'? (yes/no): "

        while True:
            confirmation = input(question).strip().lower()

            if confirmation == "yes":
                break
            elif confirmation == "no":
                print("User removal cancelled.")
                return False
            else:
                print("Invalid input. Enter 'yes' or 'no'.")

        for book in user.borrowed_books.copy():
            if not library.return_book(user, book):
                print("Could not return all books. User was not removed.")
                return False

        library.users.remove(user)
        print(f"User '{user.name}' removed successfully.")
        return True