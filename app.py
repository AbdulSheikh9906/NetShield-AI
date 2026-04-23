import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import resample
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, precision_score, recall_score, f1_score
import time
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Intrusion Detection System", layout="wide")
st.title("🛡️ Multi-Class Intrusion Detection System | Network Security")

# ------------------------------
# 1. MODEL TRAINING FUNCTION (Cached)
# ------------------------------
@st.cache_resource
def load_or_train_model(data):
    """Train model with data balancing and return model and encoders"""
    
    # Handle missing and infinite values
    if 'Label' in data.columns:
        X = data.drop('Label', axis=1)
        y = data['Label']
    else:
        st.error("Dataset must contain a 'Label' column")
        return None, None, 0, None, None, None, None, None
    
    # Replace infinite values with NaN and fill with 0
    X = X.replace([np.inf, -np.inf], np.nan)
    X = X.fillna(0)
    
    # Group similar attacks (from your notebook)
    attack_mapping = {
        'BENIGN': 'BENIGN',
        'DDoS': 'DDoS',
        'DoS Hulk': 'DoS',
        'DoS GoldenEye': 'DoS',
        'DoS slowloris': 'DoS',
        'DoS Slowhttptest': 'DoS',
        'PortScan': 'Port_Scan',
        'SSH-Patator': 'BruteForce',
        'FTP-Patator': 'BruteForce',
        'Bot': 'Botnet'
    }
    
    # Apply mapping if attack names match
    if y.dtype == 'object':
        y = y.map(attack_mapping).fillna(y)
    
    # Encode labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    # Balance classes (like in your notebook)
    df = pd.concat([X, pd.Series(y_encoded, name='Label')], axis=1)
    target_samples = 5000
    
    balanced_dfs = []
    for class_label in df['Label'].unique():
        class_data = df[df['Label'] == class_label]
        current_count = len(class_data)
        
        if current_count > target_samples:
            class_data = resample(class_data, replace=False,
                                  n_samples=target_samples, random_state=42)
        elif current_count < target_samples:
            class_data = resample(class_data, replace=True,
                                  n_samples=target_samples, random_state=42)
        
        balanced_dfs.append(class_data)
    
    balanced_df = pd.concat(balanced_dfs)
    X_balanced = balanced_df.drop('Label', axis=1)
    y_balanced = balanced_df['Label']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_balanced, y_balanced, test_size=0.2, random_state=42, stratify=y_balanced
    )
    
    # Train Random Forest
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Calculate accuracy
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    return model, le, accuracy, X_test, y_test, X_train, y_train, X_balanced.columns

# ------------------------------
# 2. PREDICTION FUNCTION
# ------------------------------
def predict_and_explain(model, features, le, feature_names):
    """Make prediction and return explanation"""
    input_df = pd.DataFrame([features], columns=feature_names)
    input_df = input_df.replace([np.inf, -np.inf], np.nan).fillna(0)
    
    pred_encoded = model.predict(input_df)[0]
    attack_type = le.inverse_transform([pred_encoded])[0]
    
    # Get prediction probabilities
    probabilities = model.predict_proba(input_df)[0]
    prob_dict = {le.classes_[i]: prob for i, prob in enumerate(probabilities)}
    
    # Attack explanation and remediation
    explanations = {
        'BENIGN': {'emoji': '✅', 'message': 'Normal traffic - No action needed', 'severity': 'Low'},
        'Botnet': {'emoji': '🚨', 'message': 'Botnet activity detected - Isolate infected hosts immediately!', 'severity': 'Critical'},
        'BruteForce': {'emoji': '🚨', 'message': 'Brute force attack detected - Check authentication logs and enforce strong passwords', 'severity': 'High'},
        'DoS': {'emoji': '🚨', 'message': 'Denial of Service attack - Check network bandwidth and enable rate limiting', 'severity': 'High'},
        'Infiltration': {'emoji': '🚨', 'message': 'Infiltration detected - Investigate compromised systems immediately!', 'severity': 'Critical'},
        'Port_Scan': {'emoji': '⚠️', 'message': 'Port scan detected - Reconnaissance activity, harden firewall rules', 'severity': 'Medium'},
        'WebAttack': {'emoji': '🚨', 'message': 'Web attack detected - Check web server logs and WAF rules', 'severity': 'High'}
    }
    
    info = explanations.get(attack_type, {'emoji': '❓', 'message': 'Unknown activity detected', 'severity': 'Unknown'})
    
    return attack_type, info, prob_dict

