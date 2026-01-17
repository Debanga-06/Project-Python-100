# Simple Contact Book 📇  ![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=yellow)

A comprehensive contact management application built with Python's tkinter GUI library. This project demonstrates File I/O operations, CRUD (Create, Read, Update, Delete) functionality, and data management best practices.

## 📋 Features

### Core CRUD Operations
- ➕ **Create**: Add new contacts with validation
- 📖 **Read**: View and search contacts
- ✏️ **Update**: Edit existing contact information
- 🗑️ **Delete**: Remove contacts with confirmation

### Data Management
- 💾 **Persistent Storage**: Saves contacts to JSON file
- 🔍 **Real-time Search**: Filter contacts as you type
- 📊 **Data Export**: Export contacts to CSV format
- 📥 **Data Import**: Import contacts from CSV files
- 💾 **Backup System**: Create timestamped backups
- ✅ **Data Validation**: Email and phone number validation
- 🔄 **Auto-save**: Automatic saving after each operation

### User Interface
- Clean and modern dark theme design
- Two-panel layout (list view and detail view)
- Search functionality with live filtering
- Category-based organization (Family, Friend, Work, Other)
- Contact count display
- Scrollable contact list
- Form-based data entry

### Advanced Features
- Duplicate contact detection
- Timestamp tracking (created/updated)
- Notes field for additional information
- Sort contacts alphabetically
- Confirmation dialogs for destructive actions

## 🎓 Learning Objectives

This project demonstrates:

1. **File I/O Operations**:
   - Reading from files (`open()`, `read()`)
   - Writing to files (`write()`)
   - JSON serialization (`json.dump()`, `json.load()`)
   - CSV file handling
   - File existence checking (`os.path.exists()`)
   - File encoding (UTF-8)

2. **CRUD Operations**:
   - **Create**: Adding new records to data structure
   - **Read**: Retrieving and displaying records
   - **Update**: Modifying existing records
   - **Delete**: Removing records from data structure

3. **Data Management**:
   - List operations (append, delete, sort)
   - Dictionary data structures
   - Data validation and sanitization
   - Search and filter algorithms
   - Data persistence strategies

4. **GUI Programming**:
   - Complex layouts with multiple frames
   - Form-based data entry
   - Listbox with scrollbar
   - Event handling and callbacks
   - Dynamic content updates

5. **Best Practices**:
   - Input validation
   - Error handling
   - User confirmation for critical actions
   - Data backup strategies
   - Code organization and modularity

## 🚀 Installation

### Prerequisites
- Python 3.6 or higher
- tkinter (usually included with Python)
- No external dependencies required

### Verify Installation

```bash
python -m tkinter
```

### Setup

1. Clone or download the project:
```bash
git clone <your-repo-url>
cd contact-book
```

2. Run the application:
```bash
python contact_book.py
```

## 💻 Usage

### Starting the Application

```bash
python contact_book.py
```

The application will:
- Create `contacts.json` if it doesn't exist
- Load existing contacts from the file
- Display the main interface

### Adding a Contact

1. Fill in the contact details:
   - **Name** (required)
   - **Phone** (optional, validated)
   - **Email** (optional, validated)
   - **Address** (optional)
   - **Category** (dropdown: Family, Friend, Work, Other)
   - **Notes** (optional, multi-line)

2. Click **➕ Add** button

3. Contact will be saved and appear in the list

### Viewing/Reading Contacts

1. Browse contacts in the left panel list
2. Use the search box to filter contacts
3. Click on a contact to view details
4. Details appear in the right panel form

### Updating a Contact

1. Select a contact from the list
2. Modify the fields in the form
3. Click **✏️ Update** button
4. Contact will be updated and saved

### Deleting a Contact

1. Select a contact from the list
2. Click **🗑️ Delete** button
3. Confirm the deletion
4. Contact will be removed

### Searching Contacts

1. Type in the search box at the top
2. Results filter automatically
3. Search works across: Name, Phone, Email, Category

### Exporting Contacts

1. Click **📊 Export CSV** button
2. Choose save location and filename
3. CSV file will be created with all contacts

### Importing Contacts

1. Click **📥 Import CSV** button
2. Select a CSV file to import
3. Contacts will be added to existing list

### Creating Backups

1. Click **💾 Backup** button
2. Timestamped backup file will be created
3. Format: `contacts_backup_YYYYMMDD_HHMMSS.json`

## 📸 Application Layout

```
┌────────────────────────────────────────────────────────────┐
│                    📇 CONTACT BOOK                         │
├──────────────────────────┬─────────────────────────────────┤
│  🔍 Search: [________]   │   Contact Details               │
│                          │                                 │
│  ┌───────────────────┐   │   Name:     [______________]   │
│  │ John Doe          │   │   Phone:    [______________]   │
│  │ Jane Smith        │   │   Email:    [______________]   │
│  │ Bob Johnson       │◄──┼─  Address:  [______________]   │
│  │ Alice Williams    │   │   Category: [Friend ▼]         │
│  │ ...               │   │   Notes:    [______________]   │
│  └───────────────────┘   │             [______________]   │
│                          │                                 │
│  Total Contacts: 15      │   [➕ Add]     [✏️ Update]     │
│                          │   [🗑️ Delete]  [🔄 Clear]      │
└──────────────────────────┴─────────────────────────────────┘
│ [📊 Export] [📥 Import] [💾 Backup] [ℹ️ About]            │
└────────────────────────────────────────────────────────────┘
```

