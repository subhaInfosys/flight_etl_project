import joblib
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def predict_delay(input_data):
    model = joblib.load('flight_delay_model.pkl')
    input_df = pd.get_dummies(pd.DataFrame([input_data]))
    # Align columns with training features
    model_features = model.feature_names_in_
    input_df = input_df.reindex(columns=model_features, fill_value=0)
    prediction = model.predict(input_df)[0]
    return prediction

def train_model(data):
    # Convert 'status' to binary label
    data['is_delayed'] = data['status'].apply(lambda x: 1 if x == 'delayed' else 0)

    # Convert datetime column to useful numeric features
    data['departure_time'] = pd.to_datetime(data['departure_time'], errors='coerce')
    data['dep_hour'] = data['departure_time'].dt.hour
    data['dep_dayofweek'] = data['departure_time'].dt.dayofweek

    # Drop rows with NaT or missing values
    data.dropna(subset=['dep_hour', 'dep_dayofweek'], inplace=True)

    # Features to use
    features = ['airline', 'departure_airport', 'arrival_airport', 'dep_hour', 'dep_dayofweek']
    X = pd.get_dummies(data[features])
    y = data['is_delayed']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Train model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Save model
    joblib.dump(model, 'flight_delay_model.pkl')
    print("✅ Model saved as flight_delay_model.pkl")

    return model
