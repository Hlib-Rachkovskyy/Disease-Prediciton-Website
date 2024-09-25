import pandas as pd
import os
import pickle
from sklearn.neighbors import KNeighborsClassifier

class AI:
    def __init__(self):
        self.model = None
        self.symptoms = None
        self.diseases = None
        self.file = 'trained_knn_model.pkl'

        if os.path.exists(self.file) and os.path.getsize(self.file) > 0:
            print("Loading model from file...")
            self.load_model()
        else:
            print("Training model...")
            self.learn()
            self.save_model()

    def learn(self):
        file_path = 'Final_Augmented_dataset_Diseases_and_Symptoms.csv'
        data = pd.read_csv(file_path, encoding='utf-8')

        columns = data.drop(columns=['diseases'])
        rows = data['diseases']

        self.symptoms = columns.columns.tolist()
        self.diseases = rows.unique()

        self.model = KNeighborsClassifier(n_neighbors=5)
        self.model.fit(columns, rows)
        print("Model trained successfully.")

    def model_predict(self, symptoms_in):
        input_data = pd.DataFrame([symptoms_in], columns=self.symptoms)
        input_data = input_data.fillna(0)

        probabilities = self.model.predict_proba(input_data)[0]
        disease_probabilities = dict(zip(self.model.classes_, probabilities))

        top_3_diseases = sorted(disease_probabilities, key=disease_probabilities.get, reverse=True)[:3]

        return top_3_diseases

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
