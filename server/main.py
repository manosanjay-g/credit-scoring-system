from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

app = FastAPI()

# Load the dataset and preprocess if necessary
df = pd.read_csv('../dataset/dataset.csv')
df = df.drop(df.columns[3], axis=1)

# Separate features and target variable
features = df.iloc[:, :6]
y = df.iloc[:, 6]

# Train-Validation-Test split
X_train, X_test, y_train, y_test = train_test_split(features, y, test_size=0.3, random_state=42)

# Base Models
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
xgb_model = XGBClassifier(n_estimators=100, random_state=42)

# # Fit base models
rf_model.fit(X_train, y_train)
xgb_model.fit(X_train, y_train)
rf_predictions = rf_model.predict(X_test)
xgb_predictions = xgb_model.predict(X_test)
# Meta model (Logistic Regression)
blend_train = pd.DataFrame({'RF': rf_predictions, 'XGB': xgb_predictions})
meta_model = LogisticRegression()
meta_model.fit(blend_train, y_test)
blend_test = pd.DataFrame({'RF': rf_model.predict(X_test), 'XGB': xgb_model.predict(X_test)})
blend_predictions = meta_model.predict(blend_test)

class Item(BaseModel):
    age: float
    gender: float
    income: float
    marital_status: float
    number_of_children: float
    house_ownership: float

@app.get("/")
def index():
    print(features)
    return {"df":"features"}

@app.post("/predict/")
async def predict(item: Item):
    input_data = np.array([[item.age, item.gender, item.income,
                            item.marital_status, item.number_of_children, item.house_ownership]])
    
    # Predict using base models
    rf_prediction = rf_model.predict(input_data)
    xgb_prediction = xgb_model.predict(input_data)
    
    # Blending features for the meta model
    blend_input = pd.DataFrame({'RF': rf_prediction, 'XGB': xgb_prediction})
    
    # Predict using meta model
    final_prediction = meta_model.predict(blend_input)
    print(final_prediction)
    return {"prediction": final_prediction[0]}

