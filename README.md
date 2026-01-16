# High-Value Customer Prediction API
The project provides an API for predicting whether a customer is a high-value customer using historical transactional data. It combines data preprocessing, feature engineering, and supervised machine learning to identify customers likely to generate high future revenue.

## Table of Contents
*  Project Overview
*  Data
*  Feature Engineering
*  Modeling
*  API Endpoints
*  Business Insights
*  Limitations
*  Usage

## Project Overview
The API provides a simple interface to get predictions and high-value probabilities for given customer features

### Defining the Problem
Businesses need to identify which customers are likely to **generate high revenue in the future to prioritize retention efforts, optimize marketing spend, and increase overall profitability**. </br>
Manually analyzing customer transactions to find high-value customers is time-consuming and error-prone. By leveraging historical purchase data and machine learning, the goal is to predict high-value customers before their future behavior occurs, enabling targeted business action such as loyalty rewards, upsell campaigns, or retention strategies.

## Data
The dataset, [Online Retail II UCI](https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci), includes transactions from a UK-based online-only retail store (2009-2011) </br>
The Attributes include...
* `InvoiceNo`: Invoice number.
* `StockCode`: Product (item) code. 
* `Description`: Product (item) name.
* `Quantity`: The quantities of each product (item) per transaction.
* `InvoiceDate`: Invice date and time.
* `UnitPrice`: Unit price in sterling (Â£).
* `CustomerID`: Customer number.
* `Country`: Country name.
### Data Cleaning
1. Removed canceled invoices (`Invoices` starting with 'c')
2. Removed rows with missing `Customer ID`
3. Removed rows with negative `Price` and/or `Quantity` entries
4. Converted `InvoiceDate` to datetime
</br>
After cleaning: **805,625 transactions** across **41 countries**

## Feature Engineering
Customer-level features were constructed based on historical data:
| **Features** | **Description** |
|---|---|
| Recency | Days since last purchase |
| Frequency | Number of purchases made |
| Monetary | Total amount spent |
| spend_last_90_days | Total spending in the last 90 days |
| SpendTrend | Change in spending between last 90 days and previous 90 days |
| AverageOrderValue | Monetary / Frequency |
### Binary Label
> High Value: Whether the customer falls in the top 25% of future spenders (excluding zero-spenders)
### Multi-Class Alternative
> FutureSpendCategory: Sorts the customer into one of the following categories Zero/Low/Medium/High

## Modeling
Multiple models were evaluated for classification
* Logistic Regression
* Random Forrest
* XGBoost
* K-Nearest Neighbors (KNN)
* Support Vector Machines (SVM)
* Naive Bayes
### Performance (Multi-Classification, ROC-AUC)
| **Model** | **ROC-AUC** |
|:---:|:---:|
| Logistic Regression | 0.75 |
| SVM | 0.76 |
| Random Forest | 0.71 |
| Naive Bayes | 0.73 |
| XGBoost | 0.70 |
| KNN | 0.69 |
### Performance (Binary Classification, ROC-AUC)
| **Model** | **ROC-AUC** |
|:---:|:---:|
| Logistic Regression | 0.88 |
| SVM | 0.88 |
| Random Forest | 0.87 |
| Naive Bayes | 0.87 |
| XGBoost | 0.85 |
| KNN | 0.83 |
</br> 
* Due to the higher ROC-AUC values, Binary Classification was chosen to evaluate high value customers
* Threshold for high-value prediction was set to 0.6
* Logistic Regression was chosen for its interpretability, stability, and strong performance

## API Endpoints
Built with FastAPI, exposing the following endpoints
* GET/: Checks API health</br>
    **Response:**  `{'message' : 'API is working'}`
* GET/health: Health check endpoint</br>
    **Response:**  `{'status' : 'ok'}`
* POST/predict: Predicts if customer is high value</br>
    **Request Body (JSON):**  `{
  "Recency": 10,
  "Frequency": 5,
  "Monetary": 200.0,
  "spend_last_90_days": 50.0,
  "SpendTrend": 10.0,
  "AverageOrderValue": 40.0
}` </be>
    **Response:** `{
  "high_value_probability": 0.72,
  "prediction": "High Value",
  "status": "success"
}`
* Validation Error: Returns detailed field errors with status code 400
## Business Insights
* **High Value Customers** tend to spend more recently, frequently, and in higher amounts
* *Negative Spend Trend* indicates declining customer engagement --> a signal for reactivation campaigns
### Actionable strategies based on prediction
| **Customer Value** | **Strategies** |
|:---:|:---|
| High | Loyalty program, personalized experiences |
| Medium | Encourage increased spending through limited timed offers, cross-sell and up-sell |
| Low | Reactivation and low-cost email campaigns |
| Zero | Churn Prevention |
## Limitations
* Dataset is historical (2009-2011) from a single UK retailer
* No marketing exposure or demographic data included
* Assumes future behavior follows past trends
* Currency and inflation are not normalized
* External validity may be limited outside this context

## Usage
1. Clone the repository
> git clone <repo-url> </br> cd <repo-folder>
2. Install dependencies
> pip install -r requirements.txt
3. Run the FastAPI app
> uvicorn main:app --reload
5. Access API docs at `http://127.0.0.1:8000/docs`
6. Send POST requests to  `/predict` with customer features to get high-value predictions

### Model Saving
The final logistic regression model pipeline is saved as `mymodel.joblib` for easy development
