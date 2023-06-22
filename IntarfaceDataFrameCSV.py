import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd

# Создаем главное окно
window = tk.Tk()

# Настраиваем окно
window.title("Интерфейс DataFrame")
window.geometry("800x400")

# Создаем левый фрейм для выбора файла и загрузки данных
left_frame = ttk.Frame(window)
left_frame.pack(side="left", padx=10, pady=10)

# Создаем переменную для хранения DataFrame
dataframes = {}


# Функция, вызываемая при нажатии кнопки выбора файла
def choose_file():
    filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    file_entry.delete(0, tk.END)
    file_entry.insert(0, filepath)


# Функция, вызываемая при нажатии кнопки загрузки данных
def load_data():
    filepath = file_entry.get()
    if filepath:
        try:
            dataframe = pd.read_csv(filepath)
            filename = filepath.split("/")[-1]  # Исправьте на "\\" для Windows
            dataframes[filename] = dataframe
            dataframe_dropdown["values"] = list(dataframes.keys())
        except pd.errors.EmptyDataError:
            messagebox.showerror("Ошибка", "Выбранный файл пустой.")
        except pd.errors.ParserError:
            messagebox.showerror("Ошибка", "Ошибка при чтении файла CSV.")
    else:
        messagebox.showerror("Ошибка", "Выберите файл CSV.")


# Функция, вызываемая при выборе DataFrame из выпадающего списка
def display_dataframe():
    selected_dataframe = dataframe_var.get()
    if selected_dataframe in dataframes:
        display_df(dataframes[selected_dataframe])


# Функция для вывода DataFrame в правом фрейме
def display_df(dataframe):
    # Очищаем правый фрейм
    for widget in right_frame.winfo_children():
        widget.destroy()

    # Создаем виджет Treeview для отображения DataFrame
    treeview = ttk.Treeview(right_frame)
    treeview["columns"] = list(dataframe.columns)

    # Устанавливаем заголовки столбцов
    for column in dataframe.columns:
        treeview.heading(column, text=column)

    # Вставляем данные из DataFrame в Treeview
    for _, row in dataframe.iterrows():
        treeview.insert("", tk.END, values=list(row))

    # Размещаем Treeview в правом фрейме
    treeview.pack()


# Создаем кнопку выбора файла
choose_button = ttk.Button(left_frame, text="Выбрать файл", command=choose_file)
choose_button.pack()

# Создаем поле ввода и кнопку загрузки данных
file_entry = ttk.Entry(left_frame)
file_entry.pack()

load_button = ttk.Button(left_frame, text="Загрузить", command=load_data)
load_button.pack()

# Создаем правый фрейм для вывода DataFrame
right_frame = ttk.Frame(window)
right_frame.pack(side="right", padx=10, pady=10)

# Создаем выпадающий список для выбора DataFrame
dataframe_var = tk.StringVar()
dataframe_dropdown = ttk.Combobox(left_frame, textvariable=dataframe_var)
dataframe_dropdown.pack()

# Создаем кнопку для отображения выбранного DataFrame
display_button = ttk.Button(left_frame, text="Отобразить", command=display_dataframe)
display_button.pack()

# Запускаем главный цикл обработки событий
window.mainloop()
