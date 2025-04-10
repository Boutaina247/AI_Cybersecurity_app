import streamlit as st
import joblib
import hashlib
import pandas as pd
from cryptography.fernet import Fernet
import torch
from transformers import AutoTokenizer
from transformers import DistilBertForSequenceClassification, DistilBertTokenizer


# ----- Authentification simulée -----
def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

AUTHORIZED_USERS = {
    "analyste": hash_password("analyst123"),
    "datascientist": hash_password("data456")
}

# ----- Clé Fernet pour démo -----
with open("fernet.key", "rb") as f:
    fernet = Fernet(f.read())

# ----- Charger les données d'accès -----
df = pd.read_csv("access_log.csv")

# ----- Hash user IDs for display to analyst -----
# Hash the user IDs to show only hashed version for data analyst
def hash_user_id(user_id):
    return hashlib.sha256(user_id.encode()).hexdigest()

# Apply the hashing function for Data Analyst
df['user_hash'] = df['user_id'].apply(hash_user_id)

# ----- Interface Streamlit -----
st.title("🔐 IMDB Sentiment Analysis - Interface Sécurisée")

# Demande de connexion
username = st.text_input("👤 Nom d'utilisateur")
password = st.text_input("🔑 Mot de passe", type="password")

if username and password:
    pwd_hash = hash_password(password)
    
    if username in AUTHORIZED_USERS and AUTHORIZED_USERS[username] == pwd_hash:
        st.success(f"Bienvenue, {username} ✅")

        if username == "analyste":
            st.info("🕵️ Rôle : Analyste (accès prédiction uniquement)")
        else:
            st.info("🧪 Rôle : Data Scientist (accès complet)")

        df['decrypted_text'] = df['encrypted_text'].apply(lambda x: fernet.decrypt(x.encode()).decode())
        # Affichage du log d'accès
        if username == "datascientist":
            st.subheader("🔍 Accès complet aux logs des utilisateurs")
            # For Data Scientists, display user_id, text and prediction
            # Decrypting the text for data scientist
            st.write(df[['user_id', 'decrypted_text', 'prediction']])  
        else:
            st.subheader("🔒 Accès limité pour l'analyste")
            # For Data Analysts, show user_hash, encrypted message, prediction, and decrypted_text
            st.write(df[['user_hash', 'decrypted_text', 'prediction']])

        # Option de test de message
        message = st.text_area("📨 Entrez un texte à analyser")

        if st.button("Analyser le texte") and message:
            # Encrypt and decrypt the message
            encrypted_msg = fernet.encrypt(message.encode()).decode()
            decrypted_msg = fernet.decrypt(encrypted_msg.encode()).decode()

            
            # Charger le modèle et le tokenizer
            model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)
            model.load_state_dict(torch.load("distilbert_model.pth", map_location=torch.device('cpu')))
            model.to(torch.device('cpu'))  # Ensure the model is on CPU

            tokenizer = joblib.load("tokenizer_new.joblib")  # Load the tokenizer

            # Tokenize the input
            inputs = tokenizer(decrypted_msg, return_tensors="pt", padding=True, truncation=True, max_length=512)
            
            # Make a prediction using the model
            with torch.no_grad():
                outputs = model(**inputs)
                logits = outputs.logits
                prediction = torch.argmax(logits, dim=-1).item()

            # Display the result
            label = "✅ POSITIVE" if prediction == 1 else "📉 NEGATIVE"
            st.markdown(f"**Résultat :** {label}")
            if username == "datascientist":
                st.code(f"Message chiffré : {encrypted_msg}")
    else:
        st.error("⛔ Utilisateur ou mot de passe incorrect")
