from library import Library
from recommender import recommend_books
from admin import Admin
from user import User
from book import Book


library = Library()
library.load_data()

admin = Admin(999, "Administrator", "admin@library.com")


while True:
    print("\n===== LIBRARY MANAGEMENT =====")
    print("1. List books")
    print("2. Search book")
    print("3. Borrow book")
    print("4. Return book")
    print("5. Extend rental period")
    print("6. Recommend books")
    print("7. Check overdue books")
    print("8. Statistics")
    print("9. Admin panel")
    print("10. Register user")
    print("0. Exit")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        print("\n--- Books ---")

        for book in library.books:
            status = "Available" if book.is_available else "Borrowed"

            print(
                f"ID:{book.book_id} {book.title} - "
                f"{book.author} - {status}"
            )

    elif choice == "2":
        search = input("Enter book title or author: ").strip().lower()

        if not search:
            print("Search cannot be empty.")
            continue

        found = False

        for book in library.books:
            if (
                search in book.title.strip().lower()
                or search in book.author.strip().lower()
            ):
                print(
                    f"{book.book_id}. {book.title} - "
                    f"{book.author}"
                )
                found = True

        if not found:
            print("Book not found.")

    elif choice == "3":
        try:
            user_id = int(input("Enter user ID: "))
            book_id = int(input("Enter book ID: "))
        except ValueError:
            print("Invalid input. Please enter numbers only.")
            continue

        user = next(
            (user for user in library.users
            if user.user_id == user_id),
            None
        )

        book = next(
            (book for book in library.books
            if book.book_id == book_id),
            None
        )

        if user and book:
            library.borrow_book(user, book)
            library.save_data()
        else:
            print("User or book not found.")

    elif choice == "4":
        try:
            user_id = int(input("Enter user ID: "))
            book_id = int(input("Enter book ID: "))
        except ValueError:
            print("Invalid input. Please enter numbers only.")
            continue

        user = next(
            (user for user in library.users
             if user.user_id == user_id),
            None
        )

        book = next(
            (book for book in library.books
             if book.book_id == book_id),
            None
        )

        if user and book:
            library.return_book(user, book)
            library.save_data()
        else:
            print("User or book not found.")

    elif choice == "5":
        try:
            user_id = int(input("Enter user ID: "))
            book_id = int(input("Enter book ID: "))
        except ValueError:
            print("Invalid input. Please enter numbers only.")
            continue

        user = next(
            (user for user in library.users
             if user.user_id == user_id),
            None
        )

        book = next(
            (book for book in library.books
             if book.book_id == book_id),
            None
        )

        if user and book:
            library.extend_book(user, book)
            library.save_data()
        else:
            print("User or book not found.")

    elif choice == "6":
        try:
            book_id = int(input("Enter book ID: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        selected_book = next(
            (book for book in library.books
             if book.book_id == book_id),
            None
        )

        if selected_book:
            recommendations = recommend_books(
                library.books,
                selected_book
            )

            print(
                f"\nRecommendations for: "
                f"{selected_book.title}"
            )

            for book, score in recommendations:
                print(
                    f"{book.title} - "
                    f"similarity: {score:.2f}"
                )
        else:
            print("Book not found.")

    elif choice == "7":
        library.check_overdue_books()

    elif choice == "8":
        print("\n--- Statistics ---")
        library.most_read_book()
        library.least_borrowed_book()

    elif choice == "9":
        try:
            admin_id = int(input("Enter admin ID: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if admin_id != admin.user_id:
            print("Access denied.")
            continue

        print("\n===== ADMIN PANEL =====")
        print("1. Add book")
        print("2. Add user")
        print("3. Remove user")
        print("0. Back")

        admin_choice = input("Choose an option: ").strip()

        if admin_choice == "1":
            try:
                book_id = int(input("Enter book ID: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if any(book.book_id == book_id for book in library.books):
                print("Book ID already exists.")
                continue

            title = input("Enter book title: ")
            author = input("Enter author: ")
            description = input("Enter description: ")

            book = Book(
                book_id,
                title,
                author,
                description
            )

            admin.add_book(library, book)
            library.save_data()

        elif admin_choice == "2":
            try:
                user_id = int(input("Enter user ID: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if any(user.user_id == user_id for user in library.users):
                print("User ID already exists.")
                continue

            name = input("Enter user name: ")
            email = input("Enter user email: ")

            user = User(user_id, name, email)

            admin.add_user(library, user)
            library.save_data()

        elif admin_choice == "3":
            try:
                user_id = int(input("Enter user ID: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            user = next(
                (user for user in library.users
                if user.user_id == user_id),
                None
            )

            if user:
                admin.remove_user(library, user)
                library.save_data()
            else:
                print("User not found.")

        elif admin_choice == "0":
            continue

        else:
            print("Invalid option.")

    elif choice == "10":
        name = input("Enter your name: ").strip()
        email = input("Enter your email: ").strip()

        if not name or not email:
            print("Name and email cannot be empty.")
            continue

        if any(user.email.lower() == email.lower()
               for user in library.users):
            print("A user with this email already exists.")
            continue

        if library.users:
            new_user_id = max(
                user.user_id for user in library.users
            ) + 1
        else:
            new_user_id = 1

        user = User(
            new_user_id,
            name,
            email
        )

        library.add_user(user)
        library.save_data()

        print("User registered successfully.")
        print(f"Your user ID is: {new_user_id}")

    elif choice == "0":
        library.save_data()
        print("Data saved. Goodbye!")
        break

    else:
        print("Invalid option.")