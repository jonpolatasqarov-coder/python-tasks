from library import Library
from recommender import recommend_books
from admin import Admin
from user import User
from book import Book
import json
import hashlib
import hmac
from datetime import date, datetime, timedelta


def verify_admin_password():
    try:
        with open("admin.json", "r", encoding="utf-8") as file:
            admin_data = json.load(file)

        salt = bytes.fromhex(admin_data["salt"])
        expected_hash = admin_data["password_hash"]
        iterations = admin_data["iterations"]

    except (OSError, json.JSONDecodeError, KeyError, ValueError, TypeError):
        print("Admin configuration is missing or invalid.")
        return False

    password = input("Enter admin password: ")

    entered_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations
    ).hex()

    if hmac.compare_digest(entered_hash, expected_hash):
        return True

    print("Access denied.")
    return False


library = Library()
library.load_data()

admin = Admin(999, "Administrator", "admin@library.com")




while True:
    print("\n" + "=" * 50)
    print("LIBRARY MANAGEMENT SYSTEM".center(50))
    print("=" * 50)

    print("\nBOOKS")
    print("  1. List books")
    print("  2. Search book")

    print("\nRENTALS")
    print("  3. Borrow book")
    print("  4. Return book")
    print("  5. Extend rental period")
    print("  6. Check overdue books")

    print("\nOTHER")
    print("  7. Recommend books")
    print("  8. Statistics")

    print("\nADMINISTRATION")
    print("  9. Admin panel")
    print(" 10. Register user")

    print("\n" + "-" * 50)
    print("  0. Exit")
    print("=" * 50)

    choice = input("\nChoose an option: ").strip()


    if choice == "1":
        print("\n" + "=" * 100)
        print("LIBRARY BOOK CATALOG".center(100))
        print("=" * 100)

        print(
            f"{'ID':<5}"
            f"{'BOOK TITLE':<35}"
            f"{'AUTHOR':<40}"
            f"{'STATUS':<15}"
        )

        print("-" * 100)

        sorted_books = sorted(
            library.books,
            key=lambda book: book.title.lower()
        )

        for book in sorted_books:
            status = "Available" if book.is_available else "Borrowed"

            print(
                f"{book.book_id:<5}"
                f"{book.title:<35}"
                f"{book.author:<40}"
                f"{status:<15}"
            )

        print("=" * 100)
        print(f"Total books: {len(library.books)}")

        available = sum(
            1 for book in library.books if book.is_available
        )
        borrowed = len(library.books) - available

        print(f"Available: {available} | Borrowed: {borrowed}")

        input("\nPress Enter to return to the main menu...")



    elif choice == "2":
        back_to_main = False

        while True:
            search = input(
                "\nEnter book title or author: "
            ).strip().lower()

            if not search:
                print("Search cannot be empty.")
                continue

            found_books = [
                book for book in library.books
                if (
                    search in book.title.lower()
                    or search in book.author.lower()
                )
            ]

            found_books.sort(
                key=lambda book: book.title.lower()
            )

            if not found_books:
                print("\nNo books found matching your search.")

                while True:
                    print("\n1. Search again")
                    print("0. Back to main menu")

                    action = input(
                        "\nChoose an option: "
                    ).strip()

                    if action == "1":
                        break
                    elif action == "0":
                        back_to_main = True
                        break
                    else:
                        print("Invalid option. Please try again.")

                if back_to_main:
                    break

                continue

            print("\n" + "=" * 100)
            print("SEARCH RESULTS".center(100))
            print("=" * 100)

            print(
                f"{'ID':<5}"
                f"{'BOOK TITLE':<35}"
                f"{'AUTHOR':<40}"
                f"{'STATUS':<15}"
            )

            print("-" * 100)

            for book in found_books:
                status = (
                    "Available"
                    if book.is_available
                    else "Borrowed"
                )

                print(
                    f"{book.book_id:<5}"
                    f"{book.title:<35}"
                    f"{book.author:<40}"
                    f"{status:<15}"
                )

            print("-" * 100)

            available_count = sum(
                1 for book in found_books
                if book.is_available
            )

            borrowed_count = sum(
                1 for book in found_books
                if not book.is_available
            )

            print(f"Results found:   {len(found_books)}")
            print(f"Available:       {available_count}")
            print(f"Borrowed:        {borrowed_count}")
            print("=" * 100)

            while True:
                print("\n1. Borrow a book")
                print("2. Search again")
                print("0. Back to main menu")

                action = input(
                    "\nChoose an option: "
                ).strip()

                if action == "0":
                    back_to_main = True
                    break

                elif action == "2":
                    break

                elif action == "1":
                    # 1. Kitobni tanlash
                    if len(found_books) == 1:
                        selected_book = found_books[0]

                        print(
                            f"\nSelected book: "
                            f"{selected_book.title}"
                        )

                    else:
                        try:
                            selected_id = int(
                                input(
                                    "Enter the book ID to borrow: "
                                )
                            )
                        except ValueError:
                            print("Please enter a valid number.")
                            continue

                        selected_book = next(
                            (
                                book for book in found_books
                                if book.book_id == selected_id
                            ),
                            None
                        )

                        if selected_book is None:
                            print(
                                "Invalid ID. Choose a book "
                                "from the search results."
                            )
                            continue

                    # 2. Kitob mavjudligini tekshirish
                    if not selected_book.is_available:
                        print("This book is already borrowed.")
                        continue

                    # 3. User ID ni tekshirish
                    while True:
                        try:
                            user_id = int(
                                input("Enter your user ID: ")
                            )
                        except ValueError:
                            print(
                                "Invalid user ID. Enter a number."
                            )
                            continue

                        user = next(
                            (
                                u for u in library.users
                                if u.user_id == user_id
                            ),
                            None
                        )

                        if user is not None:
                            break

                        print("User not found.")

                        while True:
                            print("\n1. Try again")
                            print("2. Search again")
                            print("0. Back to main menu")

                            retry = input(
                                "\nChoose an option: "
                            ).strip()

                            if retry == "1":
                                break
                            elif retry == "2":
                                action = "2"
                                break
                            elif retry == "0":
                                action = "0"
                                back_to_main = True
                                break
                            else:
                                print(
                                    "Invalid option. "
                                    "Please choose 1, 2, or 0."
                                )

                        if user is not None:
                            break

                        if action in ("2", "0"):
                            break

                    if back_to_main:
                        break

                    if action == "2":
                        break

                    # 4. Ijara muddatini so'rash
                    while True:
                        try:
                            borrow_days = int(
                                input(
                                    "Enter rental period (1-14 days): "
                                )
                            )
                        except ValueError:
                            print(
                                "Invalid input. "
                                "Please enter a whole number "
                                "from 1 to 14."
                            )
                            continue

                        if 1 <= borrow_days <= 14:
                            break

                        print(
                            "Rental period must be between "
                            "1 and 14 days."
                        )

                    # 5. Kitobni berish va saqlash
                    library.borrow_book(
                        user,
                        selected_book,
                        borrow_days
                    )
                    library.save_data()

                    print("\nBorrow request processed.")

                    # 6. Keyingi amal
                    while True:
                        print("\n1. Search again")
                        print("0. Back to main menu")

                        next_action = input(
                            "\nChoose an option: "
                        ).strip()

                        if next_action == "1":
                            action = "2"
                            break
                        elif next_action == "0":
                            back_to_main = True
                            break
                        else:
                            print(
                                "Invalid option. "
                                "Please choose 1 or 0."
                            )

                    break

                else:
                    print("Invalid option. Please try again.")

            if back_to_main:
                break

            if action == "2":
                continue

            break


    elif choice == "3":
        # 1. Foydalanuvchini topish
        user = None

        while True:
            try:
                user_id = int(input("Enter user ID: "))
            except ValueError:
                print("Invalid user ID. Please enter a number.")
                continue

            user = next(
                (u for u in library.users if u.user_id == user_id),
                None
            )

            if user is not None:
                break

            print("User not found.")
            print("1. Try again")
            print("0. Back to main menu")

            action = input("Choose an option: ").strip()

            if action == "0":
                user = None
                break
            elif action == "1":
                continue
            else:
                print("Invalid option. Please choose 1 or 0.")
                continue

        if user is None:
            continue

        # 2. Mavjud kitoblarni topish va tartiblash
        available_books = sorted(
            [book for book in library.books if book.is_available],
            key=lambda book: book.title.lower()
        )

        print("\n" + "=" * 95)
        print("AVAILABLE BOOKS".center(95))
        print("=" * 95)

        if not available_books:
            print("No books are currently available.")
            print("=" * 95)
            input("\nPress Enter to return to the main menu...")
            continue

        print(f"{'ID':<5}{'BOOK TITLE':<35}{'AUTHOR':<40}")
        print("-" * 95)

        for book in available_books:
            print(
                f"{book.book_id:<5}"
                f"{book.title:<35}"
                f"{book.author:<40}"
            )

        print("=" * 95)

        # 3. Yaqin 14 kun ichida qaytariladigan kitoblarni topish
        soon_books = []
        today = date.today()
        soon_limit = today + timedelta(days=14)

        for borrower in library.users:
            for borrowed_book in borrower.borrowed_books:
                due_date_text = borrower.borrow_dates.get(
                    borrowed_book.book_id
                )

                if not due_date_text:
                    continue

                try:
                    due_date = datetime.strptime(
                        due_date_text, "%Y-%m-%d"
                    ).date()
                except ValueError:
                    continue

                if today <= due_date <= soon_limit:
                    soon_books.append((borrowed_book, due_date))

        # Eng yaqin qaytariladigan kitoblar birinchi chiqadi
        soon_books.sort(key=lambda item: item[1])

        total_soon_books = len(soon_books)
        soon_books = soon_books[:3]

        # 4. Ixcham SOON AVAILABLE BOOKS jadvali
        print("\n" + "=" * 70)
        print("SOON AVAILABLE BOOKS".center(70))
        print("=" * 70)

        if soon_books:
            print(f"{'ID':<5}{'BOOK TITLE':<32}{'DUE DATE':<15}")
            print("-" * 70)

            for book, due_date in soon_books:
                print(
                    f"{book.book_id:<5}"
                    f"{book.title:<32}"
                    f"{due_date.isoformat():<15}"
                )

            print("-" * 70)
        else:
            print("No books are expected soon.")

        print(
            f"Showing {len(soon_books)} of {total_soon_books} books."
        )
        print("=" * 70)

        # 5. Kitob tanlash
        while True:
            try:
                book_id = int(
                    input("\nEnter book ID to borrow (0 to cancel): ")
                )
            except ValueError:
                print("Invalid input. Please enter a book ID number.")
                continue

            if book_id == 0:
                print("Borrowing cancelled.")
                break


            book = next(
                (b for b in library.books if b.book_id == book_id),
                None
            )

            if book is None:
                print(f"No book exists with ID {book_id}.")
                continue

            if not book.is_available:
                print(
                    f"'{book.title}' is currently borrowed "
                    "and is not available."
                )
                continue


            # 6. Ijara muddatini kiritish
            while True:
                try:
                    borrow_days = int(
                        input("Enter rental period (1-14 days): ")
                    )
                except ValueError:
                    print("Please enter a whole number from 1 to 14.")
                    continue

                if 1 <= borrow_days <= 14:
                    break

                print("Rental period must be between 1 and 14 days.")

            # 7. Kitobni berish va ma'lumotlarni saqlash
            library.borrow_book(user, book, borrow_days)
            library.save_data()
            break


    elif choice == "4":
        # 1. Foydalanuvchini topish
        user = None

        while True:
            try:
                user_id = int(input("Enter user ID: "))
            except ValueError:
                print("Invalid user ID. Please enter a number.")
                continue

            user = next(
                (u for u in library.users if u.user_id == user_id),
                None
            )

            if user is not None:
                break

            print("User not found.")

            while True:
                print("1. Try again")
                print("0. Back to main menu")

                action = input("Choose an option: ").strip()

                if action == "1":
                    break
                elif action == "0":
                    user = None
                    break
                else:
                    print("Invalid option. Please choose 1 or 0.")

            if action == "1":
                continue

            user = None
            break

        if user is None:
            continue

        # 2. Bir nechta kitobni ketma-ket qaytarish
        while True:

            if not user.borrowed_books:
                print("\nThis user has no borrowed books remaining.")
                input("Press Enter to return to the main menu...")
                break

            # 3. Foydalanuvchi olgan kitoblarni chiqarish
            print("\n" + "=" * 80)
            print("BORROWED BOOKS".center(80))
            print("=" * 80)
            print(f"{'ID':<6}{'BOOK TITLE':<35}{'AUTHOR':<39}")
            print("-" * 80)

            for book in user.borrowed_books:
                print(
                    f"{book.book_id:<6}"
                    f"{book.title:<35}"
                    f"{book.author:<39}"
                )

            print("=" * 80)

            # 4. Qaytariladigan kitob ID sini olish
            while True:
                try:
                    book_id = int(
                        input(
                            "\nEnter book ID to return "
                            "(0 to return to main menu): "
                        )
                    )
                except ValueError:
                    print("Invalid input. Please enter a book ID number.")
                    continue

                if book_id == 0:
                    break


                # Avval kitob umuman mavjudligini tekshirish
                existing_book = next(
                    (
                        b for b in library.books
                        if b.book_id == book_id
                    ),
                    None
                )

                if existing_book is None:
                    print(f"No book exists with ID {book_id}.")
                    continue

                # Keyin shu foydalanuvchi kitobni olganmi, tekshirish
                book = next(
                    (
                        b for b in user.borrowed_books
                        if b.book_id == book_id
                    ),
                    None
                )

                if book is None:
                    print(
                        f"'{existing_book.title}' is not borrowed "
                        "by this user."
                    )
                    continue


                # 5. Kitobni Library methodi orqali qaytarish
                success = library.return_book(user, book)

                if success:
                    library.save_data()

                break

            # 6. Foydalanuvchi 0 kiritsa, menyuga qaytish
            if book_id == 0:
                break

        continue

    elif choice == "5":
        # 1. Foydalanuvchini topish
        while True:
            try:
                user_id = int(input("Enter user ID (0 to cancel): "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if user_id == 0:
                break

            user = next(
                (u for u in library.users if u.user_id == user_id),
                None
            )

            if user is None:
                print(f"No user exists with ID {user_id}.")
                continue

            break

        if user_id == 0:
            continue

        # 2. Foydalanuvchining kitoblarini tekshirish
        if not user.borrowed_books:
            print(f"User '{user.name}' has no borrowed books.")
            continue

        print("\n" + "=" * 80)
        print("BORROWED BOOKS".center(80))
        print("=" * 80)
        print(f"{'ID':<6}{'BOOK TITLE':<35}{'AUTHOR':<39}")
        print("-" * 80)

        for borrowed_book in user.borrowed_books:
            print(
                f"{borrowed_book.book_id:<6}"
                f"{borrowed_book.title:<35}"
                f"{borrowed_book.author:<39}"
            )

        print("=" * 80)

        # 3. Uzaytiriladigan kitobni tanlash
        while True:
            try:
                book_id = int(
                    input("\nEnter book ID to extend (0 to cancel): ")
                )
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if book_id == 0:
                break

            existing_book = next(
                (b for b in library.books if b.book_id == book_id),
                None
            )

            if existing_book is None:
                print(f"No book exists with ID {book_id}.")
                continue

            book = next(
                (
                    b for b in user.borrowed_books
                    if b.book_id == book_id
                ),
                None
            )

            if book is None:
                print(
                    f"'{existing_book.title}' is not borrowed "
                    f"by user '{user.name}'."
                )
                continue

            # 4. Ijara sanalarini tekshirish
            old_due_date = user.borrow_dates.get(book.book_id)
            start_text = user.borrow_start_dates.get(book.book_id)

            if not old_due_date or not start_text:
                print(
                    "Rental date information is missing. "
                    "The rental period cannot be extended."
                )
                continue

            start_date = date.fromisoformat(start_text)
            current_due_date = date.fromisoformat(old_due_date)

            current_total_days = (current_due_date - start_date).days
            remaining_days = 14 - current_total_days

            if remaining_days <= 0:
                print(
                    "The maximum rental period of 14 days "
                    "has been reached."
                )
                continue

            print(
                f"You can extend this book by up to "
                f"{remaining_days} days."
            )

            # 5. Kun sonini so'rash va tekshirish
            while True:
                try:
                    days = int(
                        input("How many days do you want to extend? ")
                    )
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue

                success = library.extend_book(user, book, days)

                if success:
                    library.save_data()
                    break

                print(
                    "Please enter a valid number of days "
                    "and try again."
                )

            # Kitob muddati muvaffaqiyatli uzaytirildi
            break

        continue

    elif choice == "6":
        library.check_overdue_books()

    elif choice == "7":
        while True:
            print("\n--- Book Recommendations ---")

            for book in library.books:
                print(f"ID: {book.book_id} | {book.title} - {book.author}")

            print("\n0. Back to main menu")

            try:
                book_id = int(input("\nChoose a book ID: "))
            except ValueError:
                print("Please enter a valid number.")
                continue

            if book_id == 0:
                break

            selected_book = next(
                (book for book in library.books if book.book_id == book_id),
                None
            )

            if selected_book is None:
                print("Book not found. Try again.")
                continue

            recommendations = recommend_books(
                library.books,
                selected_book
            )

            print(f"\nRecommendations for '{selected_book.title}':")

            if not recommendations:
                print("No recommendations found.")
            else:
                for book, _ in recommendations:
                    print(f"- {book.title} - {book.author}")

            input("\nPress Enter to continue...")

    elif choice == "8":
        print("\n--- Statistics ---")
        library.most_read_book()
        library.least_borrowed_book()

    elif choice == "9":
        if not verify_admin_password():
            continue

        while True:
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
                    print("Error: A book with this ID already exists.")
                    continue

                title = input("Enter book title: ").strip()

                if not title:
                    print("Book title cannot be empty.")
                    continue

                if any(
                    book.title.strip().casefold() == title.casefold()
                    for book in library.books
                ):
                    print("Error: A book with this title already exists.")
                    continue

                author = input("Enter author: ").strip()

                if not author:
                    print("Author cannot be empty.")
                    continue

                description = input("Enter description: ").strip()

                book = Book(book_id, title, author, description)

                admin.add_book(library, book)
                library.save_data()

            elif admin_choice == "2":
                while True:
                    try:
                        user_id = int(input("Enter user ID: "))
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                        continue

                    if any(user.user_id == user_id for user in library.users):
                        print("Error: A user with this ID already exists.")
                        continue

                    break

                while True:
                    name = input("Enter user name: ").strip()

                    if not name:
                        print("User name cannot be empty.")
                        continue

                    break

                while True:
                    email = input("Enter user email: ").strip()

                    if " " in email:
                        print("Invalid email address. Please try again.")
                        continue

                    if email.count("@") != 1:
                        print("Invalid email address. Please try again.")
                        continue

                    local_part, domain = email.split("@")

                    if not local_part or not domain:
                        print("Invalid email address. Please try again.")
                        continue

                    if "." not in domain:
                        print("Invalid email address. Please try again.")
                        continue

                    if domain.startswith(".") or domain.endswith("."):
                        print("Invalid email address. Please try again.")
                        continue

                    if ".." in email:
                        print("Invalid email address. Please try again.")
                        continue

                    domain_parts = domain.split(".")

                    if any(not part for part in domain_parts):
                        print("Invalid email address. Please try again.")
                        continue

                    if len(domain_parts[-1]) < 2:
                        print("Invalid email address. Please try again.")
                        continue

                    if any(
                        user.email.strip().casefold() == email.casefold()
                        for user in library.users
                    ):
                        print("Error: A user with this email already exists.")
                        continue

                    break

                user = User(user_id, name, email)

                if admin.add_user(library, user):
                    library.save_data()

            elif admin_choice == "3":
                try:
                    user_id = int(input("Enter user ID: "))
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue

                user = next(
                    (
                        user for user in library.users
                        if user.user_id == user_id
                    ),
                    None
                )

                if user is None:
                    print("User not found.")
                    continue

                removed = admin.remove_user(library, user)

                if removed:
                    library.save_data()

            elif admin_choice == "0":
                print("Returning to main menu...")
                break

            else:
                print("Invalid option. Please try again.")

    elif choice == "10":
        print("\n--- Register User ---")

        # 1. Username validation
        while True:
            name = input("Enter username: ").lower()

            if not name or name != name.strip() or " " in name:
                print("Username cannot contain spaces or be empty.")
                continue

            if len(name) < 3:
                print("Username must contain at least 3 characters.")
                continue

            if not name.isascii() or not name[0].isalpha():
                print("Username must start with an English letter.")
                continue

            if not all(
                char.isalnum() or char == "_"
                for char in name
            ):
                print(
                    "Username can contain only English letters, "
                    "digits, and underscores."
                )
                continue

            if any(
                user.name.strip().lower() == name
                for user in library.users
            ):
                print("This username is already taken.")
                continue

            break
        # 2. Email validation
        while True:
            email = input("Enter email address: ").lower()

            if (
                not email
                or email != email.strip()
                or any(char.isspace() for char in email)
            ):
                print("Email cannot be empty or contain spaces.")
                continue

            if email.count("@") != 1:
                print("Invalid email format.")
                continue

            local_part, domain = email.split("@")

            if (
                not local_part
                or not domain
                or local_part.startswith(".")
                or local_part.endswith(".")
                or ".." in email
                or "." not in domain
                or domain.startswith(".")
                or domain.endswith(".")
            ):
                print("Invalid email format.")
                continue

            if any(
                user.email.strip().lower() == email
                for user in library.users
            ):
                print("This email is already registered.")
                continue

            break
        # 3. Generate a unique user ID
        user_id = max(
            (user.user_id for user in library.users),
            default=0
        ) + 1

        # 4. Create and register the user
        user = User(user_id, name, email)

        if library.add_user(user):
            library.save_data()

            print("\nRegistration successful!")
            print(f"Username: {name}")
            print(f"Email: {email}")
            print(f"User ID: {user_id}")
        else:
            print("Registration failed.")

    elif choice == "0":
        library.save_data()
        print("Data saved. Goodbye!")
        break

    else:
        print("Invalid option.")