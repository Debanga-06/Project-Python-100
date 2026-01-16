import os
import re

CONTACT_FILE = "contacts.txt"

# ---------- Helper Functions ----------
def load_contacts():
    contacts = {}
    if os.path.exists(CONTACT_FILE):
        with open(CONTACT_FILE, "r") as f:
            for line in f:
                name, phone, email = line.strip().split("|")
                contacts[name] = {"phone": phone, "email": email}
    return contacts

def save_contacts(contacts):
    with open(CONTACT_FILE, "w") as f:
        for name, info in contacts.items():
            f.write(f"{name}|{info['phone']}|{info['email']}\n")

# ---------- Validation ----------
def validate_phone(phone):
    return phone.isdigit() and len(phone) == 10

def validate_email(email):
    # Improved regex: must contain @, valid domain, no consecutive dots
    pattern = r'^(?!.*\.\.)[A-Za-z0-9._%+-]+@(?!.*\.\.)[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    if re.match(pattern, email):
        domain = email.split("@")[1]
        # Extra check: domain cannot start or end with dot
        if domain.startswith(".") or domain.endswith("."):
            return False
        return True
    return False

# ---------- CRUD Operations ----------
def add_contact(contacts):
    name = input("Enter Name: ")
    phone = input("Enter Phone (10 digits): ")
    email = input("Enter Email: ")

    errors = []
    if not validate_phone(phone):
        errors.append("⚠️ Invalid phone number! Must be exactly 10 digits.")
    if not validate_email(email):
        errors.append("⚠️ Invalid email format!")

    if errors:
        for error in errors:
            print(error)
        return

    contacts[name] = {"phone": phone, "email": email}
    save_contacts(contacts)
    print("✅ Contact added successfully!")

def view_contacts(contacts):
    if not contacts:
        print("No contacts found.")
    else:
        print("\n--- Contact List ---")
        for name, info in contacts.items():
            print(f"Name: {name}, Phone: {info['phone']}, Email: {info['email']}")

def update_contact(contacts):
    name = input("Enter the name to update: ")
    if name in contacts:
        phone = input("Enter new Phone (10 digits): ")
        email = input("Enter new Email: ")

        errors = []
        if not validate_phone(phone):
            errors.append("⚠️ Invalid phone number! Must be exactly 10 digits.")
        if not validate_email(email):
            errors.append("⚠️ Invalid email format!")

        if errors:
            for error in errors:
                print(error)
            return

        contacts[name] = {"phone": phone, "email": email}
        save_contacts(contacts)
        print("✅ Contact updated successfully!")
    else:
        print("Contact not found.")

def delete_contact(contacts):
    name = input("Enter the name to delete: ")
    if name in contacts:
        del contacts[name]
        save_contacts(contacts)
        print("✅ Contact deleted successfully!")
    else:
        print("Contact not found.")

# ---------- Main Program ----------
def main():
    contacts = load_contacts()
    while True:
        print("\n--- Contact Book Menu ---")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            view_contacts(contacts)
        elif choice == "3":
            update_contact(contacts)
        elif choice == "4":
            delete_contact(contacts)
        elif choice == "5":
            print("Exiting Contact Book. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()

