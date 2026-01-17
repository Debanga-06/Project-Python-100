# Contact Management System

A simple Python-based contact management system that allows you to add, view, update, and delete contacts. Contacts are stored in a text file (`contacts.txt`) for persistence.

## Features

- **Add Contact**: Add a new contact with name, phone number, and email.
- **View Contacts**: Display all saved contacts.
- **Update Contact**: Modify an existing contact's details.
- **Delete Contact**: Remove a contact by name.
- **Validation**: Ensures phone numbers are exactly 10 digits and emails follow a valid format.

## Requirements

- Python 3.x

## How to Run

1. Run the `Contact.py` script:
   ```
   python Contact.py
   ```
2. Follow the menu prompts to perform operations.

## Usage

- Choose an option from the menu (1-5).
- For adding/updating contacts, enter valid 10-digit phone numbers and properly formatted emails.
- Contacts are automatically saved to `contacts.txt`.

## Example

```
Enter choice: 1
Enter Name: John Doe
Enter Phone (10 digits): 1234567890
Enter Email: john.doe@example.com
✅ Contact added successfully!
```

## Notes

- Phone numbers must be exactly 10 digits.
- Emails are validated for basic format (e.g., no consecutive dots, proper domain).
- Data is stored in plain text; not encrypted.