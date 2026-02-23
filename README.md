# 🛡️ NetShield-AI

An AI-Powered Network Intrusion Detection System (IDS) built using Machine Learning and deployed with Streamlit.

NetShield-AI detects malicious network traffic using supervised learning techniques trained on the CIC-IDS dataset. The system performs preprocessing, feature scaling, model prediction, and displays results through an interactive web interface.

---

## 🚀 Live Application (Local)

Run locally using:

```bash
streamlit run app.py
```

Then open:

http://localhost:8501

---

## 📌 Project Overview

This project includes:

- Data preprocessing & cleaning
- Feature engineering
- Label encoding
- Tree-based Machine Learning model
- Saved trained model (`ids_model.pkl`)
- Streamlit-based Web Application

The model classifies network traffic as:

- ✅ Normal
- 🚨 Attack

---

## 📂 Project Structure

```
NetShield-AI/
│── app.py
│── ids_model.pkl
│── label_encoder.pkl
│── Tree_based_IDS_GlobeCom19Intrusion.ipynb
│── README.md
```

---

## ⚙️ Installation Guide

### 1️⃣ Clone Repository

```bash
git clone https://github.com/AbdulSheikh9906/NetShield-AI.git
```

### 2️⃣ Navigate to Project

```bash
cd NetShield-AI
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If requirements file is not available:

```bash
pip install streamlit pandas numpy scikit-learn joblib
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

---

## 🧠 Model Details

- Algorithm: Tree-Based Classifier
- Dataset: CIC-IDS
- Task: Binary Classification (Normal vs Attack)
- Framework: Scikit-learn

---

## 🛠 Technologies Used

- Python
- Streamlit
- Scikit-learn
- Pandas
- NumPy
- Joblib

---

## 📊 Future Improvements

- Multi-class attack detection
- Real-time packet monitoring
- Cloud deployment
- Dashboard analytics

---

## 👨‍💻 Author

**Abdul Sheikh**  
GitHub: https://github.com/AbdulSheikh9906  

---

## ⭐ Support

If you like this project, consider giving it a star ⭐ on GitHub.
