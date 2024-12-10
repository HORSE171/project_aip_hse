import pytest
from unittest import mock
from io import StringIO
import tkinter as tk
from tkinter import messagebox
from finance import FinanceTrackerApp  # Импорт вашего приложения


# Тестирование метода add_income
def test_add_income_positive():
    root = tk.Tk()
    app = FinanceTrackerApp(root)

    # Имитация ввода значения
    app.amount_var.set("1000.0")

    with mock.patch("tkinter.messagebox.showerror") as mock_showerror:
        app.add_income()

    # Проверка баланса
    assert app.balance == 1000.0
    assert len(app.transactions) == 1
    assert app.transactions[0][1] == "Доход"
    assert app.transactions[0][2] == 1000.0


def test_add_income_negative():
    root = tk.Tk()
    app = FinanceTrackerApp(root)

    # Имитация ввода некорректного значения
    app.amount_var.set("-1000.0")

    with mock.patch("tkinter.messagebox.showerror") as mock_showerror:
        app.add_income()

    # Проверка баланса (он не должен измениться)
    assert app.balance == 0.0
    mock_showerror.assert_called_once_with("Ошибка", "Введите корректную сумму.")


# Тестирование метода add_expense
def test_add_expense_positive():
    root = tk.Tk()
    app = FinanceTrackerApp(root)

    # Устанавливаем начальный баланс
    app.balance = 1000.0
    app.amount_var.set("500.0")

    with mock.patch("tkinter.messagebox.showerror") as mock_showerror:
        app.add_expense()

    # Проверка баланса
    assert app.balance == 500.0
    assert len(app.transactions) == 1
    assert app.transactions[0][1] == "Еда"  # Проверка, что категория по умолчанию - "Еда"
    assert app.transactions[0][2] == -500.0


def test_add_expense_negative():
    root = tk.Tk()
    app = FinanceTrackerApp(root)

    # Устанавливаем начальный баланс
    app.balance = 1000.0
    app.amount_var.set("-500.0")

    with mock.patch("tkinter.messagebox.showerror") as mock_showerror:
        app.add_expense()

    # Проверка, что ошибка была показана
    assert app.balance == 1000.0
    mock_showerror.assert_called_once_with("Ошибка", "Введите корректную сумму.")


# Тестирование метода update_balance
def test_update_balance():
    root = tk.Tk()
    app = FinanceTrackerApp(root)

    app.balance = 1000.0
    app.update_balance()

    assert app.balance_label.cget("text") == "Текущий баланс: 1000.00 руб"


# Тестирование метода show_expenses_chart
def test_show_expenses_chart():
    root = tk.Tk()
    app = FinanceTrackerApp(root)

    # Добавление нескольких транзакций
    app.add_transaction("Еда", -300.0)
    app.add_transaction("Транспорт", -200.0)

    with mock.patch("matplotlib.pyplot.show") as mock_show:
        app.show_expenses_chart()
        mock_show.assert_called_once()


# Тестирование сохранения транзакции в CSV
def test_save_transaction():
    root = tk.Tk()
    app = FinanceTrackerApp(root)

    # Имитация транзакции
    app.add_transaction("Доход", 1000.0)

    with open("transactions.csv", mode="r", encoding="utf-8") as file:
        lines = file.readlines()
        assert len(lines) > 0
        assert "Доход" in lines[0]
        assert "1000.0" in lines[0]
