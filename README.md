🎓 PrepPredict - AI College Prediction System
An AI-powered web platform that helps students predict probable colleges based on KCET rank, provides career guidance, and offers interest-based branch recommendations using Machine Learning.

✨ Features
🎯 College Prediction
Predicts eligible colleges based on KCET rank and category
Uses Extra Trees ML algorithm with ~90% accuracy
Calculates admission probability for each college
Provides detailed college insights and recommendations
💡 Interest-Based Guidance
Recommends engineering branches based on student interests
Matches skills with career opportunities
Provides placement insights and career paths
Covers CSE, IT, ECE, EEE, MECH, CIVIL branches
📊 Analytics Dashboard
Visualize college distribution by location
Analyze branch popularity trends
View cutoff statistics and trends
Interactive charts and graphs
🛠️ Technology Stack
Frontend: Streamlit
ML Algorithm: Extra Trees Classifier (scikit-learn)
Data Processing: Pandas, NumPy
Visualization: Plotly
Deployment: Streamlit Cloud / Local
📋 Prerequisites
Python 3.8 or higher
pip (Python package manager)
Git
🚀 Installation & Setup
1. Clone the Repository
bash
git clone https://github.com/yourusername/PrepPredict.git
cd PrepPredict
2. Create Virtual Environment
bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
3. Install Dependencies
bash
pip install -r requirements.txt
4. Add Dataset
Place your CET-CUTOFF2025.xlsx or CET-CUTOFF2025.csv file in the project root directory.

Required columns in dataset:

College - College name
Branch - Branch/Department name
Location - City/Location
CETCode - College code
Caste category columns: GM, 1G, 2AG, 2BG, 3AG, etc.
5. Train the Model
bash
python train_model.py
This will:

Load and process the dataset
Train the Extra Trees model
Save trained model to models/ directory
Display accuracy and feature importance
6. Run the Application
bash
streamlit run app.py
The app will open in your browser at http://localhost:8501

🌐 Deployment to Streamlit Cloud
Method 1: Via GitHub
Push your code to GitHub:
bash
git add .
git commit -m "Initial commit"
git push origin main
Go to Streamlit Cloud
Sign in with GitHub
Click "New app"
Select your repository
Set main file path: app.py
Click "Deploy"
Method 2: Direct Upload
Ensure all files are in the project folder
Make sure models/ directory contains trained models
Upload to Streamlit Cloud interface
📁 Project Structure
prep_predict/
├── app.py                      # Main Streamlit application
├── train_model.py              # Model training script
├── utils.py                    # Helper functions
├── requirements.txt            # Python dependencies
├── .gitignore                 # Git ignore rules
├── README.md                  # Documentation
├── CET-CUTOFF2025.xlsx        # Dataset (Excel format)
└── models/                    # Trained models directory
    ├── ext_model.joblib       # Extra Trees model
    ├── label_encoder.joblib   # Label encoder
    └── feature_cols.joblib    # Feature columns
🎯 Usage Guide
College Prediction Module
Navigate to "🎯 College Prediction" page
Enter your KCET rank (1-200000)
Select your category (GM, 1G, 2AG, etc.)
Click "🔍 Predict Colleges"
View top 5 recommended colleges with:
Admission probability
Branch-specific insights
Career guidance
Placement information
Interest-Based Guidance
Go to "💡 Interest-Based Guidance"
Select your areas of interest (multiple allowed)
Get recommendations for:
Best matching branches
Skills you'll develop
Career opportunities
Average package ranges
Analytics Dashboard
Visit "📊 Analytics" page
Explore:
College distribution by location
Branch popularity analysis
Cutoff trends and statistics
🔧 Configuration
Updating Dataset
To use a new dataset:

Replace CET-CUTOFF2025.xlsx with your new file
Ensure column names match expected format
Retrain the model:
bash
python train_model.py
Model Parameters
Edit train_model.py to adjust:

n_estimators: Number of trees (default: 200)
max_depth: Maximum tree depth (default: 20)
test_size: Train-test split ratio (default: 0.2)
📊 Model Performance
Algorithm: Extra Trees Classifier
Accuracy: ~90%+
Features: Multiple caste category cutoffs
Target: College prediction based on rank
🤝 Contributing
Contributions are welcome! Please:

Fork the repository
Create a feature branch (git checkout -b feature/AmazingFeature)
Commit changes (git commit -m 'Add AmazingFeature')
Push to branch (git push origin feature/AmazingFeature)
Open a Pull Request
🐛 Troubleshooting
Dataset Not Found
Error: Dataset file missing
Solution: Ensure CET-CUTOFF2025.xlsx or CET-CUTOFF2025.csv is in project root.

Model Not Loaded
Warning: Model not trained
Solution: Run python train_model.py first.

Import Errors
ModuleNotFoundError: No module named 'streamlit'
Solution: Activate virtual environment and run pip install -r requirements.txt

Low Accuracy
Solution:

Check dataset quality
Ensure sufficient training data
Verify feature columns are present
📝 License
This project is open source and available for educational purposes.

👨‍💻 Authors
PrepPredict Development Team

🙏 Acknowledgments
Karnataka Examination Authority (KEA) for data structure reference
Streamlit for the amazing framework
scikit-learn for ML capabilities
📧 Support
For questions or issues:

Open an issue on GitHub
Contact: support@preppredict.com
Made with ❤️ for students preparing for KCET

