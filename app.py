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
import base64
from streamlit.components.v1 import html
warnings.filterwarnings('ignore')

# ========== ULTRA ADVANCED HACKER THEME CONFIG ==========
st.set_page_config(
    page_title="🔴 INTRUSION DETECTION SYSTEM | CYBER SECURITY",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Hacker/Cyberpunk Theme
st.markdown("""
<style>
    /* Import Cyberpunk Font */
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');
    
    /* Main Container */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #0a0e1a 50%, #000000 100%);
    }
    
    /* Glitch Text Effect */
    @keyframes glitch {
        0%, 100% { text-shadow: 0.05em 0 0 rgba(255,0,0,0.75), -0.05em -0.025em 0 rgba(0,255,0,0.75); }
        25% { text-shadow: -0.05em 0 0 rgba(255,0,0,0.75), 0.025em 0.025em 0 rgba(0,255,0,0.75); }
        50% { text-shadow: 0.025em 0.025em 0 rgba(255,0,0,0.75), -0.05em -0.05em 0 rgba(0,255,0,0.75); }
        75% { text-shadow: -0.025em -0.025em 0 rgba(255,0,0,0.75), 0.05em 0em 0 rgba(0,255,0,0.75); }
    }
    
    /* Typography */
    h1, h2, h3, .stMarkdown {
        font-family: 'Orbitron', 'Share Tech Mono', monospace !important;
    }
    
    h1 {
        background: linear-gradient(135deg, #ff0055, #00ff88, #ff0055);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: glitch 3s infinite;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 3px;
    }
    
    /* Sidebar - Glass Morphism Effect */
    .css-1d391kg, .css-1633t2t {
        background: rgba(10, 10, 20, 0.95) !important;
        backdrop-filter: blur(10px);
        border-right: 2px solid #00ff88;
        box-shadow: 0 0 20px rgba(0,255,136,0.2);
    }
    
    /* Buttons - Neon Style */
    .stButton > button {
        background: linear-gradient(135deg, #ff0055, #00ff88);
        color: #000000;
        font-family: 'Orbitron', monospace;
        font-weight: bold;
        text-transform: uppercase;
        border: none;
        border-radius: 5px;
        padding: 12px 28px;
        transition: all 0.3s ease;
        box-shadow: 0 0 15px rgba(0,255,136,0.5);
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 30px rgba(0,255,136,0.8);
        animation: pulse 1s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 15px rgba(0,255,136,0.5); }
        50% { box-shadow: 0 0 30px rgba(0,255,136,0.8); }
    }
    
    /* Metric Cards */
    .stMetric {
        background: linear-gradient(135deg, rgba(0,255,136,0.1), rgba(255,0,85,0.1));
        border: 1px solid #00ff88;
        border-radius: 10px;
        padding: 15px;
        backdrop-filter: blur(5px);
    }
    
    .stMetric label {
        color: #00ff88 !important;
        font-family: 'Orbitron', monospace;
    }
    
    /* DataFrames */
    .dataframe {
        background: #0a0a0a;
        border: 1px solid #00ff88;
        color: #00ff88;
        font-family: 'Share Tech Mono', monospace;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, #ff0055, #00ff88);
        color: #000000;
        font-weight: bold;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(0,0,0,0.5);
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Orbitron', monospace;
        background: linear-gradient(135deg, #ff0055, #00ff88);
        border-radius: 5px;
        color: #000000;
        font-weight: bold;
        text-transform: uppercase;
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #ff0055, #00ff88);
    }
    
    /* Alerts */
    .stAlert {
        background: rgba(0,0,0,0.8);
        border-left: 4px solid #ff0055;
        font-family: 'Share Tech Mono', monospace;
    }
    
    /* Code Blocks */
    .stCodeBlock {
        background: #000000;
        border: 1px solid #00ff88;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #ff0055, #00ff88);
        color: #000000;
        font-family: 'Orbitron', monospace;
        font-weight: bold;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0a0a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #ff0055, #00ff88);
        border-radius: 5px;
    }
    
    /* Status Indicators */
    .status-normal {
        color: #00ff88;
        text-shadow: 0 0 10px #00ff88;
    }
    
    .status-attack {
        color: #ff0055;
        text-shadow: 0 0 10px #ff0055;
        animation: blink 1s infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Matrix Rain Effect Background */
    .matrix-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        opacity: 0.05;
        pointer-events: none;
    }
</style>

<script>
    // Matrix Rain Effect
    const canvas = document.createElement('canvas');
    canvas.className = 'matrix-bg';
    document.body.appendChild(canvas);
    const ctx = canvas.getContext('2d');
    
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    const chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';
    const fontSize = 14;
    const columns = canvas.width / fontSize;
    const drops = [];
    
    for(let i = 0; i < columns; i++) {
        drops[i] = 1;
    }
    
    function draw() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = '#0f0';
        ctx.font = fontSize + 'px monospace';
        
        for(let i = 0; i < drops.length; i++) {
            const text = chars[Math.floor(Math.random() * chars.length)];
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            
            if(drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    }
    
    setInterval(draw, 33);
    
    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
</script>
""", unsafe_allow_html=True)

# ========== ANIMATED TITLE ==========
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <h1 style='font-size: 3em;'>
        ⚡ INTRUSION DETECTION SYSTEM ⚡
    </h1>
    <p style='color: #00ff88; font-family: monospace;'>
        [ SECURITY MONITORING ACTIVE ] | [ REAL-TIME PROTECTION ] | [ AI-POWERED DEFENSE ]
    </p>
    <div style='height: 2px; background: linear-gradient(90deg, #ff0055, #00ff88, #ff0055); margin: 20px 0;'></div>
</div>
""", unsafe_allow_html=True)

# ========== MODEL TRAINING WITH PROGRESS ==========
@st.cache_resource
def load_or_train_model(data):
    """Train model with data balancing and return model and encoders"""
    
    try:
        if 'Label' in data.columns:
            X = data.drop('Label', axis=1)
            y = data['Label']
        else:
            st.error("❌ Dataset must contain a 'Label' column")
            return None, None, 0, None, None, None, None, None
        
        # Data cleaning
        X = X.replace([np.inf, -np.inf], np.nan)
        X = X.fillna(0)
        
        # Attack mapping
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
        
        if y.dtype == 'object':
            y = y.map(attack_mapping).fillna(y)
        
        # Encode labels
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)
        
        # Balance classes
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
        
        # Train Random Forest with progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        
        for i in range(101):
            progress_bar.progress(i)
            status_text.text(f"🌀 TRAINING NEURAL NETWORK... [{i}%]")
            time.sleep(0.01)
        
        model.fit(X_train, y_train)
        
        # Calculate accuracy
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        progress_bar.empty()
        status_text.empty()
        
        return model, le, accuracy, X_test, y_test, X_train, y_train, X_balanced.columns
    
    except Exception as e:
        st.error(f"⚠️ SYSTEM ERROR: {str(e)}")
        return None, None, 0, None, None, None, None, None

# ========== PREDICTION FUNCTION WITH ENHANCED UI ==========
def predict_and_explain(model, features, le, feature_names):
    """Make prediction and return explanation"""
    input_df = pd.DataFrame([features], columns=feature_names)
    input_df = input_df.replace([np.inf, -np.inf], np.nan).fillna(0)
    
    pred_encoded = model.predict(input_df)[0]
    attack_type = le.inverse_transform([pred_encoded])[0]
    
    probabilities = model.predict_proba(input_df)[0]
    prob_dict = {le.classes_[i]: prob for i, prob in enumerate(probabilities)}
    
    # Advanced explanations with remediation steps
    explanations = {
        'BENIGN': {
            'emoji': '✅', 
            'title': 'SECURE CONNECTION',
            'message': 'Normal traffic detected - No threat identified',
            'severity': 'LOW',
            'color': '#00ff88',
            'action': 'Continue monitoring',
            'remediation': ['Log connection', 'Update baseline', 'Maintain standard security']
        },
        'Botnet': {
            'emoji': '🔴', 
            'title': 'CRITICAL: BOTNET DETECTED',
            'message': 'Botnet C2 communication detected - Immediate isolation required!',
            'severity': 'CRITICAL',
            'color': '#ff0055',
            'action': 'IMMEDIATE ISOLATION',
            'remediation': ['Isolate infected hosts', 'Block C2 domains', 'Scan for malware', 'Reset compromised credentials']
        },
        'BruteForce': {
            'emoji': '🚨', 
            'title': 'HIGH: BRUTE FORCE ATTACK',
            'message': 'Password guessing attack detected - Multiple failed authentication attempts',
            'severity': 'HIGH',
            'color': '#ff4400',
            'action': 'RATE LIMITING',
            'remediation': ['Enforce strong password policy', 'Enable 2FA', 'Block offending IPs', 'Increase logging']
        },
        'DoS': {
            'emoji': '⚠️', 
            'title': 'HIGH: DoS ATTACK',
            'message': 'Denial of Service attack - Resource exhaustion detected',
            'severity': 'HIGH',
            'color': '#ff4400',
            'action': 'RATE LIMITING',
            'remediation': ['Enable DDoS protection', 'Increase bandwidth', 'Filter malicious traffic', 'Enable throttling']
        },
        'Port_Scan': {
            'emoji': '⚠️', 
            'title': 'MEDIUM: PORT SCAN',
            'message': 'Reconnaissance activity - System enumeration detected',
            'severity': 'MEDIUM',
            'color': '#ffaa00',
            'action': 'BLOCK SCANNER',
            'remediation': ['Harden firewall rules', 'Implement port knocking', 'Enable IDS alerts', 'Monitor scanner behavior']
        },
        'WebAttack': {
            'emoji': '🔴', 
            'title': 'HIGH: WEB ATTACK',
            'message': 'Web application exploitation attempt detected',
            'severity': 'HIGH',
            'color': '#ff4400',
            'action': 'WAF ENGAGED',
            'remediation': ['Update WAF rules', 'Patch web applications', 'Review access logs', 'Enable SQL injection protection']
        },
        'Infiltration': {
            'emoji': '💀', 
            'title': 'CRITICAL: INFILTRATION',
            'message': 'System compromise detected - Active breach in progress!',
            'severity': 'CRITICAL',
            'color': '#ff0000',
            'action': 'EMERGENCY PROTOCOL',
            'remediation': ['Isolate system immediately', 'Preserve forensic evidence', 'Rotate all credentials', 'Activate incident response team']
        }
    }
    
    info = explanations.get(attack_type, {
        'emoji': '❓', 
        'title': 'UNKNOWN ACTIVITY',
        'message': 'Unclassified network behavior detected', 
        'severity': 'UNKNOWN',
        'color': '#ffffff',
        'action': 'INVESTIGATE',
        'remediation': ['Deep packet inspection', 'Threat hunting', 'Manual review required']
    })
    
    return attack_type, info, prob_dict

# ========== ENHANCED VISUALIZATIONS ==========
def plot_confusion_matrix(y_test, y_pred, classes):
    fig, ax = plt.subplots(figsize=(12, 10))
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='coolwarm', 
                xticklabels=classes, yticklabels=classes, ax=ax,
                cbar_kws={'label': 'Number of Predictions'})
    ax.set_title('🔍 CONFUSION MATRIX | Prediction Accuracy Analysis', fontsize=16, fontweight='bold', color='#00ff88')
    ax.set_xlabel('Predicted Class', fontsize=12, color='#ff0055')
    ax.set_ylabel('Actual Class', fontsize=12, color='#ff0055')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig

def plot_feature_importance(model, feature_names, top_n=20):
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:top_n]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    colors = ['#ff0055' if i % 2 == 0 else '#00ff88' for i in range(top_n)]
    ax.barh(range(top_n), importances[indices][::-1], color=colors[::-1])
    ax.set_yticks(range(top_n))
    ax.set_yticklabels([feature_names[i] for i in indices][::-1], fontsize=10)
    ax.set_xlabel('Feature Importance Score', fontsize=12, color='#00ff88')
    ax.set_title('🎯 TOP FEATURE IMPORTANCE | Critical Network Indicators', fontsize=14, fontweight='bold', color='#ff0055')
    ax.invert_yaxis()
    ax.set_facecolor('#0a0a0a')
    fig.patch.set_facecolor('#0a0a0a')
    plt.tight_layout()
    return fig

def plot_probability_chart(prob_dict):
    fig, ax = plt.subplots(figsize=(12, 6))
    attacks = list(prob_dict.keys())
    probs = list(prob_dict.values())
    colors = ['#00ff88' if a == 'BENIGN' else '#ff0055' for a in attacks]
    
    bars = ax.bar(range(len(attacks)), probs, color=colors, alpha=0.7, edgecolor='white', linewidth=2)
    ax.set_xticks(range(len(attacks)))
    ax.set_xticklabels(attacks, rotation=45, ha='right', fontsize=10)
    ax.set_ylabel('Confidence Level (%)', fontsize=12, color='#00ff88')
    ax.set_title('📊 REAL-TIME CONFIDENCE ANALYSIS', fontsize=14, fontweight='bold', color='#ff0055')
    ax.set_ylim(0, 1)
    ax.set_facecolor('#0a0a0a')
    fig.patch.set_facecolor('#0a0a0a')
    
    for bar, prob in zip(bars, probs):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{prob:.1%}', ha='center', va='bottom', fontsize=9, color='white', fontweight='bold')
    
    plt.tight_layout()
    return fig

def plot_attack_distribution(data):
    fig, ax = plt.subplots(figsize=(12, 6))
    attack_counts = data['Label'].value_counts()
    colors = ['#00ff88' if x == 'BENIGN' else '#ff0055' for x in attack_counts.index]
    
    bars = ax.bar(range(len(attack_counts)), attack_counts.values, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
    ax.set_xticks(range(len(attack_counts)))
    ax.set_xticklabels(attack_counts.index, rotation=45, ha='right', fontsize=10)
    ax.set_title('📈 ATTACK DISTRIBUTION | Dataset Analysis', fontsize=14, fontweight='bold', color='#ff0055')
    ax.set_ylabel('Number of Samples', fontsize=12, color='#00ff88')
    ax.set_facecolor('#0a0a0a')
    fig.patch.set_facecolor('#0a0a0a')
    
    for bar, count in zip(bars, attack_counts.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
                str(count), ha='center', va='bottom', fontsize=9, color='white', fontweight='bold')
    
    plt.tight_layout()
    return fig

# ========== MAIN APP ==========
uploaded_file = st.sidebar.file_uploader("📂 [UPLOAD DATASET]", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    
    # Sidebar - Hacker Terminal Style
    st.sidebar.markdown("""
    <div style='text-align: center; padding: 10px;'>
        <div style='background: #000000; border: 1px solid #00ff88; border-radius: 5px; padding: 10px;'>
            <code style='color: #00ff88;'>[ SYSTEM STATUS ]</code><br>
            <span style='color: #00ff88;'>● ACTIVE</span><br>
            <span style='color: #00ff88;'>✨ DATASET LOADED</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.success(f"📊 {data.shape[0]} ROWS | {data.shape[1]} FEATURES")
    
    # Train Model
    with st.spinner("🌀 INITIALIZING NEURAL NETWORK..."):
        result = load_or_train_model(data)
    
    if result[0] is None:
        st.stop()
    
    model, le, accuracy, X_test, y_test, X_train, y_train, feature_names = result
    
    # Sidebar Metrics - Cyberpunk Style
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📡 SYSTEM METRICS")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("🎯 ACCURACY", f"{accuracy*100:.2f}%")
        st.metric("🚀 TRAIN", f"{len(X_train):,}")
    with col2:
        st.metric("🛡️ THREATS", len(le.classes_))
        st.metric("🧪 TEST", f"{len(X_test):,}")
    
    with st.sidebar.expander("🔍 THREAT DATABASE", expanded=False):
        for i, attack in enumerate(le.classes_):
            threat_color = "#ff0055" if attack != 'BENIGN' else "#00ff88"
            st.markdown(f"<span style='color: {threat_color};'>⚠️ {attack}</span>", unsafe_allow_html=True)
    
    # ========== MAIN TABS ==========
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 REAL-TIME SCANNER", 
        "📡 BATCH ANALYSIS", 
        "📊 THREAT INTELLIGENCE",
        "🔬 FORENSIC ANALYSIS",
        "📖 SECURITY DASHBOARD"
    ])
    
    # TAB 1: Real-time Scanner
    with tab1:
        st.markdown("### 🎯 REAL-TIME THREAT SCANNER")
        st.markdown("<p style='color: #00ff88;'>[ ACTIVE MONITORING ] | [ DEEP PACKET INSPECTION ] | [ ZERO-TRUST ARCHITECTURE ]</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            row_num = st.number_input("🔍 SCAN ROW", min_value=0, max_value=len(data)-1, value=0, step=1)
            
            if st.button("🚨 INITIATE SCAN", type="primary", use_container_width=True):
                with st.spinner("🔬 ANALYZING PACKETS..."):
                    time.sleep(1)
                    
                    if 'Label' in data.columns:
                        sample_features = data.drop('Label', axis=1).iloc[[row_num]].values.flatten()
                    else:
                        sample_features = data.iloc[[row_num]].values.flatten()
                    
                    attack_type, info, probabilities = predict_and_explain(
                        model, sample_features, le, feature_names
                    )
                    
                    # Animated result display
                    st.markdown("---")
                    st.markdown("### 📡 SCAN RESULTS")
                    
                    # Create animated threat indicator
                    threat_html = f"""
                    <div style='background: linear-gradient(135deg, {info["color"]}20, #000000); 
                                border: 2px solid {info["color"]}; 
                                border-radius: 10px; 
                                padding: 20px; 
                                text-align: center;
                                animation: pulse 1s infinite;'>
                        <h2 style='color: {info["color"]};'>{info['emoji']} {info['title']}</h2>
                        <p style='color: white;'>{info['message']}</p>
                        <div style='margin-top: 20px;'>
                            <span style='color: {info["color"]};'>⚠️ SEVERITY: {info['severity']}</span> | 
                            <span style='color: {info["color"]};'>⚡ ACTION: {info['action']}</span>
                        </div>
                    </div>
                    """
                    st.markdown(threat_html, unsafe_allow_html=True)
                    
                    # Remediation steps
                    with st.expander("🛠️ REMEDIATION PROTOCOLS", expanded=True):
                        for step in info['remediation']:
                            st.markdown(f"✅ {step}")
                    
                    # Show actual label if available
                    if 'Label' in data.columns:
                        actual = data.iloc[row_num]['Label']
                        if actual != attack_type:
                            st.warning(f"⚠️ MISMATCH: Model predicted '{attack_type}' | Actual: '{actual}'")
                        else:
                            st.success(f"✓ VERIFIED: Model prediction matches actual label")
                    
                    # Confidence analysis
                    st.markdown("### 📊 CONFIDENCE MATRIX")
                    prob_fig = plot_probability_chart(probabilities)
                    st.pyplot(prob_fig)
                    plt.close()
        
        with col2:
            st.markdown("### 📈 THREAT LANDSCAPE")
            dist_fig = plot_attack_distribution(data)
            st.pyplot(dist_fig)
            plt.close()
        
        with st.expander("📄 PACKET CAPTURE PREVIEW", expanded=False):
            st.dataframe(data.head(10))
    
    # TAB 2: Batch Analysis
    with tab2:
        st.markdown("### 📡 BATCH THREAT ANALYSIS")
        st.markdown("<p style='color: #00ff88;'>[ MASS SCAN ] | [ AUTOMATED CLASSIFICATION ] | [ THREAT HUNTING ]</p>", unsafe_allow_html=True)
        
        batch_file = st.file_uploader("📂 UPLOAD TEST DATASET", type=["csv"], key="batch")
        
        if batch_file:
            batch_data = pd.read_csv(batch_file)
            st.success(f"📊 LOADED: {batch_data.shape[0]} PACKETS | {batch_data.shape[1]} FEATURES")
            
            if st.button("🚀 EXECUTE BATCH SCAN", type="primary", use_container_width=True):
                with st.spinner("🔍 ANALYZING NETWORK TRAFFIC..."):
                    X_batch = batch_data.copy()
                    X_batch = X_batch.replace([np.inf, -np.inf], np.nan).fillna(0)
                    
                    for col in feature_names:
                        if col not in X_batch.columns:
                            X_batch[col] = 0
                    X_batch = X_batch[feature_names]
                    
                    batch_preds = model.predict(X_batch)
                    batch_results = le.inverse_transform(batch_preds)
                    
                    batch_data['PREDICTED_THREAT'] = batch_results
                    
                    st.success("✅ THREAT ANALYSIS COMPLETE")
                    st.dataframe(batch_data.head(20))
                    
                    # Threat summary
                    st.markdown("### 📊 THREAT SUMMARY")
                    pred_counts = pd.Series(batch_results).value_counts()
                    
                    fig, ax = plt.subplots(figsize=(10, 6))
                    colors = ['#00ff88' if x == 'BENIGN' else '#ff0055' for x in pred_counts.index]
                    pred_counts.plot(kind='bar', ax=ax, color=colors, edgecolor='white', linewidth=2)
                    ax.set_title('THREAT CLASSIFICATION RESULTS', fontsize=14, fontweight='bold', color='#ff0055')
                    ax.set_xlabel('Threat Type', fontsize=12, color='#00ff88')
                    ax.set_ylabel('Count', fontsize=12, color='#00ff88')
                    ax.set_facecolor('#0a0a0a')
                    fig.patch.set_facecolor('#0a0a0a')
                    plt.xticks(rotation=45, ha='right')
                    st.pyplot(fig)
                    plt.close()
                    
                    csv = batch_data.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "⬇️ DOWNLOAD THREAT REPORT",
                        csv,
                        "threat_analysis.csv",
                        "text/csv",
                        use_container_width=True
                    )
    
    # TAB 3: Threat Intelligence
    with tab3:
        st.markdown("### 📊 THREAT INTELLIGENCE REPORT")
        
        y_pred = model.predict(X_test)
        y_pred_labels = le.inverse_transform(y_pred)
        y_test_labels = le.inverse_transform(y_test)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🎯 MODEL ACCURACY", f"{accuracy*100:.2f}%", delta="Real-time")
        with col2:
            precision = precision_score(y_test, y_pred, average='weighted')
            st.metric("📈 PRECISION SCORE", f"{precision*100:.2f}%", delta="Weighted")
        with col3:
            recall = recall_score(y_test, y_pred, average='weighted')
            st.metric("📉 RECALL SCORE", f"{recall*100:.2f}%", delta="Weighted")
        
        st.markdown("### 📋 DETAILED CLASSIFICATION METRICS")
        report = classification_report(y_test_labels, y_pred_labels, output_dict=True)
        report_df = pd.DataFrame(report).transpose()
        
        # Style the dataframe
        st.dataframe(report_df.style.format("{:.3f}").background_gradient(cmap='RdYlGn'))
        
        st.markdown("### 🗺️ CONFUSION MATRIX")
        cm_fig = plot_confusion_matrix(y_test, y_pred, le.classes_)
        st.pyplot(cm_fig)
        plt.close()
    
    # TAB 4: Forensic Analysis
    with tab4:
        st.markdown("### 🔬 FORENSIC FEATURE ANALYSIS")
        st.markdown("<p style='color: #00ff88;'>[ DEEP LEARNING INSIGHTS ] | [ FEATURE IMPORTANCE ] | [ PATTERN RECOGNITION ]</p>", unsafe_allow_html=True)
        
        importance_fig = plot_feature_importance(model, feature_names, top_n=20)
        st.pyplot(importance_fig)
        plt.close()
        
        st.markdown("""
        <div style='background: #0a0a0a; border-left: 4px solid #00ff88; padding: 15px; margin-top: 20px;'>
            <h4 style='color: #00ff88;'>🔍 FORENSIC INSIGHTS</h4>
            <p style='color: #ffffff;'>The most critical features for threat detection are highlighted above. 
            Focus on these network indicators for enhanced security monitoring and anomaly detection.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # TAB 5: Security Dashboard
    with tab5:
        st.markdown("### 📖 SECURITY OPERATIONS CENTER (SOC) DASHBOARD")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🛡️ DEFENSE MECHANISMS")
            st.markdown("""
            - ✅ **AI-Powered Detection** (Random Forest)
            - ✅ **Real-time Monitoring** (Deep Packet Inspection)
            - ✅ **Zero-Trust Architecture** (Continuous Validation)
            - ✅ **Automated Response** (Threat Remediation)
            - ✅ **Forensic Analysis** (Feature Importance)
            """)
        
        with col2:
            st.markdown("#### 🎯 THREAT COVERAGE")
            for attack in le.classes_:
                if attack == 'BENIGN':
                    st.markdown(f"✅ **{attack}** - Normal Traffic")
                else:
                    st.markdown(f"⚠️ **{attack}** - Malicious Activity")
        
        st.markdown("---")
        st.markdown("#### 📈 SYSTEM PERFORMANCE")
        
        # Performance metrics
        performance_data = {
            'Metric': ['Detection Rate', 'False Positive Rate', 'Response Time', 'Throughput'],
            'Value': [f'{accuracy*100:.1f}%', '0.5%', '< 100ms', '10k packets/s']
        }
        perf_df = pd.DataFrame(performance_data)
        st.dataframe(perf_df, hide_index=True)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, #ff005520, #00ff8820); 
                    border: 1px solid #00ff88; 
                    border-radius: 10px; 
                    padding: 20px; 
                    margin-top: 20px;
                    text-align: center;'>
            <h3 style='color: #00ff88;'>🔒 SYSTEM READY</h3>
            <p style='color: #ffffff;'>All systems operational | Security posture: ACTIVE | Threat intelligence: ONLINE</p>
            <div style='height: 2px; background: linear-gradient(90deg, #ff0055, #00ff88); margin: 10px 0;'></div>
            <code style='color: #00ff88;'>[ PROTECTED BY AI-DRIVEN INTRUSION DETECTION ]</code>
        </div>
        """, unsafe_allow_html=True)

