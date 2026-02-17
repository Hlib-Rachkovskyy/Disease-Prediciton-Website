import pandas as pd
import os
import pickle
from sklearn.neighbors import KNeighborsClassifier


class AI:
    def __init__(self, dataset):
        self.model = None
        self.symptoms = None
        self.diseases = None
        self.file = 'trained_knn_model.pkl'
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
        data = pd.read_csv(file_path, encoding='utf-8')

        data = data.sample(frac=1, random_state=42).reset_index(drop=True)

        split_index = int(len(data) * 0.8)

        train_data, evaluate_data = data.iloc[:split_index], data.iloc[split_index:]

        self.evaluate_data = evaluate_data

        columns = train_data.drop(columns=['diseases'])
        rows = train_data['diseases']

        self.symptoms = columns.columns.tolist()
        self.diseases = rows.unique()

        self.model = KNeighborsClassifier(n_neighbors=5)
        self.model.fit(columns, rows)
        print("Model trained successfully...")

    def evaluate(self):
        print("Evaluating model...")
        value = self.evaluate_model()
        print("Model evaluated successfully...")
        print("Accuracy: ${value * 100:.2f}%")

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
