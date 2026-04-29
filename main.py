import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os
from datetime import datetime

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Файл истории
        self.history_file = "history.json"
        self.history = self.load_history()
        
        # Переменные
        self.length_var = tk.IntVar(value=12)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        
        self.create_widgets()
        self.update_history_table()
    
    def create_widgets(self):
        # Рамка настроек
        settings_frame = ttk.LabelFrame(self.root, text="Настройки пароля", padding=10)
        settings_frame.pack(fill="x", padx=10, pady=5)
        
        # Ползунок длины
        ttk.Label(settings_frame, text="Длина пароля:").grid(row=0, column=0, sticky="w")
        self.length_label = ttk.Label(settings_frame, text="12")
        self.length_label.grid(row=0, column=2, padx=5)
        
        self.length_slider = ttk.Scale(settings_frame, from_=4, to=64, orient="horizontal",
                                       variable=self.length_var, command=self.update_length_label)
        self.length_slider.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Чекбоксы
        ttk.Checkbutton(settings_frame, text="Цифры (0-9)", variable=self.use_digits).grid(row=1, column=0, sticky="w", pady=2)
        ttk.Checkbutton(settings_frame, text="Буквы (A-Z, a-z)", variable=self.use_letters).grid(row=1, column=1, sticky="w", pady=2)
        ttk.Checkbutton(settings_frame, text="Спецсимволы (!@#$%^&*()_+-=[]{}|;:,.<>?)", variable=self.use_symbols).grid(row=1, column=2, sticky="w", pady=2)
        
        # Кнопка генерации
        generate_btn = ttk.Button(settings_frame, text="Сгенерировать пароль", command=self.generate_password)
        generate_btn.grid(row=2, column=0, columnspan=3, pady=10)
        
        # Поле для отображения пароля
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(settings_frame, textvariable=self.password_var, font=("Courier", 12), state="readonly")
        password_entry.grid(row=3, column=0, columnspan=3, sticky="ew", pady=5)
        
        # Кнопка копирования
        copy_btn = ttk.Button(settings_frame, text="Копировать", command=self.copy_to_clipboard)
        copy_btn.grid(row=4, column=0, columnspan=3, pady=5)
        
        settings_frame.columnconfigure(1, weight=1)
        
        # Рамка истории
        history_frame = ttk.LabelFrame(self.root, text="История паролей", padding=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Таблица истории
        columns = ("timestamp", "password", "length", "charset")
        self.tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=10)
        
        self.tree.heading("timestamp", text="Дата и время")
        self.tree.heading("password", text="Пароль")
        self.tree.heading("length", text="Длина")
        self.tree.heading("charset", text="Набор символов")
        
        self.tree.column("timestamp", width=150)
        self.tree.column("password", width=250)
        self.tree.column("length", width=60)
        self.tree.column("charset", width=150)
        
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Кнопки управления историей
        btn_frame = ttk.Frame(history_frame)
        btn_frame.pack(fill="x", pady=5)
      ttk.Button(btn_frame, text="Очистить историю", command=self.clear_history).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Обновить", command=self.update_history_table).pack(side="left", padx=2)
    
    def update_length_label(self, value):
        self.length_label.config(text=str(int(float(value))))
    
    def get_character_set(self):
        chars = ""
        if self.use_digits.get():
            chars += string.digits
        if self.use_letters.get():
            chars += string.ascii_letters
        if self.use_symbols.get():
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        return chars
    
    def generate_password(self):
        length = self.length_var.get()
        chars = self.get_character_set()
        
        # Проверка корректности ввода
        if not chars:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов!")
            return
        
        if length < 4:
            messagebox.showerror("Ошибка", "Минимальная длина пароля - 4 символа!")
            return
        
        if length > 64:
            messagebox.showerror("Ошибка", "Максимальная длина пароля - 64 символа!")
            return
        
        # Генерация пароля
        password = ''.join(random.choice(chars) for _ in range(length))
        self.password_var.set(password)
        
        # Сохранение в историю
        charset_desc = []
        if self.use_digits.get(): charset_desc.append("цифры")
        if self.use_letters.get(): charset_desc.append("буквы")
        if self.use_symbols.get(): charset_desc.append("спецсимволы")
        
        self.save_to_history(password, length, ", ".join(charset_desc))
        self.update_history_table()
    
    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена!")
        else:
            messagebox.showwarning("Предупреждение", "Нет пароля для копирования!")
    
    def save_to_history(self, password, length, charset_desc):
        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "password": password,
            "length": length,
            "charset": charset_desc
        }
        self.history.append(record)
        
        # Ограничим историю 50 записями
        if len(self.history) > 50:
            self.history = self.history[-50:]
        
        self.save_history()
    
    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self):
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def update_history_table(self):
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Добавляем записи
        for record in reversed(self.history):  # Показываем новые сверху
            self.tree.insert("", "end", values=(
                record["timestamp"],
                record["password"],
                record["length"],
                record["charset"]
            ))
    
    def clear_history(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.history = []
            self.save_history()
            self.update_history_table()
            messagebox.showinfo("Успех", "История очищена!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
