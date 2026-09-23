# Market-Volatility-Prediction

Using simple Machine Learning to directly predict stock prices is notoriously difficult due to so many factors outside of our control, such as internal business decisions, global pandemics, erratic consumer behaviour, and unexpected trends. However, making informed decisions based on how chaotic the ups and downs (i.e volatililty) of prices are can be very useful and beneficial. This project aims to use Machine Learning to predict future volatility of the SPDR S&P 500 ETF (SPY) which is an exchange traded fund that tracks the performance of the S&P 500. In a sense, we're predicting unpredictability.

### Overview

Market volatility is a measure of how much financial returns fluctuate over a given period. This project focuses on predicting 10 day forward volatility using historical market data.

The project was developed as an end to end machine learning pipeline, covering the process from raw market data through to model deployment and automated prediction.

**What the system does**
- Retrieves historical market data using yfinance
- Engineers return and volatility-related features
- Predicts 10-day forward volatility using a trained CatBoost regression model
- Compares the machine learning model against statistical and naive baselines
- Stores market data, engineered features, and predictions in PostgreSQL
- Exposes predictions through a FastAPI application
- Containerises the application using Docker
- Deploys the application to AWS using ECS Fargate
- Runs automated weekday predictions using Amazon EventBridge Scheduler
- Records application and prediction logs using Amazon CloudWatch
- Uses GitHub Actions for CI/CD deployment

### The Aim
Using multiple different Machine Learning methods, this project aims to predict future volatility of the ETF so that data driven decisions can be made in trading or investing. 

### The objective
If this were an environment in investment banking firm or other finance related firms, the objective might be to make predictions on how volatile a certain asset is and make an automated system so that informed decisions can be made in whether or not to trade/invest now or wait until things calm down.

### The Machine Learning Design

- This would be a *supervised learning* task, as we can train our model with labelled examples
- This would be a *univariate regression* task as we are predicting a single value (standard deviation of log returns)
- And this would be an *online learning* task as we will be having a continuous stream of data for our model.

### The Data
For this project, the yfincance API will be used to get around eleven years worth of historical Open, High, Low, Close, Volume data from 1st Jan 2015 to 31st December 2025. There are no missing values or duplicate values, which means no imputation, however we will need to get rid of some outilers.

- Open = Price at the start of the day
- High = Highest price of that day
- Low = Lowest price of that day
- Close = Price at the end of the day
- Volume = Volume traded

### Results

| Model       | RMSE  |
| ------------- | -----:|
| Naive 10 day volatility | 0.006817 |
| GARCH(1,1) | 0.005938 |
| CatBoost | 0.004985|

The CatBoost model was selected as the deployed model after achieving lower validation error than the statistical baseline.

**Note:** The final deployed model was trained using the modelling pipeline developed in the project and is used to generate 10-day forward volatility predictions in the production application.

### System Architechture
<img width="3965" height="8070" alt="diagram" src="https://github.com/user-attachments/assets/941c6b61-9a53-4a2f-8460-e12de1bc04c8" />

### AWS Deployment

The application was deployed to AWS as a containerised, scheduled machine learning system.

**AWS Services used**

| Service       | Purpose  |
| ------------- | ----- |
|Amazon ECS Fargate |	Hosts the containerised FastAPI application and prediction worker|
|Amazon ECR|	Stores Docker container images|
|Amazon RDS PostgreSQL|	Stores market data, engineered features, and predictions|
|Amazon EventBridge Scheduler|	Automatically launches the prediction worker on weekdays|
|Amazon CloudWatch	|Collects application and prediction logs|
|AWS IAM|	Provides service permissions and secure access to AWS resources|
|Amazon VPC|	Provides network isolation and security controls|
|GitHub Actions|	Automates Docker image builds and ECS deployments|

**Deployment Architechture**

The FastAPI application was packaged as a Docker container and deployed to Amazon ECS using AWS Fargate.
The production database was hosted using Amazon RDS PostgreSQL. Access to the database was restricted through VPC security groups rather than exposing the database publicly.
Amazon EventBridge Scheduler was configured to launch a standalone ECS Fargate task at 8:00 AM Monday–Friday in the Australia/Melbourne timezone. The task runs the complete prediction pipeline and exits after completion.
The resulting application and task logs were captured using Amazon CloudWatch.

**CI/CD**

GitHub Actions was used to automate deployment of the API.

GitHub -> GitHub Actions -> Docker build -> Amazon ECR -> Amazon ECS







