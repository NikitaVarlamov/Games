from tkinter import *
from tkinter import messagebox


class LoanCalculator:
    def __init__(self):
        # Создание окна
        self.window = Tk()
        self.window.title("Кредитный калькулятор")

        # Создание параметров расчета и полей ввода
        Label(self.window, text="Годовая процентная ставка").grid(
            row=1, column=1, sticky=W, padx=10, pady=5)
        Label(self.window, text="Количество лет").grid(
            row=2, column=1, sticky=W, padx=10, pady=5)
        Label(self.window, text="Сумма кредита").grid(
            row=3, column=1, sticky=W, padx=10, pady=5)
        Label(self.window, text="Ежемесячный платеж").grid(
            row=4, column=1, sticky=W, padx=10, pady=5)
        Label(self.window, text="Общая сумма кредита").grid(
            row=5, column=1, sticky=W, padx=10, pady=5)

        # Переменные
        self.annualInterestRateVar = StringVar()
        self.numberOfYearsVar = StringVar()
        self.loanAmountVar = StringVar()
        self.monthlyPaymentVar = StringVar()
        self.totalPaymentVar = StringVar()

        # Создание полей ввода
        Entry(self.window, textvariable=self.annualInterestRateVar,
              justify=RIGHT).grid(row=1, column=2, padx=10, pady=5)
        Entry(self.window, textvariable=self.numberOfYearsVar,
              justify=RIGHT).grid(row=2, column=2, padx=10, pady=5)
        Entry(self.window, textvariable=self.loanAmountVar,
              justify=RIGHT).grid(row=3, column=2, padx=10, pady=5)

        # Ячейки вывода информации
        Label(self.window, textvariable=self.monthlyPaymentVar).grid(
            row=4, column=2, sticky=E, padx=10, pady=5)
        Label(self.window, textvariable=self.totalPaymentVar).grid(
            row=5, column=2, sticky=E, padx=10, pady=5)

        # Кнопка активации расчета
        Button(self.window, text="Вычислить платеж", command=self.computePayment).grid(
            row=6, column=2, sticky=E, padx=10, pady=10)

        self.window.mainloop()

    # Функции расчета
    def computePayment(self):
        try:
            # Получение значений из поля ввода
            loanAmount = float(self.loanAmountVar.get())
            annualInterestRate = float(self.annualInterestRateVar.get()) / 1200
            numberOfYears = int(self.numberOfYearsVar.get())

            # Подсчет ежемесячного платежа
            monthlyPayment = self.getMonthlyPayment(
                loanAmount, annualInterestRate, numberOfYears)

            # Обновление информации о ежемесячной и общей сумме кредита
            self.monthlyPaymentVar.set(format(monthlyPayment, '10.2f'))
            totalPayment = monthlyPayment * 12 * numberOfYears
            self.totalPaymentVar.set(format(totalPayment, '10.2f'))

        # Обработка ошибки ввода информации
        except ValueError:
            messagebox.showerror(
                "Input Error", "Ошибка при вводе информации. Пожалуйста, проверьте данные.")

    # Вспомогательная функция подсчета ежемесячного платежа
    def getMonthlyPayment(self, loanAmount, monthlyInterestRate, numberOfYears):
        return loanAmount * monthlyInterestRate / (1 - (1 / (1 + monthlyInterestRate) ** (numberOfYears * 12)))


# Запуск программы
LoanCalculator()
