"""
Author: Jaydip Dey
Project: Student Library Management System with Admin & Student Login (Website Style)
"""

import datetime
import json
import os
from time import sleep

# ========== Fancy Console Styling ==========
def line():
    print("═" * 80)

def heading(text):
    line()
    print(f"🌐  {text.center(70)}  🌐")
    line()

def subheading(text):
    print(f"\n🔹 {text}")
    print("-" * 60)

def pause():
    input("\nPress Enter to continue...")

# ------------------ Library Class ------------------
class Library:
    def __init__(self, listofBooks):
        self.books = listofBooks

    def displayAvailableBooks(self):
        heading("📚 AVAILABLE BOOKS")
        if len(self.books) == 0:
            print("❌ No books available right now.")
        else:
            for i, book in enumerate(self.books, start=1):
                print(f" {i:>2}. {book}")
        pause()

    def borrowBook(self, username, bookname):
        if bookname not in self.books:
            print(f"⚠️ '{bookname}' is not available (might be issued by someone else).")
        else:
            issue_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            track.append({"user": username, "book": bookname, "issued_on": issue_time})
            print(f"✅ '{bookname}' issued to {username} on {issue_time}.")
            self.books.remove(bookname)
        pause()

    def returnBook(self, username, bookname):
        found = False
        for record in track:
            if record["user"] == username and record["book"].lower() == bookname.lower():
                found = True
                track.remove(record)
                break
        if found:
            print(f"✅ '{bookname}' returned successfully by {username}.")
            self.books.append(bookname)
        else:
            print(f"⚠️ No record found for {username} having '{bookname}'.")
        pause()

    def donateBook(self, bookname):
        if bookname in self.books:
            print(f"⚠️ '{bookname}' already exists in the library.")
        else:
            self.books.append(bookname)
            print(f"🎁 Thank you for donating '{bookname}'! It’s now available for others.")
        pause()

    def searchBook(self, query):
        heading(f"🔍 Searching for '{query}'")
        query = query.strip().lower()
        results = [book for book in self.books if book[0].lower() == query[0]]
        if results:
            print("✅ Found (books starting with the same letter):")
            for book in results:
                print(f" - {book}")
        else:
            print("❌ No books found starting with that letter.")
        pause()

    def deleteBook(self, bookname):
        if bookname in self.books:
            self.books.remove(bookname)
            print(f"🗑️ '{bookname}' removed from library records.")
        else:
            print(f"⚠️ '{bookname}' not found in library.")
        pause()


# ------------------ Student Class ------------------
class Student:
    def __init__(self, username):
        self.username = username

    def requestBook(self):
        return input("📖 Enter the name of the book you want to borrow: ").strip()

    def returnBook(self):
        return input("🔁 Enter the name of the book you want to return: ").strip()


# ------------------ File Handling ------------------
def save_data():
    with open("books_data.json", "w") as f:
        json.dump(library.books, f, indent=4)
    with open("issued_data.json", "w") as f:
        json.dump(track, f, indent=4)
    with open("students_data.json", "w") as f:
        json.dump(students, f, indent=4)


def load_data():
    if os.path.exists("books_data.json"):
        with open("books_data.json") as f:
            books = json.load(f)
    else:
        books = [
            "Vistas", "Invention", "Rich & Poor",
            "Indian Economy", "Macroeconomics",
            "Gitanjali", "Gora", "Pather Panchali", "Ramayan"
        ]
    if os.path.exists("issued_data.json"):
        with open("issued_data.json") as f:
            issued = json.load(f)
    else:
        issued = []
    if os.path.exists("students_data.json"):
        with open("students_data.json") as f:
            student_list = json.load(f)
    else:
        student_list = {}
    return books, issued, student_list


