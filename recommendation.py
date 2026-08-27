import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

# Load the datasets
customers_df = pd.read_csv('customers.csv')
plans_df = pd.read_csv('plans.csv')

# Display basic information
print("Customer Data Shape:", customers_df.shape)
print("Plan Data Shape:", plans_df.shape)
print("\nCustomer Data Sample:")
print(customers_df.head())
print("\nPlan Data:")
print(plans_df)

def calculate_total_cost(customer_usage, plan_details):
    """
    Calculate the total monthly cost for a customer given a specific plan.
    
    Parameters:
    customer_usage: dict with keys: call_minutes, sms_count, data_gb, roaming_mins
    plan_details: dict with plan information
    
    Returns:
    total_cost: float
    cost_breakdown: dict with detailed cost breakdown
    """
    
    # Base monthly rental
    base_cost = plan_details['monthly_rental']
    
    # Calculate excess usage
    excess_minutes = max(0, customer_usage['call_minutes'] - plan_details['free_call_mins'])
    excess_sms = max(0, customer_usage['sms_count'] - plan_details['free_sms'])
    excess_data = max(0, customer_usage['data_gb'] - plan_details['free_data_gb'])
    
    # Calculate additional costs
    call_cost = excess_minutes * plan_details['cost_per_min']
    sms_cost = excess_sms * plan_details['cost_per_sms']
    data_cost = excess_data * plan_details['cost_per_gb']
    
    # Roaming is always charged (no free roaming in these plans)
    roaming_cost = customer_usage['roaming_mins'] * plan_details['cost_per_min']
    
    total_cost = base_cost + call_cost + sms_cost + data_cost + roaming_cost
    
    cost_breakdown = {
        'base_cost': base_cost,
        'call_cost': call_cost,
        'sms_cost': sms_cost,
        'data_cost': data_cost,
        'roaming_cost': roaming_cost,
        'total_cost': total_cost,
        'excess_minutes': excess_minutes,
        'excess_sms': excess_sms,
        'excess_data': excess_data
    }
    
    return total_cost, cost_breakdown

def get_top_3_recommendations(customer_data, all_plans):
    """
    Get top 3 plan recommendations for a customer based on total cost.
    
    Parameters:
    customer_data: pandas Series with customer information
    all_plans: pandas DataFrame with all available plans
    
    Returns:
    recommendations: list of top 3 cheapest plans with costs
    """
    
    customer_usage = {
        'call_minutes': customer_data['call_minutes'],
        'sms_count': customer_data['sms_count'],
        'data_gb': customer_data['data_gb'],
        'roaming_mins': customer_data['roaming_mins']
    }
    
    plan_costs = []
    
    # Calculate cost for each plan
    for _, plan in all_plans.iterrows():
        plan_details = plan.to_dict()
        total_cost, breakdown = calculate_total_cost(customer_usage, plan_details)
        
        plan_costs.append({
            'plan_id': plan['plan_id'],
            'total_cost': total_cost,
            'cost_breakdown': breakdown
        })
    
    # Sort by total cost (ascending) and return top 3
    plan_costs.sort(key=lambda x: x['total_cost'])
    return plan_costs[:3]

def generate_all_recommendations(customers_df, plans_df):
    """
    Generate top 3 recommendations for all customers.
    
    Returns:
    recommendations_df: DataFrame with customer recommendations
    """
    
    all_recommendations = []
    
    for _, customer in customers_df.iterrows():
        customer_id = customer['customer_id']
        current_plan = customer['current_plan']
        
        # Get top 3 recommendations
        top_3 = get_top_3_recommendations(customer, plans_df)
        
        # Calculate current plan cost for comparison
        current_plan_data = plans_df[plans_df['plan_id'] == current_plan].iloc[0]
        customer_usage = {
            'call_minutes': customer['call_minutes'],
            'sms_count': customer['sms_count'],
            'data_gb': customer['data_gb'],
            'roaming_mins': customer['roaming_mins']
        }
        current_cost, _ = calculate_total_cost(customer_usage, current_plan_data.to_dict())
        
        # Create recommendation records
        for rank, rec in enumerate(top_3, 1):
            savings = current_cost - rec['total_cost']
            savings_percentage = (savings / current_cost) * 100 if current_cost > 0 else 0
            
            all_recommendations.append({
                'customer_id': customer_id,
                'current_plan': current_plan,
                'current_plan_cost': current_cost,
                'rank': rank,
                'recommended_plan': rec['plan_id'],
                'recommended_cost': rec['total_cost'],
                'potential_savings': savings,
                'savings_percentage': savings_percentage,
                'call_minutes': customer['call_minutes'],
                'sms_count': customer['sms_count'],
                'data_gb': customer['data_gb'],
                'roaming_mins': customer['roaming_mins']
            })
    
    return pd.DataFrame(all_recommendations)

