# To-Do List (text file storage) (Beginner Level)

def load_tasks(filename):
    try:
        with open(filename, 'r') as file:
            tasks = file.readlines()
        return [task.strip() for task in tasks]
    except FileNotFoundError:
        return []

def save_tasks(filename, tasks):
    with open(filename, 'w') as file:
        for task in tasks:
            file.write(f"{task}\n")

def add_task(filename, task):
    tasks = load_tasks(filename)
    tasks.append(task)
    save_tasks(filename, tasks)

def remove_task(filename, task):
    tasks = load_tasks(filename)
    tasks.remove(task)
    save_tasks(filename, tasks)

def mark_task(filename, task):
    tasks = load_tasks(filename)
    tasks[tasks.index(task)] = f"{task} [DONE]"
    save_tasks(filename, tasks)

# Example usage
filename = 'todo.txt'
add_task(filename, 'Buy groceries')
add_task(filename, 'Read a book')
remove_task(filename, 'Read a book')
mark_task(filename, 'Buy groceries')