## 🔧 Code Structure

### Main Components

```python
class ContactBook:
    def __init__(self, root)              # Initialize application
    def setup_ui(self)                    # Create GUI elements
    
    # File I/O Methods
    def load_contacts(self)               # Load from JSON
    def save_contacts(self)               # Save to JSON
    
    # CRUD Operations
    def add_contact(self)                 # CREATE
    def on_contact_select(self, event)    # READ
    def update_contact(self)              # UPDATE
    def delete_contact(self)              # DELETE
    
    # Data Management
    def validate_contact(self, contact)   # Validate data
    def refresh_contact_list(self)        # Update display
    def search_contacts(self)             # Filter contacts
    
    # Import/Export
    def export_to_csv(self)               # Export data
    def import_from_csv(self)             # Import data
    def backup_contacts(self)             # Create backup
    
    # UI Helpers
    def display_contact(self, contact)    # Show in form
    def clear_form(self)                  # Clear all fields
```

### Data Structure

```python
contact = {
    'name': 'John Doe',
    'phone': '+1-555-1234',
    'email': 'john@example.com',
    'address': '123 Main St, City',
    'category': 'Friend',
    'notes': 'Met at conference',
    'created_at': '2024-12-31 10:30:00',
    'updated_at': '2024-12-31 10:30:00'
}
```

### File Storage Format (JSON)

```json
[
    {
        "name": "John Doe",
        "phone": "+1-555-1234",
        "email": "john@example.com",
        "address": "123 Main St, City",
        "category": "Friend",
        "notes": "Met at conference",
        "created_at": "2024-12-31 10:30:00",
        "updated_at": "2024-12-31 10:30:00"
    },
    {
        "name": "Jane Smith",
        "phone": "+1-555-5678",
        "email": "jane@example.com",
        "address": "456 Oak Ave, Town",
        "category": "Work",
        "notes": "Project manager",
        "created_at": "2024-12-31 11:00:00",
        "updated_at": "2024-12-31 11:00:00"
    }
]
```

## 🎨 Customization

### Change Theme Colors

Modify colors in `setup_ui()`:

```python
# Current dark theme
bg_main = '#2c3e50'      # Main background
bg_panel = '#34495e'     # Panel background
fg_text = '#ecf0f1'      # Text color
accent = '#3498db'       # Accent color

# Light theme example
bg_main = '#ecf0f1'
bg_panel = '#ffffff'
fg_text = '#2c3e50'
accent = '#3498db'
```

### Add New Categories

In `setup_ui()` method:

```python
entry = ttk.Combobox(
    form_frame,
    values=["Family", "Friend", "Work", "Business", "School", "Other"],
    state='readonly'
)
```

### Add New Fields

1. Add to form fields list:
```python
fields = [
    # ... existing fields ...
    ("Website:", "website"),
    ("Birthday:", "birthday")
]
```

2. Update contact dictionary structure
3. Modify validation logic if needed

### Change Data File Location

```python
def __init__(self, root):
    # ...
    self.data_file = "path/to/your/contacts.json"
```

## 📚 File I/O Examples

### Reading JSON

```python
import json

# Load contacts from file
with open('contacts.json', 'r', encoding='utf-8') as file:
    contacts = json.load(file)

print(f"Loaded {len(contacts)} contacts")
```

### Writing JSON

```python
import json

# Save contacts to file
contacts = [
    {'name': 'John', 'phone': '555-1234'},
    {'name': 'Jane', 'phone': '555-5678'}
]

with open('contacts.json', 'w', encoding='utf-8') as file:
    json.dump(contacts, file, indent=4, ensure_ascii=False)
```

### CSV Export

```python
# Write to CSV
with open('contacts.csv', 'w', encoding='utf-8') as file:
    file.write("Name,Phone,Email\n")
    for contact in contacts:
        file.write(f'"{contact["name"]}","{contact["phone"]}","{contact["email"]}"\n')
```

### File Existence Check

```python
import os

if os.path.exists('contacts.json'):
    print("File exists")
else:
    print("File not found, creating new")
```

## 🐛 Troubleshooting

### File Permission Error

**Error:** `PermissionError: [Errno 13] Permission denied`

**Solution:**
- Ensure you have write permissions in the directory
- Close any programs that might have the file open
- Run with appropriate permissions

### JSON Decode Error

**Error:** `json.decoder.JSONDecodeError`

**Solution:**
- Check if `contacts.json` is valid JSON
- Delete corrupted file (backup first!)
- Let app create a new file

### Contact Not Saving

**Issue:** Changes don't persist after closing

**Solutions:**
- Check if `save_contacts()` is being called
- Verify file write permissions
- Look for error messages in console
- Check disk space

