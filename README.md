# Flight Delay Predictor

A machine learning project that predicts whether a flight will be delayed by more than 15 minutes using historical US flight data from 2024.

## About the Project

I built this project to learn how a machine learning model can be taken from data preprocessing all the way to deployment.

The model is trained on flight records from the Bureau of Transportation Statistics and predicts whether a flight is likely to be delayed before departure.

## What I Used

* Python
* Pandas
* LightGBM
* Scikit-learn
* FastAPI
* MLflow
* Streamlit
* Docker

## Dataset

* 7 million+ US flight records from 2024
* Source: Bureau of Transportation Statistics
* Delay label created using departure delays greater than 15 minutes

## Feature Engineering

Some of the features I created include:

* Airline delay history
* Route delay history
* Airport delay history
* Weekend indicator
* Rush-hour departures
* Holiday season indicator
* Short flight indicator

## Model Results

* Accuracy: 66%
* Recall for delayed flights: 66%
* Training data: 5.6 million flights
* Test data: 1.4 million flights

## Project Components

### Model Training

Data cleaning, feature engineering, label encoding, and LightGBM model training.

### FastAPI Service

REST API that accepts flight information and returns a delay prediction.

### Streamlit Interface

Simple web interface for testing predictions.

### MLflow Tracking

Used to track experiments and compare model runs.

### Docker

Containerized the application for easier deployment.

## Project Structure

flight-delay-predictor/

├── api/            # FastAPI application

├── src/            # Training and Streamlit code

├── models/         # Saved model files

├── Dockerfile

└── requirements.txt

## Running the Project

1. Download the dataset
2. Train the model
3. Start the FastAPI server
4. Launch the Streamlit app

## Future Improvements

* Add weather data
* Try more advanced feature engineering
* Deploy on AWS
* Set up GitHub Actions for CI/CD

## What I Learned

* Working with large datasets
* Feature engineering for tabular ML problems
* Model experiment tracking with MLflow
* Building prediction APIs with FastAPI
* Containerizing applications with Docker