# ------------------ Login System ------------------
def login():
    heading("🔐 LOGIN PORTAL")

    print("1️⃣  Admin Login")
    print("2️⃣  Student Login")
    print("3️⃣  Register as New Student")
    print("4️⃣  Exit")

    while True:
        try:
            user_type = int(input("\n👉 Select (1–4): "))

            # Admin Login
            if user_type == 1:
                username = input("👤 Admin username: ")
                password = input("🔑 Password: ")
                if username == "admin" and password == "1234":
                    print("\n✅ Admin login successful.")
                    sleep(1)
                    admin_menu()
                    break
                else:
                    print("❌ Incorrect credentials.\n")

            # Student Login
            elif user_type == 2:
                username = input("👤 Username: ")
                password = input("🔑 Password: ")
                if username in students and students[username] == password:
                    print(f"\n✅ Welcome back, {username}!")
                    sleep(1)
                    student_menu(username)
                    break
                else:
                    print("❌ Invalid username or password.\n")

            # Register
            elif user_type == 3:
                new_user = input("🆕 Choose username: ").strip()
                if new_user in students:
                    print("⚠️ Username already exists.")
                else:
                    new_pass = input("🔑 Choose password: ").strip()
                    students[new_user] = new_pass
                    save_data()
                    print(f"🎉 Welcome, {new_user}! Registration successful.")
                pause()

            # Exit
            elif user_type == 4:
                print("\n👋 Thank you for visiting Jaydip's Library!")
                save_data()
                exit()

            else:
                print("⚠️ Invalid choice. Enter between 1–4.\n")
        except ValueError:
            print("❌ Please enter a valid number.\n")


# ------------------ Admin Menu ------------------
def admin_menu():
    while True:
        heading("🧠 ADMIN DASHBOARD")
        print("""
1️⃣  List all available books
2️⃣  Add (Donate) a new book
3️⃣  Delete a book
4️⃣  View all issued book records
5️⃣  Search for a book
6️⃣  Logout
""")
        try:
            choice = int(input("👉 Enter choice (1–6): "))
            if choice == 1:
                library.displayAvailableBooks()
            elif choice == 2:
                book = input("Enter name of the book to add: ").strip()
                library.donateBook(book)
            elif choice == 3:
                book = input("Enter book name to delete: ").strip()
                library.deleteBook(book)
            elif choice == 4:
                heading("📘 ISSUED BOOK RECORDS")
                if len(track) == 0:
                    print("No books currently issued.")
                else:
                    for record in track:
                        print(f"📗 {record['book']} → {record['user']} ({record['issued_on']})")
                pause()
            elif choice == 5:
                query = input("Enter search keyword: ").strip()
                library.searchBook(query)
            elif choice == 6:
                print("💾 Logging out...")
                sleep(1)
                save_data()
                break
            else:
                print("⚠️ Invalid option.\n")
        except ValueError:
            print("❌ Enter a valid number.\n")


# ------------------ Student Menu ------------------
def student_menu(username):
    s = Student(username)
    while True:
        heading(f"🎓 STUDENT DASHBOARD ({username})")
        print("""
1️⃣  Borrow a book
2️⃣  Return a book
3️⃣  Search for a book
4️⃣  Logout
""")
        try:
            choice = int(input("👉 Enter choice (1–4): "))
            if choice == 1:
                book = s.requestBook()
                library.borrowBook(username, book)
            elif choice == 2:
                book = s.returnBook()
                library.returnBook(username, book)
            elif choice == 3:
                query = input("Enter keyword to search: ").strip()
                library.searchBook(query)
            elif choice == 4:
                print(f"💾 Logging out, {username}...")
                sleep(1)
                save_data()
                break
            else:
                print("⚠️ Invalid input.\n")
        except ValueError:
            print("❌ Please enter a valid number.\n")


# ------------------ Main ------------------
if __name__ == "__main__":
    books_list, track, students = load_data()
    library = Library(books_list)

    heading("📖 WELCOME TO JAYDIP'S DIGITAL LIBRARY 📖")
    while True:
        login()

