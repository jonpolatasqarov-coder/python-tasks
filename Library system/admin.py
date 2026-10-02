from user import User


class Admin(User):
    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)

    def add_book(self, library, book):
        library.add_book(book)
        print(f"Book '{book.title}' added successfully.")

    def add_user(self, library, user):
        library.add_user(user)
        print(f"User '{user.name}' added successfully.")

    def remove_user(self, library, user):
        if user in library.users:
            library.users.remove(user)
            print(f"User '{user.name}' removed successfully.")
        else:
            print("User not found.")