# ------------------------------
# 3. VISUALIZATION FUNCTIONS
# ------------------------------
def plot_confusion_matrix(y_test, y_pred, classes):
    fig, ax = plt.subplots(figsize=(10, 8))
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=classes, yticklabels=classes, ax=ax)
    ax.set_title('Confusion Matrix', fontsize=14, fontweight='bold')
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig

def plot_feature_importance(model, feature_names, top_n=20):
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:top_n]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(range(top_n), importances[indices][::-1], color='steelblue')
    ax.set_yticks(range(top_n))
    ax.set_yticklabels([feature_names[i] for i in indices][::-1])
    ax.set_xlabel('Feature Importance')
    ax.set_title(f'Top {top_n} Most Important Features')
    ax.invert_yaxis()
    plt.tight_layout()
    return fig

def plot_probability_chart(prob_dict):
    fig, ax = plt.subplots(figsize=(10, 5))
    attacks = list(prob_dict.keys())
    probs = list(prob_dict.values())
    colors = ['#2ecc71' if a == 'BENIGN' else '#e74c3c' for a in attacks]
    bars = ax.bar(range(len(attacks)), probs, color=colors)
    ax.set_xticks(range(len(attacks)))
    ax.set_xticklabels(attacks, rotation=45, ha='right')
    ax.set_ylabel('Confidence Score')
    ax.set_title('Prediction Confidence by Attack Type')
    ax.set_ylim(0, 1)
    
    # Add value labels on bars
    for bar, prob in zip(bars, probs):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{prob:.2%}', ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    return fig

