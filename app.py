import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score

# 1. Page Configuration
st.set_page_config(page_title="FCEWS: Crisis Simulator", layout="wide")

# 2. Sidebar: Profile & Simulator Controls
st.sidebar.title("Project Info")
st.sidebar.info("Developer: Jihu")
st.sidebar.markdown("Certification: **Columbia Business School** (AI for Business & Finance)")

st.sidebar.markdown("---")
st.sidebar.header("Crisis Simulator (Stress Test)")
st.sidebar.markdown("Adjust indicators to see how the AI reacts.")

# User Inputs (Sliders)
user_vix = st.sidebar.slider("Market Fear (VIX)", 10.0, 80.0, 15.0)
user_oil = st.sidebar.slider("Oil Price ($)", 20.0, 150.0, 75.0)
user_yield = st.sidebar.slider("Yield Spread (10Y-2Y)", -2.0, 3.0, 0.7)

st.title("Financial Crisis Early Warning System")
st.markdown("### AI-Powered Stress Testing & Risk Management")

# 3. Load Data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('financial_dataset.csv', index_col=0, parse_dates=True)
        return df
    except:
        return None

df = load_data()

if df is not None:
    # 4. Train AI Model (Background)
    df['Return'] = df['S&P500'].pct_change(20)
    df['Target'] = (df['Return'] < -0.05).astype(int)
    
    df['VIX_Lag'] = df['VIX'].shift(20)
    df['Oil_Lag'] = df['Oil'].shift(20)
    df['T10Y2Y_Lag'] = df['T10Y2Y'].shift(20)
    model_df = df.dropna()

    X = model_df[['VIX_Lag', 'Oil_Lag', 'T10Y2Y_Lag']]
    y = model_df['Target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    model.fit(X_train, y_train)
    
    # 5. Run Simulation
    input_data = pd.DataFrame({
        'VIX_Lag': [user_vix], 
        'Oil_Lag': [user_oil], 
        'T10Y2Y_Lag': [user_yield]
    })
    
    simulation_prob = model.predict_proba(input_data)[0][1]
    simulation_result = "CRASH WARNING" if simulation_prob > 0.5 else "STABLE"

    # 6. Dashboard Layout
    col1, col2 = st.columns([1, 2])

    # Left Column: Simulation Results
    with col1:
        st.subheader("Simulation Result")
        st.write(f"If **VIX** is **{user_vix}**, **Oil** is **${user_oil}**...")
        
        if simulation_prob > 0.5:
            st.error(f"Alert: {simulation_result}")
            st.metric("Crash Probability", f"{simulation_prob:.1%}", delta="-High Risk")
        else:
            st.success(f"Status: {simulation_result}")
            st.metric("Crash Probability", f"{simulation_prob:.1%}", delta="Safe")
            
        st.markdown("---")
        st.markdown("**AI Analyst Comment:**")
        if user_vix > 30:
            st.warning("The AI detects extreme market fear (High VIX). Historical patterns suggest a potential sell-off.")
        elif user_yield < 0:
            st.warning("The Yield Curve is inverted. This is a strong historical indicator of an incoming recession.")
        else:
            st.info("Current indicators suggest a stable market environment based on historical data.")

    # Right Column: Line Chart
    with col2:
        st.subheader("Real-time Data Visualization")
        recent_df = df.iloc[-252:] 
        
        fig, ax1 = plt.subplots(figsize=(10, 4.5))
        ax1.plot(recent_df.index, recent_df['S&P500'], color='tab:blue', label='S&P 500')
        ax1.set_ylabel('S&P 500', color='tab:blue')
        ax1.set_title("Market Trend (Last 1 Year)")
        ax1.grid(True, alpha=0.3)
        st.pyplot(fig)

    # 7. Bottom Section: Feature Importance (Bar Chart Restored!)
    st.divider()
    st.subheader("Model Insights: Key Drivers")
    st.markdown("Which economic indicators does the AI consider most important?")
    
    importance = pd.DataFrame({'Feature': X.columns, 'Importance': model.feature_importances_})
    st.bar_chart(importance.set_index('Feature'))

else:
    st.error("Data file not found. Please run 'data_collection.py' first.")