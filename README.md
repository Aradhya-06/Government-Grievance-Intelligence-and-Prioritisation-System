# Government Grievance Intelligence & Prioritization System

## Quick Setup

```bash
# 1. Virtual Environment Setup
python -m venv venv
# On Windows: venv\Scripts\activate

# 2. Install Dependencies
pip install django scikit-learn pandas numpy matplotlib seaborn plotly statsmodels scikit-fuzzy pdfplumber joblib

# 3. Apply Migrations & Seed Data
python manage.py makemigrations core accounts grievances analytics
python manage.py migrate
python manage.py seed_data

# 4. Run Development Server
python manage.py runserver