### Duplicate Contacts

**Issue:** Same contact appears multiple times

**Solution:**
- Use the duplicate detection warning
- Manually remove duplicates from JSON file
- Implement stronger duplicate checking

### Search Not Working

**Issue:** Search box doesn't filter contacts

**Solution:**
- Ensure `search_var.trace()` is set up correctly
- Check if `search_contacts()` is being called
- Verify search logic includes all fields

## 📖 CRUD Operations Explained

### CREATE (Add)

```python
def add_contact(self):
    # 1. Collect data from form
    contact = {
        'name': self.entries['name'].get(),
        # ... other fields
    }
    
    # 2. Validate data
    if not self.validate_contact(contact):
        return
    
    # 3. Add to list
    self.contacts.append(contact)
    
    # 4. Persist to file
    self.save_contacts()
    
    # 5. Update UI
    self.refresh_contact_list()
```

### READ (View)

```python
def on_contact_select(self, event):
    # 1. Get selection
    index = self.contact_listbox.curselection()[0]
    
    # 2. Retrieve data
    contact = self.contacts[index]
    
    # 3. Display in form
    self.display_contact(contact)
```

### UPDATE (Edit)

```python
def update_contact(self):
    # 1. Verify selection
    if self.selected_index is None:
        return
    
    # 2. Get updated data
    updated_contact = {
        'name': self.entries['name'].get(),
        # ... other fields
    }
    
    # 3. Validate
    if not self.validate_contact(updated_contact):
        return
    
    # 4. Update in list
    self.contacts[self.selected_index] = updated_contact
    
    # 5. Save changes
    self.save_contacts()
    
    # 6. Refresh display
    self.refresh_contact_list()
```

### DELETE (Remove)

```python
def delete_contact(self):
    # 1. Verify selection
    if self.selected_index is None:
        return
    
    # 2. Confirm action
    if not messagebox.askyesno("Confirm", "Delete?"):
        return
    
    # 3. Remove from list
    del self.contacts[self.selected_index]
    
    # 4. Save changes
    self.save_contacts()
    
    # 5. Clear form and refresh
    self.clear_form()
    self.refresh_contact_list()
```

## 📝 Project Files

```
contact-book-project/
├── contact_book.py        # Main application file
├── contacts.json          # Data file (auto-created)
├── README.md             # This file
└── backups/              # Backup directory (optional)
    ├── contacts_backup_20241231_120000.json
    └── contacts_backup_20241231_150000.json
```

## 💡 Tips for Beginners

1. **Start Simple**: Test with a few contacts first
2. **Backup Regularly**: Use the backup feature before major changes
3. **Validate Input**: Always check user input before saving
4. **Handle Errors**: Use try-except blocks for file operations
5. **Test Edge Cases**: Empty lists, invalid data, missing files
6. **Comment Your Code**: Explain complex logic
7. **Save Often**: Implement auto-save after each operation

## 🎯 Practice Challenges

1. **Add Photo Support**: Store contact photos
2. **Birthday Reminders**: Alert for upcoming birthdays
3. **Contact Groups**: Create and manage contact groups
4. **Email Integration**: Send emails directly from app
5. **Phone Formatting**: Auto-format phone numbers
6. **Dark/Light Theme**: Add theme toggle
7. **Undo Feature**: Implement undo for deletions
8. **Advanced Search**: Search with multiple criteria
9. **Export to VCard**: Export in vCard format
10. **Cloud Sync**: Sync contacts to cloud storage

## 🚀 Advanced Features to Add

### 1. Contact Groups
```python
contact = {
    'name': 'John Doe',
    'groups': ['Family', 'Work', 'Soccer Team']
}
```

### 2. Custom Fields
Allow users to add custom fields dynamically

### 3. Contact Merging
Detect and merge duplicate contacts

### 4. History Tracking
Keep history of all changes

### 5. Advanced Search
```python
def advanced_search(self, criteria):
    # Search by multiple fields
    # Support wildcards
    # Date range filtering
    pass
```

### 6. Data Encryption
Encrypt sensitive contact information

### 7. Multi-user Support
Support multiple user profiles

### 8. Import from VCard
Support vCard (.vcf) format

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional import/export formats
- Better validation
- More contact fields
- Cloud synchronization
- Mobile responsiveness
- Unit tests
- Documentation improvements

## 📄 License

This project is open source and available for educational purposes.

## 🌟 Acknowledgments

- Built with Python's tkinter
- JSON for data persistence
- Inspired by contact management systems

## 📚 Learning Resources

### File I/O
- [Python File I/O documentation](https://docs.python.org/3/tutorial/inputoutput.html)
- [Working with JSON in Python](https://docs.python.org/3/library/json.html)
- CSV file handling

### CRUD Operations
- Database design principles
- Data validation techniques
- Error handling strategies

### GUI Programming
- [tkinter documentation](https://docs.python.org/3/library/tkinter.html)
- Layout management
- Event-driven programming

---

**Happy Contact Managing! 📇✨**

Made with ❤️ for learning Python File I/O, CRUD, and Data Management