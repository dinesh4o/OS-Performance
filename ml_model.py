from sklearn.tree import DecisionTreeClassifier
import numpy as np
import pickle
import os

MODEL_FILE = 'model.pkl'

# Define load classes
LOAD_LOW = 0
LOAD_MEDIUM = 1
LOAD_HIGH = 2

LABELS = {0: "Low Load", 1: "Medium Load", 2: "High Load"}

def train_dummy_model():
    """Trains a simple model on synthetic data for demonstration purposes."""
    
    # 1. Generate Dummy Features [CPU, RAM, DISK]
    # We create 100 samples with random values between 0-100
    X_train = np.random.rand(100, 3) * 100
    
    # 2. Generate Logical Labels
    # We assign labels based on rules so the model learns a sensible pattern
    # instead of random noise.
    y_train = []
    
    for row in X_train:
        cpu, ram, disk = row
        
        # Rule: High CPU (>70) or Very High RAM (>85) -> High Load
        if cpu > 70 or ram > 85:
            y_train.append(LOAD_HIGH)
        # Rule: Moderate CPU (>30) or High RAM (>60) -> Medium Load
        elif cpu > 30 or ram > 60:
            y_train.append(LOAD_MEDIUM)
        # Else -> Low Load
        else:
            y_train.append(LOAD_LOW)
            
    y_train = np.array(y_train)
    
    # 3. Train the Model
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)
    
    # 4. Save
    with open(MODEL_FILE, 'wb') as f:
        pickle.dump(clf, f)
    
    return clf

def load_or_train_model():
    """Loads existing model or trains a new one."""
    if os.path.exists(MODEL_FILE):
        try:
            with open(MODEL_FILE, 'rb') as f:
                return pickle.load(f)
        except:
            return train_dummy_model()
    else:
        return train_dummy_model()

def predict_system_load(cpu, ram, disk):
    """Predicts system load status."""
    model = load_or_train_model()
    # Reshape for single sample prediction
    prediction = model.predict([[cpu, ram, disk]])
    return LABELS[prediction[0]]
