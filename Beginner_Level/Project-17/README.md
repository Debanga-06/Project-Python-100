# To-Do List Application ![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=yellow)
![Python Logo](https://www.python.org/static/community_logos/python-logo.png)

A feature-rich **To-Do List Manager** written in Python with persistent storage using JSON.  
Manage your daily tasks efficiently with priority levels, completion tracking, and more!

---

## 📌 Features

- ➕ **Add Tasks** - Create new tasks with title, description, and priority
- 📋 **View Tasks** - Display all tasks with status and priority indicators
- ✅ **Mark Complete** - Mark tasks as done
- ❌ **Delete Tasks** - Remove tasks from your list
- 🔍 **Search Tasks** - Find tasks by keyword
- 💾 **Persistent Storage** - All tasks saved automatically in JSON format
- 🎨 **Color-coded Priorities** - High (🔴), Medium (🟡), Low (🟢)

---

## 🖥️ Code Structure

The application consists of:
- **ToDoList Class** - Main class handling all task operations
- **JSON Storage** - Tasks stored in `tasks.json` file
- **Interactive Menu** - User-friendly command-line interface

---

## 🚀 How to Run

### 1. Make sure you have Python 3 installed
Check using:
```bash
python --version
```
or
```bash
python3 --version
```

### 2. Run the program
```bash
python todo.py
```
or
```bash
python3 todo.py
```

### 3. Use the Interactive Menu
```
=====================================
    📝 TO-DO LIST MANAGER
=====================================
1. Add Task
2. View All Tasks
3. Mark Task as Complete
4. Delete Task
5. Search Tasks
6. Exit
=====================================
```

---

## 📖 Usage Examples

### Adding a Task
```
Choose an option: 1
Enter task title: Buy groceries
Enter description (optional): Milk, eggs, bread
Enter priority (high/medium/low): high
✅ Task 'Buy groceries' added successfully!
```

### Viewing Tasks
```
======================================================================
📋 YOUR TO-DO LIST
======================================================================

[1] ○ 🔴 Buy groceries
    Description: Milk, eggs, bread
    Priority: high | Created: 2024-12-09 10:30:00

[2] ✓ 🟡 Complete Python project
    Description: Finish to-do list app
    Priority: medium | Created: 2024-12-08 15:20:00
```

### Marking as Complete
```
Enter task ID to mark complete: 1
✅ Task 'Buy groceries' marked as complete!
```

---

## 📂 Folder Structure

```
To-Do-List/
   ├── todo.py          # Main Python script
   ├── tasks.json       # JSON file for storing tasks (auto-generated)
   └── README.md        # Documentation
```

---

## 🎯 Task Properties

Each task contains:
- **ID** - Unique identifier
- **Title** - Task name
- **Description** - Optional details
- **Priority** - High, Medium, or Low
- **Status** - Completed or Pending
- **Created At** - Timestamp of creation

---

## ✅ Purpose

- Learn file handling in Python (JSON)
- Practice object-oriented programming
- Build a practical CLI application
- Understand CRUD operations (Create, Read, Update, Delete)
- Manage daily tasks efficiently

---

## 🛠️ Technologies Used

- **Python 3.x** - Programming language
- **JSON** - Data storage format
- **datetime** - Timestamp management
- **os** - File system operations

---

## 🔮 Future Enhancements

- [ ] Add due dates and reminders
- [ ] Category/tag system for tasks
- [ ] Export tasks to CSV
- [ ] GUI version using Tkinter
- [ ] Task statistics and analytics
- [ ] Multi-user support

---

## 👨‍💻 Author

**Developed by Debanga**

---

## 📝 License

This project is open source and available for educational purposes.

---

## 🤝 Contributing

Feel free to fork this project and add your own features!

---

**Happy Task Managing! 📝✨**