"""
Expense Tracker Web Application
"""
from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'data.json'

def load_data():
    """Load expense data from JSON file"""
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(expenses):
    """Save expense data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(expenses, f, indent=2)

def monthly_analysis(expenses):
    """Generate monthly spending analysis"""
    analysis = {}
    for expense in expenses:
        date = datetime.strptime(expense['date'], '%Y-%m-%d')
        month_key = f"{date.year}-{date.month:02d}"
        
        if month_key not in analysis:
            analysis[month_key] = {
                'total': 0,
                'categories': {}
            }
        
        analysis[month_key]['total'] += expense['amount']
        category = expense['category']
        if category not in analysis[month_key]['categories']:
            analysis[month_key]['categories'][category] = 0
        analysis[month_key]['categories'][category] += expense['amount']
    
    return analysis

@app.route('/')
def index():
    """Show recent expenses and basic overview"""
    expenses = load_data()
    return render_template('index.html', 
                         expenses=reversed(expenses[-10:]),  # Show last 10
                         total=sum(e['amount'] for e in expenses))

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    """Add new expense through form"""
    if request.method == 'POST':
        new_expense = {
            'date': request.form['date'],
            'category': request.form['category'],
            'amount': float(request.form['amount']),
            'description': request.form['description']
        }
        
        expenses = load_data()
        expenses.append(new_expense)
        save_data(expenses)
        
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/analysis')
def spending_analysis():
    """Show monthly spending breakdown"""
    expenses = load_data()
    analysis = monthly_analysis(expenses)
    return render_template('analysis.html', analysis=analysis)

if __name__ == '__main__':
    app.run(debug=True)