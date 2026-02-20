# Disease Prediction App Setup Guide

Welcome to the project! This guide will walk you through setting up the required dataset, database, environment variables, and starting both the frontend and backend servers.

## Prerequisites

### 1. Dataset
Before running the backend, you must download the AI model's training data.
* **Download here:** [Diseases and Symptoms Dataset on Kaggle](https://www.kaggle.com/datasets/dhivyeshrk/diseases-and-symptoms-dataset)
* Extract the `.csv` file and place it in the root of your **backend** directory. Ensure the filename matches what is expected in `app.py` (e.g., `Final\_Augmented\_dataset\_Diseases\_and\_Symptoms.csv`).

### 2. Database
This project requires **PostgreSQL**. You need to have a Postgres server running and accepting connections.

---

## Environment Variables

You need to create two separate `.env` files to configure the application locally.

### 1. Backend `.env`
Create a file named `.env` inside your **backend** directory:
```env
# PostgreSQL connection string
DATABASE_URL=postgresql://postgres:yoursecretpassword@localhost:5431/postgres

# JWT Secret Key for authentication
SECRET_KEY=your-super-secret-key
```
### 2. Frontend `.env`

Create a file named `.env` inside your **frontend** directory:

```env
# Point Vite to the local Flask backend
VITE_API_URL=http://localhost:5000/api/
```
---
## Starting the Application localy

You will need two separate terminal windows to run the frontend and backend simultaneously.

### 1. Start the Backend (Flask)

Install required Python packages:

```bash
pip install -r requirements.txt
```
Start the Flask server:

```bash
python app.py
```
### 2. Start the Frontend (Vite/React)

Install Node modules:

```bash
npm install
```
Start the development server:

```bash
npm run dev
```
---
## Running app via docker
In progress