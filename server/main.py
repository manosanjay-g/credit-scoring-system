from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Allow all methods you need
    allow_headers=["*"],  # Allow all headers
)
# Load the dataset and preprocess if necessary
df = pd.read_csv('../dataset/credit-score.csv')

# Separate features and target variable
features = df.iloc[:, :8]
y = df.iloc[:, 8]

# Train-Validation-Test split
X_train, X_test, y_train, y_test = train_test_split(features, y, test_size=0.3, random_state=42)

# Base Models
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
xgb_model = XGBClassifier(n_estimators=100, random_state=42)

# Fit base models
rf_model.fit(X_train.values, y_train.values)
xgb_model.fit(X_train.values, y_train.values)
rf_predictions = rf_model.predict(X_test)
xgb_predictions = xgb_model.predict(X_test)

# Meta model (Logistic Regression)
blend_train = pd.DataFrame({'RF': rf_predictions, 'XGB': xgb_predictions})
meta_model = LogisticRegression()
meta_model.fit(blend_train, y_test)
blend_test = pd.DataFrame({'RF': rf_model.predict(X_test), 'XGB': xgb_model.predict(X_test)})
blend_predictions = meta_model.predict(blend_test)

class CreditInfo(BaseModel):
    age:int
    income:int
    num_of_loans:int
    no_of_delayed_payments:int
    no_of_credit_inquires:int
    credit_mix:int
    credit_util_ratio:int
    payment_behaviour:int

class Item(BaseModel):
    age: int
    gender: int
    income: int
    marital_status: int
    number_of_children: int
    house_ownership: int

@app.get("/")
def index():
    print(features)
    s = 0
    for value in df['Age']:
        s+=value
    return {"df":s}

@app.post("/credit-score/")
async def credit_score(creditInfo: CreditInfo):
    input_data = np.array([[
        creditInfo.age,
        creditInfo.income,
        creditInfo.num_of_loans,
        creditInfo.no_of_credit_inquires,
        creditInfo.no_of_delayed_payments,
        creditInfo.credit_mix,
        creditInfo.credit_util_ratio,
        creditInfo.payment_behaviour
    ]])

    # Predict using base models
    rf_prediction = rf_model.predict(input_data)
    xgb_prediction = xgb_model.predict(input_data)
    
    # Blending features for the meta model
    blend_input = pd.DataFrame({'RF': rf_prediction, 'XGB': xgb_prediction})
    
    # Predict using meta model
    final_prediction = meta_model.predict(blend_input)

    credit_score = ""

    if(final_prediction[0] == 0):
        credit_score = "Low"
    elif(final_prediction[0] == 1):
        credit_score = "Average"
    else:
        credit_score = "High"
    
    

    return {"credit_rating": credit_score}


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
    credit_score = ""
    if(final_prediction[0] == 0):
        credit_score = "Low"
    elif(final_prediction[0] == 1):
        credit_score = "Average"
    else:
        credit_score = "High"
    return {"credit_rating": credit_score}