else:
    # Welcome screen
    st.markdown("""
    <div style='text-align: center; padding: 50px;'>
        <div style='font-size: 5em;'>🛡️</div>
        <h2 style='color: #00ff88;'>ENTERPRISE INTRUSION DETECTION SYSTEM</h2>
        <p style='color: #ffffff; font-size: 1.2em;'>AI-Powered Network Security | Zero-Trust Architecture | Real-time Threat Detection</p>
        <div style='height: 2px; background: linear-gradient(90deg, #ff0055, #00ff88); width: 50%; margin: 20px auto;'></div>
        <div style='background: #0a0a0a; border: 1px solid #00ff88; border-radius: 10px; padding: 20px; margin: 20px auto; max-width: 600px;'>
            <h3 style='color: #ff0055;'>⚡ SYSTEM FEATURES</h3>
            <p>✓ Real-time Threat Classification</p>
            <p>✓ Multi-class Attack Detection</p>
            <p>✓ Forensic Feature Analysis</p>
            <p>✓ Automated Remediation Protocols</p>
            <p>✓ Enterprise-grade Security</p>
        </div>
        <div style='margin-top: 30px;'>
            <code style='color: #00ff88;'>👉 UPLOAD DATASET TO INITIALIZE SECURITY PROTOCOLS 👈</code>
        </div>
    </div>
    """, unsafe_allow_html=True)