import tkinter as tk
from tkinter import ttk, messagebox
import random


class YDPRAutomaton:
    def __init__(self, root, size):
        self.root = root
        self.root.title("МОДЕЛЮВАННЯ ЙМОВІРНІСНИХ АВТОМАТІВ")

        # для вводу матриці
        self.matrix_entries = []

        # для вводу значень Z
        self.Z_entries = []

        # для вводу кількрсті тактів
        self.n_entry = 0

        # для виводу матриці В
        self.B_labels = []

        # для воводу ймовірностей того, що автомат закінчить свою роботу в певному стані
        self.prob_label = None

        # для виводу ймовірності того, що автомат закінчить свою роботу в стані, вихідний сигнал якого рівний 1
        self.prob_of_one_label = None

        self.size = size

        self.create_widgets()

    def get_matrix_data(self):
        m = [[0 for col in range(self.size)] for row in range(self.size)]
        for r, row in enumerate(self.matrix_entries):
            for c, entry in enumerate(row):
                text = entry.get()
                m[r][c] = float(text)
        # m = [[0, 0.1, 0, 0, 0, 0.1, 0.8],
        #      [0, 0, 0.6, 0.4, 0, 0, 0],
        #      [0, 0, 0.2, 0, 0, 0.7, 0.1],
        #      [0, 0, 0, 0, 0.8, 0.2, 0],
        #      [0, 0.5, 0.5, 0, 0, 0, 0],
        #      [0, 0.4, 0, 0, 0, 0.6, 0],
        #      [0, 0.5, 0, 0, 0, 0, 0.5]]
        return m

    def create_widgets(self):

        # підписуємо стовпці
        for c in range(self.size):
            l = tk.Label(self.root, text="z" + str(c))
            l.grid(row=0, column=c + 1, padx=5, pady=5)

        for r in range(self.size):
            entries_row = []

            # підписуємо колонки
            l = tk.Label(self.root, text="z" + str(r))
            l.grid(row=r + 1, column=0, padx=5, pady=5)
            for c in range(self.size):
                # додаємо поля для вводу матриці
                e = tk.Entry(self.root, width=5)
                e.insert('end', 0)
                e.grid(row=r + 1, column=c + 1, padx=5, pady=5)
                entries_row.append(e)
            self.matrix_entries.append(entries_row)

        l = tk.Label(self.root, text="Z = ")
        l.grid(row=self.size + 2, column=0, padx=5, pady=5)
        for c in range(self.size):
            # додаємо поля для вводу Z
            e = tk.Entry(self.root, width=5)
            e.insert('end', 0)
            e.grid(row=self.size + 2, column=c + 1, padx=5, pady=5)
            self.Z_entries.append(e)

        n_label = tk.Label(self.root, text="Кількість тактів: ")
        n_label.grid(row=self.size + 3, column=0, padx=5, pady=5)

        # додаємо поле для вводу кількості тактів
        e = tk.Entry(self.root, width=5)
        e.insert('end', 0)
        e.grid(row=self.size + 3, column=1, padx=5, pady=5)
        self.n_entry = e

        # додаємо кнопку, при її натисканні викликається метод simulate
        simulate_button = ttk.Button(self.root, text="Симулювати", command=self.simulate)
        simulate_button.grid(row=self.size + 4, column=self.size // 2, columnspan=self.size // 2, padx=5, pady=5)

        B_label = ttk.Label(self.root, text="Матриця В:")
        B_label.grid(row=0, column=self.size + 3, padx=5, pady=5, columnspan=self.size)

        # підготовлюємо місце для матриці В (додаємо пусті рядки)
        for i in range(self.size):
            self.B_labels.append(ttk.Label(self.root, text="", justify="left"))
            self.B_labels[i].grid(row=i + 1, column=self.size + 6, padx=5, pady=5, columnspan=self.size)

        # підготовлюємо місце для виводу ймовірностей
        prob_header = tk.Label(self.root, text="Ймовірності перебування автомата у станах")
        prob_header.grid(row=self.size + 3, column=self.size + 3, padx=5, pady=5, columnspan=self.size)
        prob_values = tk.Label(self.root, text="\t".join([f"z{i}" for i in range(self.size)]))
        prob_values.grid(row=self.size + 4, column=self.size + 3, padx=5, pady=5, columnspan=self.size)
        self.prob_label = tk.Label(self.root, text="")
        self.prob_label.grid(row=self.size + 5, column=self.size + 3, padx=5, pady=5, columnspan=self.size)

        self.prob_of_one_label = tk.Label(self.root, text="Йомвірність вихідного сигнала 1:")
        self.prob_of_one_label.grid(row=self.size + 7, column=self.size + 3, padx=5, pady=5, columnspan=self.size)

    def simulate(self):
        try:
            # торимуємо введені дані
            matrix = self.get_matrix_data()
            n = int(self.n_entry.get())
            Z = [int(entry.get()) for entry in self.Z_entries]

            curr_state = 0
            population = [i for i in range(self.size)]
            B = [[0 for col in range(self.size)] for row in range(self.size)]
            summ_of_cols = [0] * self.size
            summ_one = 0
            total = 0
            probabilities = "   "

            for _ in range(n):
                # вибираємо, в який стан перейти залежно від йомвірності
                next_state = random.choices(population, matrix[curr_state])[0]
                B[curr_state][next_state] += 1
                curr_state = next_state

            for i in range(0, self.size):
                for j in range(self.size):
                    summ_of_cols[i] += B[i][j]
                    B[i][j] = str(B[i][j])

                if Z[i] == 1:
                    summ_one += summ_of_cols[i]
                total += summ_of_cols[i]

            # виводимо результат роботи алгоритму
            for i in range(self.size):
                self.B_labels[i].config(text="\t".join(B[i]))

            self.prob_of_one_label.config(text=f"Йомвірність вихідного сигнала 1: {round(summ_one / total, 2)}")

            summ_of_cols[0] = 0
            for i in range(self.size):
                probabilities += "  " + str(round(summ_of_cols[i] / total, 2)) + "\t "
            self.prob_label.config(text=probabilities)

        except Exception as e:
            messagebox.showinfo("Помилка!!!", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x450")
    app = YDPRAutomaton(root, 7)
    root.mainloop()

# if __name__ == '__main__':
#     try:
#         A = [[0, 0.1, 0, 0, 0, 0.1, 0.8],
#              [0, 0, 0.6, 0.4, 0, 0, 0],
#              [0, 0, 0.2, 0, 0, 0.7, 0.1],
#              [0, 0, 0, 0, 0.8, 0.2, 0],
#              [0, 0.5, 0.5, 0, 0, 0, 0],
#              [0, 0.4, 0, 0, 0, 0.6, 0],
#              [0, 0.5, 0, 0, 0, 0, 0.5]]
#
#         Z = [0, 0, 0, 0, 1, 1, 1]
#         n = 150
#         YDPRAutomaton(A, Z, n)
#     except Exception as e:
#         print("Exeption:", e)
