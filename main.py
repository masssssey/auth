import tkinter as tk
from tkinter import messagebox
import sqlite3

# Функция для создания базы данных и таблицы пользователей
def create_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Функция для регистрации пользователя
def register_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        messagebox.showinfo("Успех", "Регистрация прошла успешно!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Ошибка", "Пользователь с таким именем уже существует.")
    finally:
        conn.close()

# Функция для авторизации пользователя
def login_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        messagebox.showinfo("Успех", "Авторизация прошла успешно!")
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль.")

# Окно регистрации
def open_registration_window():
    reg_window = tk.Toplevel(root)
    reg_window.title("Регистрация")

    tk.Label(reg_window, text="Логин:").pack()
    username_entry = tk.Entry(reg_window)
    username_entry.pack()

    tk.Label(reg_window, text="Пароль:").pack()
    password_entry = tk.Entry(reg_window, show='*')
    password_entry.pack()

    tk.Button(reg_window, text="Зарегистрироваться", command=lambda: register_user(username_entry.get(), password_entry.get())).pack()

# Основное окно приложения
root = tk.Tk()
root.title("Авторизация")

create_database()

tk.Label(root, text="Логин:").pack()
username_entry = tk.Entry(root)
username_entry.pack()

tk.Label(root, text="Пароль:").pack()
password_entry = tk.Entry(root, show='*')
password_entry.pack()

tk.Button(root, text="Войти", command=lambda: login_user(username_entry.get(), password_entry.get())).pack()
tk.Button(root, text="Регистрация", command=open_registration_window).pack()

root.mainloop()
