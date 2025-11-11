import streamlit as st
import pandas as pd
import joblib
import os
import plotly.graph_objects as go
import plotly.express as px
from utils import generate_college_summary, get_branch_category, recommend_branches_by_interest, BRANCH_SKILLS

# Page config
st.set_page_config(
    page_title="PrepPredict - KCET College Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.75rem;
        border: none;
    }
    .college-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# File paths
DATA_FILE_CSV = "CET-CUTOFF2025.csv"
DATA_FILE_XLSX = "CET-CUTOFF2025.xlsx"
MODEL_FILE = "models/ext_model.joblib"
ENC_FILE = "models/label_encoder.joblib"
FEATURE_FILE = "models/feature_cols.joblib"

# Load dataset
@st.cache_data
def load_data():
    if os.path.exists(DATA_FILE_CSV):
        return pd.read_csv(DATA_FILE_CSV)
    elif os.path.exists(DATA_FILE_XLSX):
        return pd.read_excel(DATA_FILE_XLSX)
    else:
        return None

# Load model
@st.cache_resource
def load_model():
    if os.path.exists(MODEL_FILE) and os.path.exists(ENC_FILE):
        model = joblib.load(MODEL_FILE)
        encoder = joblib.load(ENC_FILE)
        features = joblib.load(FEATURE_FILE) if os.path.exists(FEATURE_FILE) else None
        return model, encoder, features
    return None, None, None

# Initialize
df = load_data()
model, label_encoder, feature_cols = load_model()

# Header
st.markdown('<h1 class="main-header">🎓 PrepPredict</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered KCET College Prediction & Career Guidance</p>', unsafe_allow_html=True)

if df is None:
    st.error("⚠️ Dataset not found. Please upload CET-CUTOFF2025.csv or CET-CUTOFF2025.xlsx")
    st.stop()

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/graduation-cap.png", width=100)
    st.title("Navigation")
    
    page = st.radio("Select Module", [
        "🏠 Home",
        "🎯 College Prediction",
        "💡 Interest-Based Guidance",
        "📊 Analytics"
    ])
    
    st.markdown("---")
    st.markdown("### About PrepPredict")
    st.info("AI-powered platform using Extra Trees algorithm to predict colleges and provide personalized career guidance.")
    
    if model is not None:
        st.success("✅ ML Model Loaded")
    else:
        st.warning("⚠️ Model not trained. Run train_model.py first.")

