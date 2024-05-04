from tkinter import *
from tkinter import ttk, messagebox
import tkinter as tk

import sqlite3

i = 0

COLOR_PROGRAM = "#a7a385"

root = Tk()
root.title("База данных | Tkinter & SQLite | Версия: 1.0")
root.geometry("680x430")
root["bg"] = COLOR_PROGRAM

row_start = 5
columns_treeview = "#1, #2, #3, #4"


class DB:
    def __init__(self):
        self.conn = sqlite3.connect("products.db")
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, color TEXT, articul TEXT)")
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def view(self):
        self.cur.execute("SELECT * FROM products")
        rows = self.cur.fetchall()
        return rows

    def insert(self, name, color, articul):
        insert_elements = (
            "INSERT INTO products (name, color, articul) VALUES (:name, :color, :articul)")
        self.cur.execute(insert_elements, {"name": name, "color": color, "articul": articul})
        self.conn.commit()

    def update(self, id, name, color, articul):
        self.cur.execute("UPDATE products SET name=?, color=?, articul=? WHERE id=?",
                         (name, color, articul, id,))
        self.conn.commit()

    def delete(self, id):
        self.cur.execute("DELETE FROM products WHERE id=?", (id,))
        self.conn.commit()


db = DB()


def view_command():
    # Очищаем все строки в Treeview
    for row in tree.get_children():
        tree.delete(row)

    # Проходим все записи в БД
    for row in db.view():
        # Добавляем запись в Treeview
        tree.insert("", "end", values=row)


def add_command():
    db.insert(entry_name.get(), entry_color.get(), entry_articul.get())
    view_command()


def delete_command():
    col = tree.focus()

    if col:
        id_num = tree.item(col)['values'][0]
        tree.delete(col)
        db.delete(id_num)
    else:
        messagebox.showerror("Ошибка", "Для начала нужно выбрать!")


def edit_command():
    col = tree.focus()

    if col:
        id_num = tree.item(col)['values'][0]
        db.update(id_num, entry_name.get(), entry_color.get(), entry_articul.get())
        view_command()
    else:
        messagebox.showerror("Ошибка", "Для начала нужно выбрать!")


""" Label Name Programm Text """
Label(text="База данных продуктов\n", font="Arial 22 bold", background=COLOR_PROGRAM, foreground="#000000").grid(row=row_start - 5, column=0, columnspan=6, sticky="ew")

''' Entry All '''
entry_name = tk.Entry()
entry_color = tk.Entry()
entry_articul = tk.Entry()

entry_name.grid(row=row_start - 3, column=0, sticky="ew", padx=(100, 0))
entry_color.grid(row=row_start - 2, column=0, sticky="ew", padx=(100, 0))
entry_articul.grid(row=row_start - 1, column=0, sticky="ew", padx=(100, 0))

''' Entry Text '''
entry_text_name = Label(root, text="Название:", font="Arial 11 bold", background=COLOR_PROGRAM)
entry_text_color = Label(root, text="Цвет:", font="Arial 11 bold", background=COLOR_PROGRAM)
entry_text_articul = Label(root, text="Артикул:", font="Arial 11 bold", background=COLOR_PROGRAM)

entry_text_name.grid(row=row_start - 3, column=0, sticky="w", padx=10)
entry_text_color.grid(row=row_start - 2, column=0, sticky="w", padx=10)
entry_text_articul.grid(row=row_start - 1, column=0, sticky="w", padx=10)
Label(root, text="", background=COLOR_PROGRAM).grid(row=row_start)

""" Treeview """
tree = ttk.Treeview(show="headings", columns=columns_treeview)
tree.grid(row=row_start + 1, column=0, columnspan=4, padx=10)

tree.heading("#1", text="#")
tree.heading("#2", text="Название")
tree.heading("#3", text="Цвет")
tree.heading("#4", text="Артикул")

tree.column("#1", width=30, anchor=tk.CENTER)

""" Scroll Bar Treeview """
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=row_start + 1, column=5, sticky='ns')

''' Button All '''
button_add = tk.Button(text="Добавить", command=add_command)
button_delete = tk.Button(text="Удалить", command=delete_command)
button_edit = tk.Button(text="Редактировать", command=edit_command)

button_add.grid(row=row_start - 4, column=3, rowspan=2, ipadx=10, sticky="e")
button_delete.grid(row=row_start - 4, column=3, rowspan=2, ipadx=10, sticky="w")
button_edit.grid(row=row_start - 2, column=3, rowspan=2, sticky="ew")

view_command()
root.mainloop()