from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Combobox
import tkinter as tk
from tkinter import messagebox
import json


def clear_view():
    for slave in tk.grid_slaves():
        slave.destroy()


def render_main_view():
    clear_view()
    tk.geometry('250x70')
    button = Button(tk, text="List all tasks", command=render_list_tasks_view).grid(column=2, row=0, padx=20, pady=20)
    button2 = Button(tk, text='Create new task', command=render_create_view).grid(column=0, row=0, padx=20, pady=20)


def create_task(name, description, priority):
    try:
        with open('db.txt', 'r') as file:
            tasks = json.loads(file.read())
            task = {'name': name, 'description': description, 'priority': priority_mapper[priority]}
            tasks.append(task)
            with open('db.txt', 'w') as file:
                json.dump(tasks, file)
            render_main_view()
    except:
        tasks = []
        task = {'name': name, 'description': description, 'priority': priority_mapper[priority]}
        tasks.append(task)
        with open('db.txt', 'w') as file:
            json.dump(tasks, file)
        render_main_view()


def render_create_view():
    clear_view()
    tk.geometry('700x350')
    Label(tk, text="Enter your Task's name").grid(column=0, row=0, padx=10, pady=20)
    task_name = Entry(tk)
    task_name.grid(column=1, row=0, padx=10, pady=20)
    Label(tk, text="Enter your comment:").grid(column=0, row=1)
    comment_entry = ScrolledText(tk, width=25, height=1)
    comment_entry.grid(column=1, row=1, padx=10, pady=20)
    Button(tk, text="Apply changes", bg='grey', fg='black', command=lambda:create_task(task_name.get(), comment_entry.get('1.0', END), task_priority.get())).grid(column=1, row=4, padx=10, pady=10)
    Label(tk, text='Priority:').grid(column=0, row=3, padx=10, pady=10)
    task_priority = IntVar()
    radio_button = Radiobutton(tk, text='Low', value=1, variable=task_priority)
    radio_button.grid(column=1, row=3, padx=20, pady=10)
    radio_button2 = Radiobutton(tk, text='Mid', value=2, variable=task_priority)
    radio_button2.grid(column=2, row=3, padx=20, pady=10)
    radio_button3 = Radiobutton(tk, text='High', value=3, variable=task_priority)
    radio_button3.grid(column=3, row=3, padx=20, pady=10)


def delete_task(task):
    ans = messagebox.askquestion('Confirm delete', 'Are you sure?')
    if ans == 'no':
        return
    if task:
        task_as_abject = eval(task)
        with open('db.txt', 'r+') as file:
            all_tasks = json.loads(file.read())
            for index in range(len(all_tasks)):
                if all_tasks[index]['name'] == task_as_abject['name']:
                    break
            del all_tasks[index]
            file.truncate(0)
            file.seek(0)
            json.dump(all_tasks, file)
    render_main_view()


def render_list_tasks_view():
    clear_view()
    tk.geometry('700x250')
    with open('db.txt', 'r') as file:
        tasks = json.loads(file.read())
    selected_task = StringVar(tk)
    dropdown = Combobox(tk, textvariable=selected_task, width=100)
    dropdown['values'] = tasks
    dropdown.grid(column=0, row=0, pady=10, padx=20)
    Button(tk, text='  Delete ', bg='red', command=lambda: delete_task(selected_task.get())).grid(column=0, row=1, pady=10)
    Button(tk, text='Find Task', command=find_task).grid(column=0, row=2, pady=10)
    Button(tk, text=' <Back>  ', command=render_main_view).grid(column=0, row=3, padx=10, pady=20)


def find_task():
    clear_view()
    search_name = Entry(tk)
    search_name.grid(column=0, row=0, pady=10, padx=20)
    Button(tk, text=' <Back> ', command=render_list_tasks_view).grid(column=2, row=0, padx=10, pady=20)
    Button(tk, text="Search Now", command=lambda: search(search_name.get())).grid(column=1, row=0, padx=10, pady=20)


def search(name):
    found = False
    with open('db.txt', 'r') as file:
        list_of_task = json.loads(file.read())
        for i in range(len(list_of_task)):
            if list_of_task[i]['name'] == name:
                found = True
                position = i+1
        if found:
            messagebox.showinfo('Info', f'Found on position: {position}')
            find_task()
        else:
            messagebox.showinfo('Info', '404: Not Found!')
            find_task()


priority_mapper = {1: 'Low', 2: 'Med', 3: 'High'}
all_tasks = []

if __name__ == '__main__':
    tk = tk.Tk()
    tk.title('Task Manager')
    tk.geometry('250x70')
    render_main_view()
    tk.mainloop()