# Simple Contact Book

import json

class ContactBook:
    def __init__(self, filename='contacts.json'):
        self.filename = filename
        self.contacts = self.load_contacts()

    def load_contacts(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_contacts(self):
        with open(self.filename, 'w') as file:
            json.dump(self.contacts, file)

    def add_contact(self, name, phone):
        self.contacts[name] = phone
        self.save_contacts()

    def remove_contact(self, name):
        if name in self.contacts:
            del self.contacts[name]
            self.save_contacts()

    def update_contact(self, name, phone):
        if name in self.contacts:
            self.contacts[name] = phone
            self.save_contacts()

    def display_contacts(self):
        for name, phone in self.contacts.items():
            print(f'Name: {name}, Phone: {phone}')

if __name__ == "__main__":
    contact_book = ContactBook()
    contact_book.add_contact('John Doe', '123-456-7890')
    contact_book.display_contacts()
    contact_book.update_contact('John Doe', '098-765-4321')
    contact_book.display_contacts()
    contact_book.remove_contact('John Doe')
    contact_book.display_contacts()