def plot_attack_distribution(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    attack_counts = data['Label'].value_counts()
    colors = ['#2ecc71' if x == 'BENIGN' else '#e74c3c' for x in attack_counts.index]
    bars = ax.bar(range(len(attack_counts)), attack_counts.values, color=colors)
    ax.set_xticks(range(len(attack_counts)))
    ax.set_xticklabels(attack_counts.index, rotation=45, ha='right')
    ax.set_title('Attack Distribution in Dataset')
    ax.set_ylabel('Number of Samples')
    
    for bar, count in zip(bars, attack_counts.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
                str(count), ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    return fig

# ------------------------------
# 4. MAIN APP
# ------------------------------
uploaded_file = st.sidebar.file_uploader("📂 Upload Network Logs (CSV)", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.sidebar.success(f"✅ Dataset Loaded: {data.shape[0]} rows, {data.shape[1]} columns")
    
    # Load/Train Model
    with st.spinner("Training model... This may take a moment..."):
        result = load_or_train_model(data)
    
    if result[0] is None:
        st.error("Failed to train model. Please check your dataset format.")
        st.stop()
    
    model, le, accuracy, X_test, y_test, X_train, y_train, feature_names = result
    
    # Sidebar metrics
    st.sidebar.metric("🎯 Model Accuracy", f"{accuracy*100:.2f}%")
    st.sidebar.metric("📊 Training Samples", f"{len(X_train):,}")
    st.sidebar.metric("🧪 Test Samples", f"{len(X_test):,}")
    st.sidebar.metric("🏷️ Attack Types", len(le.classes_))
    
    with st.sidebar.expander("📋 Attack Types Detected"):
        for i, attack in enumerate(le.classes_):
            st.write(f"{i+1}. {attack}")
    
    # ------------------------------
    # MAIN AREA: TABS
    # ------------------------------
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔎 Single Prediction", 
        "📁 Batch Prediction", 
        "📊 Model Performance",
        "🔬 Feature Analysis",
        "📖 About"
    ])
    
    # TAB 1: Single Prediction
    with tab1:
        st.subheader("🔎 Predict Network Traffic")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            row_num = st.number_input("Enter Row Number", min_value=0, max_value=len(data)-1, value=0, step=1)
            
            if st.button("🚀 Predict Attack", type="primary", use_container_width=True):
                # Get sample features
                if 'Label' in data.columns:
                    sample_features = data.drop('Label', axis=1).iloc[[row_num]].values.flatten()
                else:
                    sample_features = data.iloc[[row_num]].values.flatten()
                
                # Make prediction
                attack_type, info, probabilities = predict_and_explain(
                    model, sample_features, le, feature_names
                )
                
                # Display result with styling
                st.markdown("---")
                st.subheader("📋 Prediction Result")
                
                # Color-coded result box
                if attack_type == 'BENIGN':
                    st.success(f"{info['emoji']} **Prediction: {attack_type}**")
                else:
                    st.error(f"{info['emoji']} **ALERT: {attack_type} DETECTED!**")
                
                st.info(f"💡 **Explanation:** {info['message']}")
                st.metric("⚠️ Severity Level", info['severity'])
                
                # Show actual label if available
                if 'Label' in data.columns:
                    actual = data.iloc[row_num]['Label']
                    if actual != attack_type:
                        st.warning(f"📌 Note: Actual label was '{actual}' (Model may need improvement)")
                    else:
                        st.success(f"✅ Model predicted correctly!")
                
                # Show probability chart in the same column
                st.subheader("📊 Confidence Scores")
                prob_fig = plot_probability_chart(probabilities)
                st.pyplot(prob_fig)
                plt.close()
        
        with col2:
            st.subheader("📊 Attack Distribution")
            dist_fig = plot_attack_distribution(data)
            st.pyplot(dist_fig)
            plt.close()
        
        # Show sample data preview
        with st.expander("📄 View Dataset Preview"):
            st.dataframe(data.head(10))
    
    # TAB 2: Batch Prediction
    with tab2:
        st.subheader("📁 Batch Prediction on New Data")
        st.write("Upload a CSV file with the same features (without Label column) for batch prediction")
        
        batch_file = st.file_uploader("Upload Test CSV", type=["csv"], key="batch")
        
        if batch_file:
            batch_data = pd.read_csv(batch_file)
            st.write(f"📊 Uploaded: {batch_data.shape[0]} rows, {batch_data.shape[1]} columns")
            
            if st.button("🔮 Run Batch Prediction", type="primary"):
                with st.spinner("Processing predictions..."):
                    # Prepare features
                    X_batch = batch_data.copy()
                    X_batch = X_batch.replace([np.inf, -np.inf], np.nan).fillna(0)
                    
                    # Align columns with training data
                    for col in feature_names:
                        if col not in X_batch.columns:
                            X_batch[col] = 0
                    X_batch = X_batch[feature_names]
                    
                    # Predict
                    batch_preds = model.predict(X_batch)
                    batch_results = le.inverse_transform(batch_preds)
                    
                    # Add predictions to dataframe
                    batch_data['Predicted_Attack'] = batch_results
                    
                    # Show results
                    st.success("✅ Predictions Complete!")
                    st.dataframe(batch_data.head(20))
                    
                    # Summary statistics
                    st.subheader("📊 Prediction Summary")
                    pred_counts = pd.Series(batch_results).value_counts()
                    fig, ax = plt.subplots()
                    colors = ['#2ecc71' if x == 'BENIGN' else '#e74c3c' for x in pred_counts.index]
                    pred_counts.plot(kind='bar', ax=ax, color=colors)
                    ax.set_title('Distribution of Predictions')
                    ax.set_xlabel('Attack Type')
                    ax.set_ylabel('Count')
                    plt.xticks(rotation=45, ha='right')
                    st.pyplot(fig)
                    plt.close()
                    
                    # Download button
                    csv = batch_data.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "⬇️ Download Predictions as CSV",
                        csv,
                        "predictions.csv",
                        "text/csv",
                        use_container_width=True
                    )
    
    # TAB 3: Model Performance
    with tab3:
        st.subheader("📊 Model Performance Metrics")
        
        # Predict on test set
        y_pred = model.predict(X_test)
        y_pred_labels = le.inverse_transform(y_pred)
        y_test_labels = le.inverse_transform(y_test)
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🎯 Test Accuracy", f"{accuracy*100:.2f}%")
        with col2:
            precision = precision_score(y_test, y_pred, average='weighted')
            st.metric("📈 Weighted Precision", f"{precision*100:.2f}%")
        with col3:
            recall = recall_score(y_test, y_pred, average='weighted')
            st.metric("📉 Weighted Recall", f"{recall*100:.2f}%")
        
        # Classification Report
        st.subheader("📋 Detailed Classification Report")
        report = classification_report(y_test_labels, y_pred_labels, output_dict=True)
        report_df = pd.DataFrame(report).transpose()
        st.dataframe(report_df.style.format("{:.3f}"))
        
        # Confusion Matrix
        st.subheader("🗺️ Confusion Matrix")
        cm_fig = plot_confusion_matrix(y_test, y_pred, le.classes_)
        st.pyplot(cm_fig)
        plt.close()
    
    # TAB 4: Feature Analysis
    with tab4:
        st.subheader("🔬 Feature Importance Analysis")
        st.write("Which network features are most important for detecting attacks?")
        
        importance_fig = plot_feature_importance(model, feature_names, top_n=20)
        st.pyplot(importance_fig)
        plt.close()
        
        st.info("💡 **Insight:** Features with higher importance values play a bigger role in identifying malicious traffic. Focus on these features for network monitoring and anomaly detection.")
    
    # TAB 5: About
    with tab5:
        st.subheader("📖 About This System")
        st.markdown("""
        ### 🛡️ Multi-Class Intrusion Detection System
        
        **Model:** Random Forest Classifier  
        **Dataset:** CICIDS2017 (Network Intrusion Dataset)
        
        #### 🎯 Attack Types Detected:
        - ✅ **BENIGN** - Normal network traffic
        - 🚨 **DoS** - Denial of Service attacks
        - 🚨 **Port_Scan** - Network reconnaissance
        - 🚨 **BruteForce** - Password guessing attacks
        - 🚨 **Botnet** - Compromised device networks
        - 🚨 **WebAttack** - Web application attacks
        - 🚨 **Infiltration** - Network compromise attempts
        
        #### 🔧 How It Works:
        1. Upload a CSV file with network traffic features
        2. The model analyzes 77 different network features
        3. Real-time prediction with confidence scores
        4. Detailed explanations and remediation suggestions
        
        #### 📈 Performance:
        - Accuracy: ~99% on test data
        - Supports 7 attack categories + normal traffic
        - Fast inference for real-time detection
        """)

else:
    # Welcome message when no file uploaded
    st.info("👈 **Please upload a CSV dataset to begin**")
    
    st.markdown("""
    ### 🔐 Welcome to the Intrusion Detection System
    
    This system uses Machine Learning to detect various types of network attacks in real-time.
    
    #### 📂 Supported Dataset Format:
    - CSV file with network traffic features
    - Must contain a 'Label' column for training
    - Compatible with CICIDS2017 dataset format
    
    #### 🚀 Features:
    - Real-time attack prediction
    - Batch prediction on multiple samples
    - Confidence scores for each prediction
    - Feature importance analysis
    - Download prediction results
    
    #### 📊 Detects:
    - Normal traffic (BENIGN)
    - Denial of Service (DoS)
    - Port Scanning
    - Brute Force attacks
    - Botnet activity
    - Web attacks
    - Network infiltration
    """)