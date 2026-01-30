"""
Author: Jaydip Dey
Project: Student Library Management System with Admin & Student Login (Website Style)
"""

import datetime
import json
import os

# ========== Fancy Console Styling ==========
def line():
    print("═" * 80)

def heading(text):
    line()
    print(f"🌐  {text.center(70)}  🌐")
    line()

def pause():
    input("\nPress Enter to continue...")

# ------------------ Library Class ------------------
class Library:
    def __init__(self, listofBooks):
        self.books = listofBooks

    def displayAvailableBooks(self):
        heading("📚 AVAILABLE BOOKS")
        if not self.books:
            print("❌ No books available.")
        else:
            for i, book in enumerate(self.books, start=1):
                print(f"{i}. {book}")
        pause()

    def borrowBook(self, username, bookname):
        if bookname not in self.books:
            print("⚠️ Book not available.")
        else:
            issue_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            track.append({"user": username, "book": bookname, "issued_on": issue_time})
            self.books.remove(bookname)
            print(f"✅ '{bookname}' issued to {username}")
        pause()

    def returnBook(self, username, bookname):
        for record in track:
            if record["user"] == username and record["book"].lower() == bookname.lower():
                track.remove(record)
                self.books.append(bookname)
                print("✅ Book returned.")
                pause()
                return
        print("⚠️ No record found.")
        pause()

    def donateBook(self, bookname):
        if bookname in self.books:
            print("⚠️ Book already exists.")
        else:
            self.books.append(bookname)
            print("🎁 Book added.")
        pause()

    def searchBook(self, query):
        heading("🔍 SEARCH RESULT")
        results = [b for b in self.books if query.lower() in b.lower()]
        if results:
            for b in results:
                print(b)
        else:
            print("❌ Not found.")
        pause()

    def deleteBook(self, bookname):
        if bookname in self.books:
            self.books.remove(bookname)
            print("🗑️ Book deleted.")
        else:
            print("⚠️ Book not found.")
        pause()

# ------------------ File Handling ------------------
def save_data():
    json.dump(library.books, open("books_data.json","w"), indent=4)
    json.dump(track, open("issued_data.json","w"), indent=4)
    json.dump(students, open("students_data.json","w"), indent=4)

def load_data():
    books = json.load(open("books_data.json")) if os.path.exists("books_data.json") else ["Ramayan","Gitanjali","Economics"]
    issued = json.load(open("issued_data.json")) if os.path.exists("issued_data.json") else []
    student_list = json.load(open("students_data.json")) if os.path.exists("students_data.json") else {}
    return books, issued, student_list

# ------------------ Login System ------------------
def login():
    heading("🔐 LOGIN PORTAL")
    print("1. Admin Login")
    print("2. Student Login")
    print("3. Exit\n")

    while True:
        try:
            ch = int(input("Select (1-3): "))
            if ch == 1:
                if input("Admin Username: ")=="admin" and input("Password: ")=="1234":
                    admin_menu()
                    break
                else:
                    print("❌ Wrong admin login")

            elif ch == 2:
                u = input("Username: ")
                p = input("Password: ")
                if u in students and students[u]==p:
                    student_menu(u)
                    break
                else:
                    print("❌ Invalid login")

            elif ch == 3:
                save_data()
                exit()
            else:
                print("⚠️ Invalid choice. Enter 1-3.\n")
        except ValueError:
            print("❌ Please enter a valid number.\n")

# ------------------ Admin Menu ------------------
def admin_menu():
    global track, students

    while True:
        heading("🧠 ADMIN DASHBOARD")
        print("""
1. View Books
2. Add Book
3. Delete Book
4. View Issued Records (All)
5. Search Book
6. Register Student
7. View Students
8. Delete Student
9. View Student Issue History
10. Logout
""")
        try:
            ch = int(input("Choice (1-10): "))
            if ch == 1:
                library.displayAvailableBooks()
            elif ch == 2:
                library.donateBook(input("Book Name: "))
            elif ch == 3:
                library.deleteBook(input("Book Name: "))
            elif ch == 4:
                heading("📘 ALL ISSUED RECORDS")
                if track:
                    for r in track:
                        print(f"{r['book']} → {r['user']} ({r['issued_on']})")
                else:
                    print("No issued records.")
                pause()
            elif ch == 5:
                library.searchBook(input("Search Keyword: "))
            elif ch == 6:
                u = input("New Student Username: ")
                if u in students:
                    print("⚠️ Username already exists.")
                else:
                    students[u] = input("Password: ")
                    print("🎉 Student registered.")
                pause()
            elif ch == 7:
                heading("👨‍🎓 REGISTERED STUDENTS")
                if students:
                    for s in students:
                        print(s)
                else:
                    print("No students registered yet.")
                pause()
            elif ch == 8:
                d = input("Enter student username to delete: ")
                if d in students:
                    del students[d]
                    track = [r for r in track if r["user"] != d]
                    print("🗑️ Student deleted.")
                else:
                    print("⚠️ Student not found.")
                pause()
            elif ch == 9:
                user = input("Enter student username to view history: ")
                heading(f"📜 ISSUE HISTORY: {user}")
                found = False
                for r in track:
                    if r["user"] == user:
                        print(f"{r['book']} ({r['issued_on']})")
                        found = True
                if not found:
                    print("No history found.")
                pause()
            elif ch == 10:
                save_data()
                break
            else:
                print("⚠️ Invalid choice. Enter 1-10.\n")
        except ValueError:
            print("❌ Please enter a valid number.\n")

# ------------------ Student Menu ------------------
def student_menu(username):
    while True:
        heading(f"🎓 STUDENT DASHBOARD ({username})")
        print("""
1. Borrow Book
2. Return Book
3. Search Book
4. View My Issue History
5. Logout
""")
        try:
            ch = int(input("Choice (1-5): "))
            if ch == 1:
                library.borrowBook(username, input("Book Name: "))
            elif ch == 2:
                library.returnBook(username, input("Book Name: "))
            elif ch == 3:
                library.searchBook(input("Search Keyword: "))
            elif ch == 4:
                heading(f"📜 YOUR ISSUE HISTORY ({username})")
                found = False
                for r in track:
                    if r["user"] == username:
                        print(f"{r['book']} ({r['issued_on']})")
                        found = True
                if not found:
                    print("No history found.")
                pause()
            elif ch == 5:
                save_data()
                break
            else:
                print("⚠️ Invalid choice. Enter 1-5.\n")
        except ValueError:
            print("❌ Please enter a valid number.\n")

# ------------------ Main ------------------
books_list, track, students = load_data()
library = Library(books_list)

heading("📖 JAYDIP'S DIGITAL LIBRARY")
while True:
    login()