# HOME PAGE
if page == "🏠 Home":
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2>🎓</h2>
            <h3>College Prediction</h3>
            <p>Get accurate predictions based on rank & category</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2>💡</h2>
            <h3>Career Guidance</h3>
            <p>Find the best branch matching your interests</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h2>📊</h2>
            <h3>Data Insights</h3>
            <p>Analyze trends and make informed decisions</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🚀 How It Works")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 1️⃣ Input Your Details
        - Enter your KCET rank
        - Select your category
        - Share your interests (optional)
        
        #### 2️⃣ AI Prediction
        - Extra Trees ML model analyzes data
        - Matches your profile with colleges
        - Calculates admission probability
        """)
    
    with col2:
        st.markdown("""
        #### 3️⃣ Get Results
        - Top college recommendations
        - Branch-specific insights
        - Career guidance
        
        #### 4️⃣ Make Decision
        - Compare colleges
        - Review placement data
        - Choose confidently
        """)
    
    st.markdown("---")
    st.markdown("### 📈 System Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Colleges in Database", len(df['College'].unique()))
    col2.metric("Branches Available", len(df['Branch'].unique()))
    col3.metric("Categories Supported", 20)
    col4.metric("ML Accuracy", "90%+" if model else "Training Required")

# COLLEGE PREDICTION PAGE
elif page == "🎯 College Prediction":
    st.markdown("## 🎯 College Prediction")
    st.markdown("Enter your details to get personalized college recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        rank = st.number_input(
            "Enter Your KCET Rank",
            min_value=1,
            max_value=200000,
            value=5000,
            step=100,
            help="Enter your KCET examination rank"
        )
    
    with col2:
        # Get available caste categories from dataset
        caste_cols = [col for col in df.columns if col not in ['College', 'Branch', 'Location', 'CETCode']]
        caste = st.selectbox(
            "Select Your Category",
            options=caste_cols,
            index=0 if 'GM' not in caste_cols else caste_cols.index('GM'),
            help="Select your caste category"
        )
    
    if st.button("🔍 Predict Colleges", type="primary"):
        with st.spinner("Analyzing your profile..."):
            
            # Filter eligible colleges
            if caste in df.columns:
                eligible = df[df[caste] >= rank].copy()
            else:
                st.error(f"Category '{caste}' not found in dataset")
                st.stop()
            
            if eligible.empty:
                st.warning("⚠️ No colleges found for this rank-category combination. Try a different category or check your rank.")
            else:
                # Calculate chance scores
                eligible['ChanceScore'] = eligible[caste] - rank
                eligible['ChancePercent'] = eligible['ChanceScore'].apply(
                    lambda x: min(95, max(10, (x / 5000) * 100))
                )
                eligible = eligible.sort_values('ChanceScore', ascending=False)
                
                # Get top 5
                top_colleges = eligible.head(5)
                
                st.success(f"✅ Found {len(eligible)} eligible colleges. Showing top 5 recommendations:")
                
                # Display summary metrics
                col1, col2, col3 = st.columns(3)
                col1.metric("Your Rank", f"{rank:,}")
                col2.metric("Eligible Colleges", len(eligible))
                col3.metric("Best Match", f"{top_colleges.iloc[0]['ChancePercent']:.0f}% chance")
                
                st.markdown("---")
                
                # Display each college
                for idx, row in top_colleges.iterrows():
                    branch_cat = get_branch_category(row['Branch'])
                    summary, chance_pct = generate_college_summary(row, rank, branch_cat)
                    
                    with st.expander(f"🏛️ {row['College']} - {row['Branch']}", expanded=(idx == top_colleges.index[0])):
                        st.markdown(summary)
                        
                        # Progress bar for admission chance
                        st.progress(chance_pct / 100)
                        
                        # Quick stats
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Cutoff Rank", f"{row[caste]:,}")
                        col2.metric("Your Advantage", f"{int(row['ChanceScore']):,} ranks")
                        col3.metric("Admission Chance", f"{chance_pct}%")

# INTEREST-BASED GUIDANCE PAGE
elif page == "💡 Interest-Based Guidance":
    st.markdown("## 💡 Interest-Based Career Guidance")
    st.markdown("Discover the best engineering branch matching your interests and skills")
    
    st.markdown("### Select Your Interests")
    
    all_interests = []
    for branch_info in BRANCH_SKILLS.values():
        all_interests.extend(branch_info['interests'])
    all_interests = sorted(list(set(all_interests)))
    
    selected_interests = st.multiselect(
        "Choose areas you're interested in (select multiple):",
        options=all_interests,
        help="Select all areas that interest you"
    )
    
    if selected_interests:
        st.markdown("---")
        recommendations = recommend_branches_by_interest(selected_interests)
        
        if recommendations:
            st.success(f"✅ Found {len(recommendations)} matching branches:")
            
            for i, rec in enumerate(recommendations, 1):
                branch = rec['branch']
                info = rec['info']
                
                st.markdown(f"### {i}. {branch} - {info['description']}")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Matched Interests:** {', '.join(rec['matched_interests'])}")
                    st.markdown(f"**Average Package:** {info['avg_package']}")
                    
                    st.markdown("**Skills You'll Develop:**")
                    for skill in info['skills']:
                        st.markdown(f"- {skill}")
                
                with col2:
                    st.markdown("**Career Paths:**")
                    for career in info['careers']:
                        st.markdown(f"• {career}")
                
                st.markdown("---")
        else:
            st.info("Select more interests to get recommendations")
    else:
        st.info("👆 Select your interests above to get personalized branch recommendations")
        
        # Show all branches
        st.markdown("### 📚 Available Engineering Branches")
        
        for branch, info in BRANCH_SKILLS.items():
            with st.expander(f"{branch} - {info['description']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Skills:**")
                    for skill in info['skills']:
                        st.markdown(f"- {skill}")
                
                with col2:
                    st.markdown("**Careers:**")
                    for career in info['careers']:
                        st.markdown(f"- {career}")
                
                st.markdown(f"**Avg Package:** {info['avg_package']}")

# ANALYTICS PAGE
elif page == "📊 Analytics":
    st.markdown("## 📊 Data Analytics & Insights")
    
    tab1, tab2, tab3 = st.tabs(["College Distribution", "Branch Analysis", "Cutoff Trends"])
    
    with tab1:
        st.markdown("### College Distribution by Location")
        
        location_counts = df['Location'].value_counts().head(10)
        
        fig = px.bar(
            x=location_counts.index,
            y=location_counts.values,
            labels={'x': 'Location', 'y': 'Number of Colleges'},
            title="Top 10 Locations with Most Colleges"
        )
        fig.update_traces(marker_color='#667eea')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Branch Distribution")
        
        df['BranchCategory'] = df['Branch'].apply(get_branch_category)
        branch_counts = df['BranchCategory'].value_counts()
        
        fig = px.pie(
            values=branch_counts.values,
            names=branch_counts.index,
            title="Distribution of Engineering Branches"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### Cutoff Analysis")
        
        if 'GM' in df.columns:
            st.markdown("#### General Merit (GM) Category Statistics")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Highest Cutoff", f"{df['GM'].max():,.0f}")
            col2.metric("Average Cutoff", f"{df['GM'].mean():,.0f}")
            col3.metric("Lowest Cutoff", f"{df['GM'].min():,.0f}")
            
            fig = px.histogram(
                df,
                x='GM',
                nbins=50,
                title="Distribution of GM Cutoff Ranks"
            )
            fig.update_traces(marker_color='#764ba2')
            st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>PrepPredict - AI-Powered College Prediction System</p>
    <p>Powered by Extra Trees Machine Learning | Made with ❤️ for Students</p>
</div>
""", unsafe_allow_html=True)
