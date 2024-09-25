import pandas as pd
import numpy as np
from collections import defaultdict
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Otwórz plik bezpośrednio
file_path = r'C:\Users\racho\PycharmProjects\PPYLastProject\Final_Augmented_dataset_Diseases_and_Symptoms.csv'
with open(file_path, 'r', encoding='utf-8') as file:
    data = pd.read_csv(file)

# Przygotowanie danych
X = data.drop(columns=['diseases'])
y = data['diseases']

# Unikalne choroby i symptomy
diseases = y.unique()
symptoms = X.columns

# Liczba przypadków
num_cases = len(data)

# Prawdopodobieństwo wystąpienia każdej choroby
P_disease = y.value_counts() / num_cases

# Prawdopodobieństwo wystąpienia symptomów przy danej chorobie
P_symptom_given_disease = defaultdict(lambda: defaultdict(lambda: 0))

# Liczenie prawdopodobieństw
for disease in diseases:
    disease_data = data[data['diseases'] == disease]
    for symptom in symptoms:
        P_symptom_given_disease[disease][symptom] = (disease_data[symptom].sum() + 1) / (len(disease_data) + 2)


# Funkcja klasyfikująca
def predict(symptoms_input):
    print(symptoms_input)
    disease_probabilities = {}
    for disease in diseases:
        # P(Disease)
        probability = P_disease[disease]
        for symptom in symptoms:
            if symptoms_input.get(symptom, 0):
                # P(Symptom|Disease)
                probability *= P_symptom_given_disease[disease][symptom]
            else:
                # P(~Symptom|Disease)
                probability *= (1 - P_symptom_given_disease[disease][symptom])
        disease_probabilities[disease] = probability

    # Znajdowanie trzech chorób z największym prawdopodobieństwem
    top_3_diseases = sorted(disease_probabilities, key=disease_probabilities.get, reverse=True)[:3]
    return top_3_diseases


# Funkcja zwracająca zaznaczone symptomy
def symptom_input():
    user_symptoms = {symptom: var.get() for symptom, var in symptom_vars.items()}
    selected_symptoms = {symptom: value for symptom, value in user_symptoms.items() if value == 1}
    print("Zaznaczone symptomy:", selected_symptoms)
    return selected_symptoms


# Funkcja obsługująca kliknięcie przycisku "Search"
def on_search():
    selected_symptoms = symptom_input()
    top_3_diseases = predict(selected_symptoms)
    messagebox.showinfo("Przewidywane choroby",
                        f"Przewidywane choroby:\n1. {top_3_diseases[0]}\n2. {top_3_diseases[1]}\n3. {top_3_diseases[2]}")


# Funkcja filtrująca checkboxy na podstawie wyszukiwania
def filter_symptoms(*args):
    search_text = search_var.get().lower()
    for symptom, var in symptom_vars.items():
        if search_text in symptom.lower():
            symptom_checkbuttons[symptom].grid()
        else:
            symptom_checkbuttons[symptom].grid_remove()


# Utworzenie okna GUI
root = tk.Tk()
root.title("Przewidywanie chorób na podstawie symptomów")
root.geometry("800x600")

# Utworzenie ramki dla przewijania
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=1)

# Utworzenie płótna
canvas = tk.Canvas(main_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Dodanie paska przewijania do płótna
scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Skonfigurowanie płótna
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Utworzenie drugiej ramki wewnątrz płótna
second_frame = ttk.Frame(canvas)

# Dodanie tej ramki do okna na płótnie
canvas.create_window((0, 0), window=second_frame, anchor="nw")

# Utworzenie przycisku "Search" na górze po prawej stronie
btn_search = tk.Button(second_frame, text="Search", command=on_search)
btn_search.grid(row=0, column=2, padx=10, pady=10, sticky='ne')

# Utworzenie pola wyszukiwania
search_var = tk.StringVar()
search_var.trace('w', filter_symptoms)
search_entry = tk.Entry(second_frame, textvariable=search_var)
search_entry.grid(row=0, column=0, padx=10, pady=10, sticky='nw')

# Utworzenie zmiennych dla symptomów
symptom_vars = {symptom: tk.IntVar() for symptom in symptoms}
symptom_checkbuttons = {}

# Utworzenie checkboxów dla symptomów w trzech kolumnach poniżej przycisku "Search"
for i, (symptom, var) in enumerate(symptom_vars.items()):
    col = i % 3
    row = (i // 3) + 1  # Dodajemy 1, aby zacząć od drugiego wiersza
    chk = tk.Checkbutton(second_frame, text=symptom, variable=var)
    chk.grid(row=row, column=col, sticky='w')
    symptom_checkbuttons[symptom] = chk

# Uruchomienie GUI
root.mainloop()
