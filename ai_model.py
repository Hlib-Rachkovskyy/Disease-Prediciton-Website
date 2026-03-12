import pandas as pd
import os
import pickle
from sklearn.tree import DecisionTreeClassifier

class AI:
    def __init__(self, dataset):
        self.model = None
        self.symptoms = None
        self.diseases = None
        self.file = 'trained_logreg_model.pkl'
        self.train_data = None
        self.evaluate_data = None

        if os.path.exists(self.file) and os.path.getsize(self.file) > 0:
            print("Loading model from file...")
            self.load_model()
        else:
            print("Training model...")
            if dataset:
                self.learn(dataset)
                self.evaluate()
                self.save_model()
            else:
                print("No dataset found!")

    def learn(self, dataset):
        file_path = dataset
        print("1. Loading dataset into memory...")
        data = pd.read_csv(file_path, encoding='utf-8')

        print(f"   -> Dataset loaded: {len(data)} rows found.")

        data = data.sample(frac=1, random_state=42).reset_index(drop=True)

        split_index = int(len(data) * 0.8)

        print("2. Splitting data into training and evaluation sets...")
        train_data, evaluate_data = data.iloc[:split_index], data.iloc[split_index:]

        self.evaluate_data = evaluate_data

        columns = train_data.drop(columns=['diseases'])
        rows = train_data['diseases']

        self.symptoms = columns.columns.tolist()
        self.diseases = rows.unique()

        print(f"   -> Setup complete. Found {len(self.symptoms)} symptoms and {len(self.diseases)} diseases.")
        print("3. Starting Decision Tree training...")

        self.model = DecisionTreeClassifier(random_state=42)
        self.model.fit(columns, rows)

        print("\nModel trained successfully!")

    def evaluate(self):
        print("Evaluating model...")
        value = self.evaluate_model()
        print("Model evaluated successfully...")
        print(f"Accuracy: {value * 100:.2f}%")

    def model_predict(self, symptoms_in):
        input_data = pd.DataFrame([symptoms_in], columns=self.symptoms)
        input_data = input_data.fillna(0)

        probabilities = self.model.predict_proba(input_data)[0]
        disease_probabilities = dict(zip(self.model.classes_, probabilities))

        top_3_diseases = sorted(disease_probabilities, key=disease_probabilities.get, reverse=True)[:3]

        return top_3_diseases

    def evaluate_model(self):
        y_true = self.evaluate_data['diseases']
        X_eval = self.evaluate_data.drop(columns=['diseases'])
        y_pred = self.model.predict(X_eval)
        accuracy = (y_pred == y_true).mean()

        return accuracy

    def save_model(self):
        model_data = {
            'model': self.model,
            'symptoms': self.symptoms,
            'diseases': self.diseases
        }

        with open(self.file, 'wb') as f:
            pickle.dump(model_data, f)
        print("Model saved to file.")

    def load_model(self):
        with open(self.file, 'rb') as f:
            model_data = pickle.load(f)

        self.model = model_data['model']
        self.symptoms = model_data['symptoms']
        self.diseases = model_data['diseases']
        print("Model loaded successfully.")