# Advanced Level

"""
To-Do List Manager 
Task management with file persistence.
"""

import json
import os
from datetime import datetime


class TodoList:
    """Todo list manager with file storage."""
    
    def __init__(self, filename="todos.json"):
        """Initialize with file storage."""
        self.filename = filename
        self.tasks = self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_tasks(self):
        """Save tasks to file."""
        with open(self.filename, 'w') as f:
            json.dump(self.tasks, f, indent=2)
    
    def add_task(self, description, priority="medium"):
        """Add new task."""
        task = {
            "id": len(self.tasks) + 1,
            "description": description,
            "completed": False,
            "priority": priority,
            "created": datetime.now().isoformat(),
            "completed_at": None
        }
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def remove_task(self, task_id):
        """Remove task by ID."""
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        self.reindex_tasks()
        self.save_tasks()
    
    def mark_complete(self, task_id):
        """Mark task as complete."""
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                task["completed_at"] = datetime.now().isoformat()
                self.save_tasks()
                return True
        return False
    
    def mark_incomplete(self, task_id):
        """Mark task as incomplete."""
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = False
                task["completed_at"] = None
                self.save_tasks()
                return True
        return False
    
    def reindex_tasks(self):
        """Reindex task IDs after removal."""
        for i, task in enumerate(self.tasks, 1):
            task["id"] = i
    
    def get_all_tasks(self):
        """Get all tasks."""
        return self.tasks
    
    def get_pending_tasks(self):
        """Get incomplete tasks."""
        return [t for t in self.tasks if not t["completed"]]
    
    def get_completed_tasks(self):
        """Get completed tasks."""
        return [t for t in self.tasks if t["completed"]]
    
    def clear_completed(self):
        """Remove all completed tasks."""
        self.tasks = [t for t in self.tasks if not t["completed"]]
        self.reindex_tasks()
        self.save_tasks()


def display_tasks(tasks, title="Tasks"):
    """Display tasks in formatted table."""
    if not tasks:
        print(f"\n📋 {title}: None")
        return
    
    print(f"\n{'=' * 80}")
    print(f"📋 {title}")
    print("=" * 80)
    print(f"{'ID':<4} {'Status':<8} {'Priority':<10} {'Description'}")
    print("-" * 80)
    
    for task in tasks:
        status = "✓ Done" if task["completed"] else "○ Pending"
        priority_icons = {"high": "🔴", "medium": "🟡", "low": "🟢"}
        priority = f"{priority_icons.get(task['priority'], '')} {task['priority'].title()}"
        
        print(f"{task['id']:<4} {status:<8} {priority:<10} {task['description']}")
    
    print("=" * 80)
    
    # Statistics
    total = len(tasks)
    completed = sum(1 for t in tasks if t["completed"])
    pending = total - completed
    
    print(f"\nTotal: {total} | Completed: {completed} | Pending: {pending}")


def main():
    """Main program execution."""
    todo = TodoList()
    
    print("=" * 80)
    print("                        TO-DO LIST MANAGER")
    print("=" * 80)
    
    while True:
        print("\n" + "-" * 80)
        print("Options:")
        print("  1. View all tasks")
        print("  2. View pending tasks")
        print("  3. View completed tasks")
        print("  4. Add new task")
        print("  5. Mark task complete")
        print("  6. Mark task incomplete")
        print("  7. Remove task")
        print("  8. Clear completed tasks")
        print("  q. Quit")
        print("-" * 80)
        
        choice = input("\nYour choice: ").strip().lower()
        
        if choice == 'q':
            print("\n✓ All changes saved. Goodbye!")
            break
        
        try:
            if choice == '1':
                display_tasks(todo.get_all_tasks(), "All Tasks")
            
            elif choice == '2':
                display_tasks(todo.get_pending_tasks(), "Pending Tasks")
            
            elif choice == '3':
                display_tasks(todo.get_completed_tasks(), "Completed Tasks")
            
            elif choice == '4':
                description = input("\nTask description: ").strip()
                if not description:
                    print("❌ Description cannot be empty.")
                    continue
                
                print("\nPriority: 1) High  2) Medium  3) Low")
                priority_choice = input("Select (default: 2): ").strip()
                
                priority_map = {"1": "high", "2": "medium", "3": "low"}
                priority = priority_map.get(priority_choice, "medium")
                
                task = todo.add_task(description, priority)
                print(f"\n✓ Task #{task['id']} added successfully!")
            
            elif choice == '5':
                display_tasks(todo.get_pending_tasks(), "Pending Tasks")
                task_id = int(input("\nEnter task ID to mark complete: "))
                if todo.mark_complete(task_id):
                    print(f"\n✓ Task #{task_id} marked as complete!")
                else:
                    print(f"\n❌ Task #{task_id} not found.")
            
            elif choice == '6':
                display_tasks(todo.get_completed_tasks(), "Completed Tasks")
                task_id = int(input("\nEnter task ID to mark incomplete: "))
                if todo.mark_incomplete(task_id):
                    print(f"\n✓ Task #{task_id} marked as incomplete!")
                else:
                    print(f"\n❌ Task #{task_id} not found.")
            
            elif choice == '7':
                display_tasks(todo.get_all_tasks(), "All Tasks")
                task_id = int(input("\nEnter task ID to remove: "))
                confirm = input(f"Confirm removal of task #{task_id}? (y/n): ")
                if confirm.lower() == 'y':
                    todo.remove_task(task_id)
                    print(f"\n✓ Task #{task_id} removed!")
            
            elif choice == '8':
                completed_count = len(todo.get_completed_tasks())
                if completed_count == 0:
                    print("\n📋 No completed tasks to clear.")
                else:
                    confirm = input(f"\nClear {completed_count} completed task(s)? (y/n): ")
                    if confirm.lower() == 'y':
                        todo.clear_completed()
                        print(f"\n✓ Cleared {completed_count} completed task(s)!")
            
            else:
                print("\n❌ Invalid choice. Please try again.")
        
        except ValueError:
            print("\n❌ Invalid input. Please enter a number.")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()