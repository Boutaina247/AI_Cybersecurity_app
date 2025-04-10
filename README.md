# AI Cybersecurity Application

This project demonstrates sentiment analysis using Natural Language Processing (NLP) and encryption for secure data access. The app is designed for different user roles with different access levels.

## Features

- **User Roles**: Two roles are defined: 
  - **Analyste**: Limited access (prediction-only access).
  - **Data Scientist**: Full access (access to user data, encrypted messages, and predictions).
- **Text Analysis**: Users can input text for sentiment analysis.
- **Encryption**: User messages are encrypted and decrypted securely.

## Prerequisites

1. **Python 3.x** installed on your machine.
2. **Required Libraries**:
   - `streamlit`
   - `joblib`
   - `hashlib`
   - `cryptography`
   - `pandas`
   - `torch` (for model handling)

## Setup

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/Boutaina247/AI_Cybersecurity_app.git
   cd AI_Cybersecurity_app
   ```

2. Place the encryption key file `fernet.key` in the root directory.

3. Make sure to have the model files:
   - `distilbert_model.pth`
   - `tokenizer_new.joblib`

4. Create a CSV file `access_log.csv` containing user access data (user ID, encrypted text, and predictions).

## Running the App

1. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

2. Open the app in your browser (typically at http://localhost:8501).

## User Roles and Credentials

- **Analyste** (Limited access to prediction results):
  - Username: `analyste`
  - Password: `analyst123`

- **Data Scientist** (Full access to logs and predictions):
  - Username: `datascientist`
  - Password: `data456`

### Access Levels

- **Analyst**:
  - Can only view hashed user IDs and messages along with their predictions.
  - Can input new text to analyze sentiment (Positive/Negative).
  - Can see the decrypted text of analyzed messages.

- **Data Scientist**:
  - Full access to user data logs (user ID, decrypted text, predictions).
  - Can view the encrypted messages and their decrypted versions.
  - Can input new text to analyze sentiment (Positive/Negative).

### Interface

1. **Login Screen**: Enter the username and password to log in as either an analyst or a data scientist.
2. **Text Area**: Both roles can input text for sentiment analysis.
3. **Prediction**: After clicking "Analyze Text," the model predicts the sentiment of the text and displays the result.

## Testing the App

### 1. **Log in as Analyst**:
- Username: `analyste`
- Password: `analyst123`

You will be able to:
- View user IDs (hashed) and messages with predictions.
- View the decrypted text for analyzed messages.

### 2. **Log in as Data Scientist**:
- Username: `datascientist`
- Password: `data456`

You will be able to:
- View full user logs, including user IDs, decrypted texts, and predictions.
- Input text for sentiment analysis and see results.

## Troubleshooting

If you encounter any issues while running the app, check the following:
- Ensure all required files (`fernet.key`, model files, `access_log.csv`) are present in the project directory.
- Verify that the correct Python environment is activated.

If the app doesn't run properly, you can check the logs and error messages provided by Streamlit for further debugging.
