import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()
np.random.seed(42)
random.seed(42)

# Constants
RECIPIENT_CATEGORIES = [
    'food', 'transportation', 'fashion', 'insurance', 'investment', 
    'utility', 'telco', 'rental', 'insurance', 'credit card payment', 
    'buy now pay later', 'mortgage loan', 'installments', 'gym membership', 
    'taxes', 'groceries'
]

NECESSITY_CATEGORIES = [
    'food', 'transportation', 'utility', 'telco', 'rental', 'insurance',
    'mortgage loan', 'taxes', 'groceries'
]

def generate_monthly_transactions(user_id, month_date):
    """Generate transactions for a single user for a specific month"""
    num_transactions = random.randint(3, 8)  # Random number of categories per month
    transactions = []
    
    # Randomly select categories for this month
    month_categories = random.sample(RECIPIENT_CATEGORIES, num_transactions)
    
    for category in month_categories:
        # Generate transaction amount based on category
        if category in ['investment', 'mortgage loan']:
            amount = round(random.uniform(1000, 10000), 2)
        elif category in ['fashion', 'buy now pay later']:
            amount = round(random.uniform(50, 500), 2)
        else:
            amount = round(random.uniform(10, 1000), 2)
            
        transactions.append({
            'userid': user_id,
            'spending_amount': amount,
            'receipient_category': category,
            'Necessities_or_non_essential': category in NECESSITY_CATEGORIES,
            'timestamp': month_date + timedelta(days=random.randint(0, 27))
        })
    
    return transactions

def generate_transaction_data(num_users=100, num_transactions=2000):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)  # Last 6 months
    
    transactions = []
    user_ids = [str(i).zfill(6) for i in range(num_users)]  # 6-digit user IDs
    
    # Generate transactions for each month for each user
    for user_id in user_ids:
        for month in range(6):
            month_date = end_date - timedelta(days=30 * month)
            transactions.extend(generate_monthly_transactions(user_id, month_date))
    
    # Randomly select transactions to match desired total
    if len(transactions) > num_transactions:
        transactions = random.sample(transactions, num_transactions)
    
    return pd.DataFrame(transactions)

def calculate_monthly_metrics(user_transactions):
    """Calculate financial metrics based on monthly transactions"""
    total_spending = user_transactions['spending_amount'].sum()
    luxury_spending = user_transactions[~user_transactions['Necessities_or_non_essential']]['spending_amount'].sum()
    necessity_spending = user_transactions[user_transactions['Necessities_or_non_essential']]['spending_amount'].sum()
    
    return {
        'total_spending': total_spending,
        'impulsive_purchase_rate': round((luxury_spending / total_spending * 100) if total_spending > 0 else 0, 2),
        'necessity_ratio': round((necessity_spending / total_spending * 100) if total_spending > 0 else 0, 2)
    }

def generate_merged_data(transaction_df, num_records=500):
    user_transactions = transaction_df.groupby('userid')
    unique_users = transaction_df['userid'].unique()[:int(num_records/6)]  # Divide by 6 as each user will have 6 records
    
    end_date = datetime.now()
    merged_data = []
    
    for user_id in unique_users:
        # Generate base profile for user that stays consistent
        base_profile = {
            'years_of_employment': random.randint(0, 20),
            'permanent_employment': random.choice(['yes', 'no']),
            'type_of_gig': random.choice(['high_value', 'low_value']),
            'gross_income': round(random.uniform(3000, 15000), 2),
            'social_media_activeness_score': round(random.uniform(1, 5), 2),
        }
        
        # Generate 6 months of records
        for month in range(6):
            record_date = end_date - timedelta(days=30 * month)
            month_start = record_date - timedelta(days=30)
            
            # Get transactions for this month
            month_transactions = transaction_df[
                (transaction_df['userid'] == user_id) & 
                (transaction_df['timestamp'] >= month_start) & 
                (transaction_df['timestamp'] <= record_date)
            ]
            
            metrics = calculate_monthly_metrics(month_transactions)
            
            record = {
                'userID': user_id,
                'Cancellation_rate': round(random.uniform(0, 5), 2),
                'ratings': round(random.uniform(3.5, 5), 2),
                'responsiveness_to_task': round(random.uniform(3, 5), 2),
                'Min_Max_Diff_Past_6_months': round(random.uniform(0, 1), 2),
                'ratings_influx': round(random.uniform(3, 5), 2),
                'type_of_gig': base_profile['type_of_gig'],
                'social_media_activeness_score': base_profile['social_media_activeness_score'],
                
                'Permanent_Employment': base_profile['permanent_employment'],
                'Years_of_Employment': base_profile['years_of_employment'],
                'fluctuation_rate': round(random.uniform(1, 10), 2),
                'gross_income': base_profile['gross_income'],
                'net_income': round(base_profile['gross_income'] * 0.8, 2),
                
                'Impulsive_purchase_rate': metrics['impulsive_purchase_rate'],
                'Recurring_expense_consistency': round(random.uniform(60, 95), 2),
                'Expense_to_Income_Ratio': round((metrics['total_spending'] / base_profile['gross_income'] * 100), 2),
                'Regular_saving': random.choice([True, False]),
                'regular_savings_amount': round(random.uniform(100, 1000), 2),
                'Emergency_fund_availability': random.choice([True, False]),
                'Emergency_fund_amount': round(random.uniform(1000, 10000), 2),
                'consistent_spending': random.choice([True, False]),
                'spending_amount': metrics['total_spending'],
                'portfolio_diversification_risk': round(random.uniform(1, 5), 2),
                'Awareness_of_utilisation_of_PFM': random.randint(1, 5),
                'timestamp': record_date
            }
            
            merged_data.append(record)
    
    return pd.DataFrame(merged_data)

if __name__ == "__main__":
    # Generate transaction data first
    print("Generating transaction data...")
    transactions_df = generate_transaction_data(num_users=84, num_transactions=2000)  # 84 users * 6 months ≈ 500 records
    transactions_df.to_csv('transaction.csv', index=False)
    print(f"Generated {len(transactions_df)} transactions")
    
    # Generate merged data based on transactions
    print("Generating merged data...")
    merged_df = generate_merged_data(transactions_df, num_records=500)
    merged_df.to_csv('merged.csv', index=False)
    print(f"Generated {len(merged_df)} merged records")