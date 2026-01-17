"""
Simple Contact Book Application
Demonstrates: File I/O, CRUD Operations, Data Management, GUI (tkinter)
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import re
from datetime import datetime


class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        self.root.configure(bg='#2c3e50')
        
        # Data storage
        self.contacts = []
        self.data_file = "contacts.json"
        self.selected_index = None
        
        # Load existing contacts
        self.load_contacts()
        
        # Setup GUI
        self.setup_ui()
        
        # Display contacts
        self.refresh_contact_list()
        
    def setup_ui(self):
        """Create and configure GUI elements"""
        
        # Title Label
        title_label = tk.Label(
            self.root,
            text="📇 CONTACT BOOK",
            font=('Helvetica', 20, 'bold'),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_label.pack(pady=15)
        
        # Main Container
        main_container = tk.Frame(self.root, bg='#2c3e50')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left Panel - Contact List
        left_panel = tk.Frame(main_container, bg='#34495e', relief=tk.RAISED, bd=3)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Search Frame
        search_frame = tk.Frame(left_panel, bg='#34495e')
        search_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(
            search_frame,
            text="🔍 Search:",
            font=('Helvetica', 11),
            bg='#34495e',
            fg='#ecf0f1'
        ).pack(side=tk.LEFT, padx=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.search_contacts())
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Helvetica', 11),
            bg='#2c3e50',
            fg='#ecf0f1',
            insertbackground='white'
        )
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Contact List
        list_frame = tk.Frame(left_panel, bg='#34495e')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.contact_listbox = tk.Listbox(
            list_frame,
            font=('Courier', 10),
            bg='#2c3e50',
            fg='#ecf0f1',
            selectbackground='#3498db',
            selectforeground='white',
            yscrollcommand=scrollbar.set,
            height=15
        )
        self.contact_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.contact_listbox.yview)
        self.contact_listbox.bind('<<ListboxSelect>>', self.on_contact_select)
        
        # Contact count label
        self.count_label = tk.Label(
            left_panel,
            text="Total Contacts: 0",
            font=('Helvetica', 10),
            bg='#34495e',
            fg='#95a5a6'
        )
        self.count_label.pack(pady=5)
        
        # Right Panel - Contact Details and Form
        right_panel = tk.Frame(main_container, bg='#34495e', relief=tk.RAISED, bd=3)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Form Frame
        form_frame = tk.LabelFrame(
            right_panel,
            text="Contact Details",
            font=('Helvetica', 12, 'bold'),
            bg='#34495e',
            fg='#ecf0f1',
            relief=tk.GROOVE,
            bd=2
        )
        form_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Form Fields
        fields = [
            ("Name:", "name"),
            ("Phone:", "phone"),
            ("Email:", "email"),
            ("Address:", "address"),
            ("Category:", "category"),
            ("Notes:", "notes")
        ]
        
        self.entries = {}
        
        for i, (label_text, field_name) in enumerate(fields):
            tk.Label(
                form_frame,
                text=label_text,
                font=('Helvetica', 11),
                bg='#34495e',
                fg='#ecf0f1',
                anchor='w'
            ).grid(row=i, column=0, sticky='w', padx=10, pady=8)
            
            if field_name == "notes":
                entry = tk.Text(
                    form_frame,
                    font=('Helvetica', 10),
                    bg='#2c3e50',
                    fg='#ecf0f1',
                    insertbackground='white',
                    height=4,
                    width=30
                )
            elif field_name == "category":
                entry = ttk.Combobox(
                    form_frame,
                    font=('Helvetica', 10),
                    values=["Family", "Friend", "Work", "Other"],
                    state='readonly',
                    width=28
                )
                entry.set("Friend")
            else:
                entry = tk.Entry(
                    form_frame,
                    font=('Helvetica', 10),
                    bg='#2c3e50',
                    fg='#ecf0f1',
                    insertbackground='white',
                    width=30
                )
            
            entry.grid(row=i, column=1, padx=10, pady=8, sticky='ew')
            self.entries[field_name] = entry
        
        # Button Frame
        button_frame = tk.Frame(right_panel, bg='#34495e')
        button_frame.pack(pady=10, padx=10)
        
        # CRUD Buttons
        buttons = [
            ("➕ Add", self.add_contact, '#27ae60'),
            ("✏️ Update", self.update_contact, '#f39c12'),
            ("🗑️ Delete", self.delete_contact, '#e74c3c'),
            ("🔄 Clear", self.clear_form, '#95a5a6')
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                font=('Helvetica', 10, 'bold'),
                bg=color,
                fg='white',
                width=10,
                height=1,
                relief=tk.RAISED,
                bd=2,
                cursor='hand2'
            )
            btn.grid(row=i//2, column=i%2, padx=5, pady=5)
        
        # Bottom Menu Bar
        menu_frame = tk.Frame(self.root, bg='#34495e', relief=tk.RAISED, bd=2)
        menu_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        menu_buttons = [
            ("📊 Export CSV", self.export_to_csv),
            ("📥 Import CSV", self.import_from_csv),
            ("💾 Backup", self.backup_contacts),
            ("ℹ️ About", self.show_about)
        ]
        
        for text, command in menu_buttons:
            btn = tk.Button(
                menu_frame,
                text=text,
                command=command,
                font=('Helvetica', 9),
                bg='#3498db',
                fg='white',
                relief=tk.FLAT,
                cursor='hand2'
            )
            btn.pack(side=tk.LEFT, padx=5, pady=5)
        
    def load_contacts(self):
        """Load contacts from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as file:
                    self.contacts = json.load(file)
                print(f"✓ Loaded {len(self.contacts)} contacts")
            else:
                self.contacts = []
                print("✓ Starting with empty contact list")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load contacts: {str(e)}")
            self.contacts = []
    
    def save_contacts(self):
        """Save contacts to JSON file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as file:
                json.dump(self.contacts, file, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save contacts: {str(e)}")
            return False
    
    def validate_contact(self, contact):
        """Validate contact information"""
        # Name is required
        if not contact['name'].strip():
            messagebox.showwarning("Validation Error", "Name is required!")
            return False
        
        # Validate phone number (basic)
        if contact['phone'] and not re.match(r'^[\d\s\-\+\(\)]+$', contact['phone']):
            messagebox.showwarning("Validation Error", "Invalid phone number format!")
            return False
        
        # Validate email (basic)
        if contact['email']:
            email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(email_pattern, contact['email']):
                messagebox.showwarning("Validation Error", "Invalid email format!")
                return False
        
        return True
    
    def add_contact(self):
        """Add a new contact (CREATE)"""
        # Get form data
        contact = {
            'name': self.entries['name'].get().strip(),
            'phone': self.entries['phone'].get().strip(),
            'email': self.entries['email'].get().strip(),
            'address': self.entries['address'].get().strip(),
            'category': self.entries['category'].get(),
            'notes': self.entries['notes'].get('1.0', tk.END).strip(),
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Validate
        if not self.validate_contact(contact):
            return
        
        # Check for duplicate
        for existing in self.contacts:
            if existing['name'].lower() == contact['name'].lower():
                response = messagebox.askyesno(
                    "Duplicate Contact",
                    f"A contact with name '{contact['name']}' already exists.\nDo you want to add anyway?"
                )
                if not response:
                    return
        
        # Add contact
        self.contacts.append(contact)
        
        # Save to file
        if self.save_contacts():
            messagebox.showinfo("Success", f"Contact '{contact['name']}' added successfully!")
            self.clear_form()
            self.refresh_contact_list()
    
    def update_contact(self):
        """Update existing contact (UPDATE)"""
        if self.selected_index is None:
            messagebox.showwarning("No Selection", "Please select a contact to update!")
            return
        
        # Get form data
        contact = {
            'name': self.entries['name'].get().strip(),
            'phone': self.entries['phone'].get().strip(),
            'email': self.entries['email'].get().strip(),
            'address': self.entries['address'].get().strip(),
            'category': self.entries['category'].get(),
            'notes': self.entries['notes'].get('1.0', tk.END).strip(),
            'created_at': self.contacts[self.selected_index]['created_at'],
            'updated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Validate
        if not self.validate_contact(contact):
            return
        
        # Update contact
        self.contacts[self.selected_index] = contact
        
        # Save to file
        if self.save_contacts():
            messagebox.showinfo("Success", f"Contact '{contact['name']}' updated successfully!")
            self.refresh_contact_list()
    
    def delete_contact(self):
        """Delete selected contact (DELETE)"""
        if self.selected_index is None:
            messagebox.showwarning("No Selection", "Please select a contact to delete!")
            return
        
        contact_name = self.contacts[self.selected_index]['name']
        
        # Confirm deletion
        response = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete '{contact_name}'?\nThis action cannot be undone."
        )
        
        if response:
            # Delete contact
            del self.contacts[self.selected_index]
            
            # Save to file
            if self.save_contacts():
                messagebox.showinfo("Success", f"Contact '{contact_name}' deleted successfully!")
                self.clear_form()
                self.selected_index = None
                self.refresh_contact_list()
    
    def on_contact_select(self, event):
        """Handle contact selection from list (READ)"""
        selection = self.contact_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        
        # Get the actual contact index (accounting for search filter)
        display_text = self.contact_listbox.get(index)
        # Extract name from display text
        name = display_text.split(' - ')[0].strip()
        
        # Find contact by name
        for i, contact in enumerate(self.contacts):
            if contact['name'] == name:
                self.selected_index = i
                self.display_contact(contact)
                break
    
    def display_contact(self, contact):
        """Display contact details in form"""
        # Clear form first
        self.clear_form()
        
        # Fill form with contact data
        self.entries['name'].insert(0, contact['name'])
        self.entries['phone'].insert(0, contact['phone'])
        self.entries['email'].insert(0, contact['email'])
        self.entries['address'].insert(0, contact['address'])
        self.entries['category'].set(contact['category'])
        self.entries['notes'].insert('1.0', contact['notes'])
    
    def clear_form(self):
        """Clear all form fields"""
        self.entries['name'].delete(0, tk.END)
        self.entries['phone'].delete(0, tk.END)
        self.entries['email'].delete(0, tk.END)
        self.entries['address'].delete(0, tk.END)
        self.entries['category'].set("Friend")
        self.entries['notes'].delete('1.0', tk.END)
        self.selected_index = None
    
    def refresh_contact_list(self):
        """Refresh the contact list display"""
        self.contact_listbox.delete(0, tk.END)
        
        # Sort contacts by name
        sorted_contacts = sorted(self.contacts, key=lambda x: x['name'].lower())
        
        # Display contacts
        for contact in sorted_contacts:
            display_text = f"{contact['name']} - {contact['phone']} ({contact['category']})"
            self.contact_listbox.insert(tk.END, display_text)
        
        # Update count
        self.count_label.config(text=f"Total Contacts: {len(self.contacts)}")
    
    def search_contacts(self):
        """Search and filter contacts"""
        search_term = self.search_var.get().lower()
        
        self.contact_listbox.delete(0, tk.END)
        
        # Filter contacts
        filtered = [c for c in self.contacts if 
                   search_term in c['name'].lower() or
                   search_term in c['phone'].lower() or
                   search_term in c['email'].lower() or
                   search_term in c['category'].lower()]
        
        # Sort and display
        sorted_contacts = sorted(filtered, key=lambda x: x['name'].lower())
        
        for contact in sorted_contacts:
            display_text = f"{contact['name']} - {contact['phone']} ({contact['category']})"
            self.contact_listbox.insert(tk.END, display_text)
        
        # Update count
        self.count_label.config(text=f"Showing: {len(filtered)} / {len(self.contacts)}")
    
    def export_to_csv(self):
        """Export contacts to CSV file"""
        if not self.contacts:
            messagebox.showinfo("No Data", "No contacts to export!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"contacts_export_{datetime.now().strftime('%Y%m%d')}.csv"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as file:
                    # Write header
                    file.write("Name,Phone,Email,Address,Category,Notes,Created,Updated\n")
                    
                    # Write contacts
                    for contact in self.contacts:
                        line = f'"{contact["name"]}","{contact["phone"]}","{contact["email"]}",'
                        line += f'"{contact["address"]}","{contact["category"]}","{contact["notes"]}",'
                        line += f'"{contact["created_at"]}","{contact["updated_at"]}"\n'
                        file.write(line)
                
                messagebox.showinfo("Success", f"Exported {len(self.contacts)} contacts to CSV!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def import_from_csv(self):
        """Import contacts from CSV file"""
        filename = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                imported_count = 0
                with open(filename, 'r', encoding='utf-8') as file:
                    lines = file.readlines()[1:]  # Skip header
                    
                    for line in lines:
                        # Parse CSV line (basic parsing)
                        fields = line.strip().split('","')
                        fields = [f.strip('"') for f in fields]
                        
                        if len(fields) >= 6:
                            contact = {
                                'name': fields[0],
                                'phone': fields[1],
                                'email': fields[2],
                                'address': fields[3],
                                'category': fields[4],
                                'notes': fields[5],
                                'created_at': fields[6] if len(fields) > 6 else datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'updated_at': fields[7] if len(fields) > 7 else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                            
                            self.contacts.append(contact)
                            imported_count += 1
                
                if self.save_contacts():
                    messagebox.showinfo("Success", f"Imported {imported_count} contacts!")
                    self.refresh_contact_list()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import: {str(e)}")
    
    def backup_contacts(self):
        """Create a backup of contacts"""
        if not self.contacts:
            messagebox.showinfo("No Data", "No contacts to backup!")
            return
        
        backup_file = f"contacts_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(backup_file, 'w', encoding='utf-8') as file:
                json.dump(self.contacts, file, indent=4, ensure_ascii=False)
            
            messagebox.showinfo("Success", f"Backup created: {backup_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create backup: {str(e)}")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
        📇 Contact Book v1.0
        
        A simple contact management application
        
        Features:
        • Add, Update, Delete contacts
        • Search and filter
        • Export to CSV
        • Import from CSV
        • Automatic backups
        
        Demonstrates:
        • File I/O operations
        • CRUD operations
        • Data management
        • GUI programming
        
        Made with ❤️ for learning Python
        """
        messagebox.showinfo("About Contact Book", about_text)
    
    def run(self):
        """Start the application main loop"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Handle application closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()


def main():
    """Main function to run the contact book application"""
    root = tk.Tk()
    contact_book = ContactBook(root)
    contact_book.run()


if __name__ == "__main__":
    main()