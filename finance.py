import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime
import matplotlib.pyplot as plt


class FinanceTrackerApp:
    """Приложение для управления личными финансами.

    Атрибуты:
        root (tk.Tk): Главное окно приложения.
        balance (float): Текущий баланс.
        transactions (list): Список транзакций.
        amount_var (tk.StringVar): Переменная для ввода суммы.
        category_var (tk.StringVar): Переменная для выбора категории.
        balance_label (ttk.Label): Виджет для отображения баланса.
        transactions_tree (ttk.Treeview): Виджет для отображения истории транзакций.
    """

    def __init__(self, root):
        """Инициализация приложения.

        Аргументы:
            root (tk.Tk): Главное окно приложения.
        """
        self.root = root
        self.root.title("Личный Финансовый Трекер")
        self.root.geometry("600x500")

        # Баланс
        self.balance = 0.0
        # Список транзакций
        self.transactions = []

        # Интерфейс
        self.create_widgets()

    def create_widgets(self):
        """Создание элементов управления в интерфейсе.

        Эта функция создает все элементы интерфейса, включая поля для ввода,
        кнопки и виджеты для отображения баланса и истории транзакций.
        """
        # Фрейм для управления
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill="x")

        # Поле ввода для суммы
        self.amount_var = tk.StringVar()
        ttk.Label(control_frame, text="Сумма:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(control_frame, textvariable=self.amount_var, width=20).grid(
            row=0, column=1, padx=5, pady=5
        )

        # Категории
        self.category_var = tk.StringVar(value="Доход")
        categories = ["Доход", "Еда", "Транспорт", "Развлечения", "Одежда", "Здоровье"]
        ttk.Label(control_frame, text="Категория:").grid(
            row=1, column=0, padx=5, pady=5
        )
        ttk.Combobox(
            control_frame, textvariable=self.category_var, values=categories, width=18
        ).grid(row=1, column=1, padx=5, pady=5)

        # Кнопки для добавления дохода/расхода
        ttk.Button(control_frame, text="Добавить Доход", command=self.add_income).grid(
            row=2, column=0, padx=5, pady=10
        )
        ttk.Button(
            control_frame, text="Добавить Расход", command=self.add_expense
        ).grid(row=2, column=1, padx=5, pady=10)

        # Фрейм для отображения баланса и истории транзакций
        display_frame = ttk.Frame(self.root, padding="10")
        display_frame.pack(fill="x")

        self.balance_label = ttk.Label(
            display_frame,
            text=f"Текущий баланс: {self.balance:.2f} руб",
            font=("Arial", 14),
        )
        self.balance_label.pack(padx=5, pady=10)

        # История транзакций
        self.transactions_tree = ttk.Treeview(
            display_frame, columns=("Дата", "Категория", "Сумма"), show="headings"
        )
        self.transactions_tree.heading("Дата", text="Дата")
        self.transactions_tree.heading("Категория", text="Категория")
        self.transactions_tree.heading("Сумма", text="Сумма")
        self.transactions_tree.pack(fill="both", expand=True)

        # Кнопка для построения графика
        ttk.Button(
            self.root, text="Показать График Расходов", command=self.show_expenses_chart
        ).pack(pady=10)

    def add_income(self):
        """Добавление дохода.

        Эта функция добавляет доход к текущему балансу и записывает транзакцию.

        Аргументы:
            Нет.

        Возвращаемое значение:
            Нет.
        """
        try:
            amount = float(self.amount_var.get())
            if amount <= 0:
                raise ValueError
            self.balance += amount
            self.update_balance()
            self.add_transaction("Доход", amount)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную сумму.")

    def add_expense(self):
        """Добавление расхода.

        Эта функция добавляет расход к текущему балансу и записывает транзакцию.

        Аргументы:
            Нет.

        Возвращаемое значение:
            Нет.
        """
        try:
            amount = float(self.amount_var.get())
            if amount <= 0:
                raise ValueError
            self.balance -= amount
            self.update_balance()
            category = self.category_var.get()
            self.add_transaction(category, -amount)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную сумму.")

    def update_balance(self):
        """Обновление отображения баланса.

        Эта функция обновляет текстовое поле, отображающее текущий баланс.

        Аргументы:
            Нет.

        Возвращаемое значение:
            Нет.
        """
        self.balance_label.config(text=f"Текущий баланс: {self.balance:.2f} руб")

    def add_transaction(self, category, amount):
        """Добавление транзакции в историю и сохранение в файл.

        Аргументы:
            category (str): Категория транзакции (например, "Доход" или "Еда").
            amount (float): Сумма транзакции.

        Возвращаемое значение:
            Нет.
        """
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transactions_tree.insert(
            "", "end", values=(date, category, f"{amount:.2f} руб")
        )
        self.transactions.append((date, category, amount))
        self.save_transaction(date, category, amount)

    def save_transaction(self, date, category, amount):
        """Сохранение транзакции в CSV файл.

        Аргументы:
            date (str): Дата транзакции.
            category (str): Категория транзакции.
            amount (float): Сумма транзакции.

        Возвращаемое значение:
            Нет.
        """
        with open("transactions.csv", mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([date, category, amount])

    def show_expenses_chart(self):
        """Показать график расходов по категориям.

        Эта функция создает и отображает график расходов по категориям на основе
        всех записанных транзакций.

        Аргументы:
            Нет.

        Возвращаемое значение:
            Нет.
        """
        categories = {}
        for transaction in self.transactions:
            date, category, amount = transaction
            if category != "Доход":
                if category not in categories:
                    categories[category] = 0
                categories[category] += abs(amount)

        if categories:
            plt.figure(figsize=(7, 5))
            plt.pie(
                categories.values(),
                labels=categories.keys(),
                autopct="%1.1f%%",
                startangle=90,
            )
            plt.title("Расходы по Категориям")
            plt.axis("equal")  # Чтобы график был круглый
            plt.show()
        else:
            messagebox.showinfo("Информация", "У вас нет расходов для отображения.")


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceTrackerApp(root)

    # Запуск главного цикла обработки событий
    # Этот метод запускает основной цикл событий в приложении Tkinter,
    # позволяя взаимодействовать с пользователем через графический интерфейс.
    # Не имеет возвращаемого значения.
    root.mainloop()