def segment_customers(customers_df):
    """
    Segment customers based on their usage patterns using K-means clustering.
    """
    
    # Create usage features for clustering
    usage_features = ['call_minutes', 'sms_count', 'data_gb', 'roaming_mins']
    X = customers_df[usage_features].copy()
    
    # Normalize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Perform K-means clustering
    kmeans = KMeans(n_clusters=5, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    
    customers_df_copy = customers_df.copy()
    customers_df_copy['cluster'] = clusters
    
    return customers_df_copy, kmeans

print("Generating recommendations for all customers...")

# Generate recommendations
recommendations_df = generate_all_recommendations(customers_df, plans_df)

# Perform customer segmentation
customers_with_clusters, kmeans_model = segment_customers(customers_df)

# Define segment names
segment_names = {
    0: "Moderate Users",
    1: "Heavy Voice Users", 
    2: "Low Usage",
    3: "Data-Heavy Users",
    4: "Balanced High Users"
}

# Create final export with all details
final_recommendations = []

for _, customer in customers_df.iterrows():
    customer_id = customer['customer_id']
    cluster = customers_with_clusters[customers_with_clusters['customer_id'] == customer_id]['cluster'].iloc[0]
    segment_name = segment_names[cluster]
    
    customer_recommendations = recommendations_df[recommendations_df['customer_id'] == customer_id]
    
    for _, rec in customer_recommendations.iterrows():
        final_recommendations.append({
            'customer_id': rec['customer_id'],
            'customer_segment': segment_name,
            'current_plan': rec['current_plan'],
            'current_plan_cost': rec['current_plan_cost'],
            'call_minutes': rec['call_minutes'],
            'sms_count': rec['sms_count'],
            'data_gb': rec['data_gb'],
            'roaming_mins': rec['roaming_mins'],
            'recommendation_rank': rec['rank'],
            'recommended_plan': rec['recommended_plan'],
            'recommended_cost': rec['recommended_cost'],
            'potential_savings': rec['potential_savings'],
            'savings_percentage': rec['savings_percentage']
        })

final_df = pd.DataFrame(final_recommendations)

# Save results to CSV
final_df.to_csv('customer_plan_recommendations.csv', index=False)

print(f"Successfully generated recommendations for {len(customers_df)} customers")
print(f"Total recommendation records: {len(final_df)}")

# Analyze results
rank_1_recommendations = final_df[final_df['recommendation_rank'] == 1]

print("RESULTS SUMMARY:")
print(f"Customers who can save money: {(rank_1_recommendations['potential_savings'] > 0).sum()}")
print(f"Average potential savings: Rs.{rank_1_recommendations['potential_savings'].mean():.2f}")
print(f"Maximum potential savings: Rs.{rank_1_recommendations['potential_savings'].max():.2f}")
print(f"Average savings percentage: {rank_1_recommendations['savings_percentage'].mean():.2f}%")

# Most recommended plans
print("\nMost Recommended Plans:")
print(rank_1_recommendations['recommended_plan'].value_counts())

# Savings by customer segment
print("\nSavings by Customer Segment:")
segment_analysis = rank_1_recommendations.groupby('customer_segment').agg({
    'potential_savings': ['mean', 'max'],
    'savings_percentage': ['mean', 'max'],
    'customer_id': 'count'
}).round(2)
print(segment_analysis)

