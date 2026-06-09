import pandas as pd
from sklearn.preprocessing import LabelEncoder 
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score 
from sklearn.metrics import classification_report
import joblib
import mlflow
from sklearn.metrics import recall_score 

df = pd.read_csv("flight_data_2024.csv")
df["is_delayed"]=(df["dep_delay"]>15).astype(int)

#dropping useless data/columns
df = df.drop([
    "dep_time", "arr_time", "arr_delay",
    "taxi_out", "taxi_in", "wheels_off", "wheels_on",
    "actual_elapsed_time", "air_time",
    "carrier_delay", "weather_delay", "nas_delay", 
    "security_delay", "late_aircraft_delay",
    "fl_date", "origin_city_name", "dest_city_name",
    "origin_state_nm", "dest_state_nm", "op_carrier_fl_num",
    "year", "dep_delay"
], axis=1)
df = df.dropna(subset=["is_delayed"])
df=df.drop(["cancelled", "diverted", "cancellation_code"],axis=1)
df = df.drop(["crs_arr_time"], axis=1)
df["crs_elapsed_time"]=df["crs_elapsed_time"].fillna(df["crs_elapsed_time"].median())

#feature engineering
df["dep_hour"]=df["crs_dep_time"]//100
df["is_rush_hour"]=df["dep_hour"].isin([7,8,9,17,18,19]).astype(int)
df["is_holiday_month"]=df["month"].isin([7,8,12,1]).astype(int)
df["is_weekend"]=df["day_of_week"].isin([5,6,7]).astype(int)
df["is_short_flight"]=(df["distance"]<500).astype(int)
df = df.drop(["crs_dep_time"], axis=1)



#labelEncoder
encoder={}
for col in ['op_unique_carrier', 'origin', 'dest']:
    enc=LabelEncoder()
    df[col]=enc.fit_transform(df[col])
    encoder[col]=enc


print(df.shape)
print(df.head())

X=df.drop("is_delayed",axis=1)
Y=df["is_delayed"]
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2)

# Calculate rates on TRAINING data only
train_data = X_train.copy()
train_data["is_delayed"] = Y_train.values

airline_delay_rate = train_data.groupby("op_unique_carrier")["is_delayed"].mean()

# Map to both train and test
X_train["airline_delay_rate"] = X_train["op_unique_carrier"].map(airline_delay_rate)
X_test["airline_delay_rate"] = X_test["op_unique_carrier"].map(airline_delay_rate)

# origin delay rate
origin_delay_rate = train_data.groupby("origin")["is_delayed"].mean()
X_train["origin_delay_rate"] = X_train["origin"].map(origin_delay_rate)
X_test["origin_delay_rate"] = X_test["origin"].map(origin_delay_rate)

# route delay rate
route_delay_rate = train_data.groupby(["origin", "dest"])["is_delayed"].mean()
X_train["route_delay_rate"] = X_train.set_index(["origin", "dest"]).index.map(route_delay_rate)
X_test["route_delay_rate"] = X_test.set_index(["origin", "dest"]).index.map(route_delay_rate)

mlflow.set_experiment("Flight Delay Predictor")
with mlflow.start_run():
    model = LGBMClassifier(
        class_weight='balanced',
        random_state=42,
        max_depth=7,
        n_estimators=200,
        learning_rate=0.05,
        num_leaves=31
)
    mlflow.log_param("n_estimators", 200)
    mlflow.log_param("max_depth", 7)
    mlflow.log_param("learning_rate", 0.05)
    
   
    model.fit(X_train,Y_train)
    predictions=model.predict(X_test)
    accuracy=accuracy_score(Y_test,predictions)
    mlflow.log_metric("accuracy", accuracy)
    recall = recall_score(Y_test, predictions)
    mlflow.log_metric("recall_delayed", recall)

    print(classification_report(Y_test,predictions))

    joblib.dump(model,"model.pkl")
    joblib.dump(encoder,"encoder.pkl")
    joblib.dump(airline_delay_rate, "airline_delay_rate.pkl")
    joblib.dump(origin_delay_rate, "origin_delay_rate.pkl")
    joblib.dump(route_delay_rate, "route_delay_rate.pkl")
