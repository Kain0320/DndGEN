import tkinter as tk
from tkinter import ttk, messagebox
from base import races, classes, backgrounds, names
import random

# Funkce pro generování jména
def generate_name():
    selected_race = race_var.get()
    selected_gender = gender_var.get()
    
    if selected_race and selected_gender:
        name = random.choice(names[selected_race][selected_gender])
        name_var.set(name)
    else:
        messagebox.showerror("Chyba", "Vyber rasu a pohlaví pro generování jména!")

# Funkce pro generování postavy
def generate_character():
    character_info = (
        f"Jméno: {name_var.get()}\n"
        f"Rasa: {race_var.get()}\n"
        f"Povolání: {class_var.get()}\n"
        f"Pohlaví: {gender_var.get()}\n"
        f"Zázemí: {background_var.get()}\n"
    )
    result_label.config(text=character_info)

# Hlavní okno
root = tk.Tk()
root.title("D&D 5e Generátor postav")
root.geometry("400x400")

# Výběrové menu
race_var = tk.StringVar()
class_var = tk.StringVar()
gender_var = tk.StringVar()
background_var = tk.StringVar()
name_var = tk.StringVar()

tk.Label(root, text="Vyber rasu:").pack()
race_dropdown = ttk.Combobox(root, textvariable=race_var, values=list(races.keys()))
race_dropdown.pack()

tk.Label(root, text="Vyber povolání:").pack()
class_dropdown = ttk.Combobox(root, textvariable=class_var, values=list(classes.keys()))
class_dropdown.pack()

tk.Label(root, text="Vyber pohlaví:").pack()
gender_dropdown = ttk.Combobox(root, textvariable=gender_var, values=["Muž", "Žena"])
gender_dropdown.pack()

tk.Label(root, text="Vyber zázemí:").pack()
background_dropdown = ttk.Combobox(root, textvariable=background_var, values=list(backgrounds.keys()))
background_dropdown.pack()

tk.Label(root, text="Jméno:").pack()
name_entry = tk.Entry(root, textvariable=name_var)
name_entry.pack()

tk.Button(root, text="Generovat jméno", command=generate_name).pack()
tk.Button(root, text="Vytvořit postavu", command=generate_character).pack()

result_label = tk.Label(root, text="", justify="left")
result_label.pack()

root.mainloop()
