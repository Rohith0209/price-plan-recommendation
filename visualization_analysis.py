# Complete Visualization Code for Customer Plan Recommendations

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')

# Set style for better-looking plots
plt.style.use('seaborn')
sns.set_palette("husl")

def load_and_prepare_data():
    """Load the recommendations CSV and prepare data for visualization"""
    try:
        df = pd.read_csv('customer_plan_recommendations.csv')
        print(f"Successfully loaded {len(df)} recommendation records")
        return df
    except FileNotFoundError:
        print("Error: customer_plan_recommendations.csv not found!")
        print("Please run the recommendation model first to generate this file.")
        return None

def create_comprehensive_visualizations(df):
    """Create multiple visualizations to analyze the recommendations"""
    
    # Filter for top recommendations only
    top_recommendations = df[df['recommendation_rank'] == 1].copy()
    
    # Create a figure with multiple subplots
    fig = plt.figure(figsize=(20, 15))
    
    # 1. Distribution of Recommended Plans
    plt.subplot(2, 3, 1)
    plan_counts = top_recommendations['recommended_plan'].value_counts()
    colors = plt.cm.Set3(np.linspace(0, 1, len(plan_counts)))
    bars = plt.bar(plan_counts.index, plan_counts.values, color=colors)
    plt.title('Distribution of Top Recommended Plans', fontsize=14, fontweight='bold')
    plt.xlabel('Plan ID')
    plt.ylabel('Number of Customers')
    plt.xticks(rotation=45)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(height)}', ha='center', va='bottom')
    
    # 2. Potential Savings Distribution
    plt.subplot(2, 3, 2)
    plt.hist(top_recommendations['potential_savings'], bins=30, alpha=0.7, color='green', edgecolor='black')
    plt.title('Distribution of Potential Monthly Savings', fontsize=14, fontweight='bold')
    plt.xlabel('Savings Amount (Rs.)')
    plt.ylabel('Number of Customers')
    plt.axvline(top_recommendations['potential_savings'].mean(), color='red', linestyle='--', 
                label=f'Average: Rs.{top_recommendations["potential_savings"].mean():.0f}')
    plt.legend()
    
    # 3. Savings by Customer Segment
    plt.subplot(2, 3, 3)
    segment_savings = top_recommendations.groupby('customer_segment')['potential_savings'].mean().sort_values(ascending=True)
    bars = plt.barh(segment_savings.index, segment_savings.values, color='skyblue')
    plt.title('Average Savings by Customer Segment', fontsize=14, fontweight='bold')
    plt.xlabel('Average Savings (Rs.)')
    
    # Add value labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(width + 20, bar.get_y() + bar.get_height()/2,
                f'Rs.{width:.0f}', ha='left', va='center')
    
    # 4. Current vs Recommended Cost Comparison
    plt.subplot(2, 3, 4)
    plt.scatter(top_recommendations['current_plan_cost'], top_recommendations['recommended_cost'], 
                alpha=0.6, c=top_recommendations['potential_savings'], cmap='RdYlGn', s=50)
    plt.plot([0, top_recommendations['current_plan_cost'].max()], [0, top_recommendations['current_plan_cost'].max()], 
             'r--', alpha=0.8, label='No Change Line')
    plt.title('Current vs Recommended Plan Costs', fontsize=14, fontweight='bold')
    plt.xlabel('Current Plan Cost (Rs.)')
    plt.ylabel('Recommended Plan Cost (Rs.)')
    plt.colorbar(label='Savings Amount (Rs.)')
    plt.legend()
    
    # 5. Savings Percentage Distribution
    plt.subplot(2, 3, 5)
    plt.hist(top_recommendations['savings_percentage'], bins=25, alpha=0.7, color='orange', edgecolor='black')
    plt.title('Distribution of Savings Percentage', fontsize=14, fontweight='bold')
    plt.xlabel('Savings Percentage (%)')
    plt.ylabel('Number of Customers')
    plt.axvline(top_recommendations['savings_percentage'].mean(), color='red', linestyle='--', 
                label=f'Average: {top_recommendations["savings_percentage"].mean():.1f}%')
    plt.legend()
    
    # 6. Plan Migration Matrix
    plt.subplot(2, 3, 6)
    migration_matrix = pd.crosstab(top_recommendations['current_plan'], top_recommendations['recommended_plan'])
    sns.heatmap(migration_matrix, annot=True, fmt='d', cmap='Blues', cbar_kws={'label': 'Number of Customers'})
    plt.title('Plan Migration Patterns', fontsize=14, fontweight='bold')
    plt.xlabel('Recommended Plan')
    plt.ylabel('Current Plan')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    plt.savefig('customer_recommendations_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_customer_segment_analysis(df):
    """Create detailed analysis by customer segments"""
    
    top_recommendations = df[df['recommendation_rank'] == 1].copy()
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Usage patterns by segment
    usage_cols = ['call_minutes', 'sms_count', 'data_gb', 'roaming_mins']
    segment_usage = top_recommendations.groupby('customer_segment')[usage_cols].mean()
    
    ax1 = axes[0, 0]
    segment_usage.plot(kind='bar', ax=ax1, width=0.8)
    ax1.set_title('Average Usage Patterns by Customer Segment', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Customer Segment')
    ax1.set_ylabel('Usage Amount')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax1.tick_params(axis='x', rotation=45)
    
    # 2. Recommended plans by segment
    ax2 = axes[0, 1]
    segment_plans = pd.crosstab(top_recommendations['customer_segment'], top_recommendations['recommended_plan'])
    segment_plans.plot(kind='bar', stacked=True, ax=ax2)
    ax2.set_title('Recommended Plans by Customer Segment', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Customer Segment')
    ax2.set_ylabel('Number of Customers')
    ax2.legend(title='Recommended Plan', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax2.tick_params(axis='x', rotation=45)
    
    # 3. Savings distribution by segment
    ax3 = axes[1, 0]
    top_recommendations.boxplot(column='potential_savings', by='customer_segment', ax=ax3)
    ax3.set_title('Savings Distribution by Customer Segment', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Customer Segment')
    ax3.set_ylabel('Potential Savings (Rs.)')
    plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)
    
    # 4. Cost reduction effectiveness
    ax4 = axes[1, 1]
    segment_stats = top_recommendations.groupby('customer_segment').agg({
        'potential_savings': 'mean',
        'savings_percentage': 'mean',
        'customer_id': 'count'
    }).round(2)
    
    x_pos = np.arange(len(segment_stats))
    bars1 = ax4.bar(x_pos - 0.2, segment_stats['potential_savings'], 0.4, label='Avg Savings (Rs.)', alpha=0.8)
    ax4_twin = ax4.twinx()
    bars2 = ax4_twin.bar(x_pos + 0.2, segment_stats['savings_percentage'], 0.4, label='Avg Savings (%)', alpha=0.8, color='orange')
    
    ax4.set_title('Cost Reduction Effectiveness by Segment', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Customer Segment')
    ax4.set_ylabel('Average Savings (Rs.)', color='blue')
    ax4_twin.set_ylabel('Average Savings (%)', color='orange')
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(segment_stats.index, rotation=45)
    
    # Add legends
    ax4.legend(loc='upper left')
    ax4_twin.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig('customer_segment_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def show_top_customers_with_savings(df):
    """Display top customers who can save the most money"""
    
    top_recommendations = df[df['recommendation_rank'] == 1].copy()
    top_savers = top_recommendations.nlargest(10, 'potential_savings')
    
    print("\n" + "="*80)
    print("TOP 10 CUSTOMERS WITH HIGHEST SAVINGS POTENTIAL")
    print("="*80)
    
    for idx, customer in top_savers.iterrows():
        print(f"\nCustomer ID: {customer['customer_id']}")
        print(f"Segment: {customer['customer_segment']}")
        print(f"Current Plan: {customer['current_plan']} (Rs.{customer['current_plan_cost']:.2f}/month)")
        print(f"Recommended Plan: {customer['recommended_plan']} (Rs.{customer['recommended_cost']:.2f}/month)")
        print(f"Monthly Savings: Rs.{customer['potential_savings']:.2f} ({customer['savings_percentage']:.1f}%)")
        print(f"Usage: {customer['call_minutes']} mins, {customer['sms_count']} SMS, {customer['data_gb']:.1f} GB, {customer['roaming_mins']} roaming mins")
        print("-" * 40)

def create_individual_customer_reports(df, customer_ids):
    """Create detailed reports for specific customers"""
    
    print("\n" + "="*80)
    print("DETAILED CUSTOMER RECOMMENDATION REPORTS")
    print("="*80)
    
    for customer_id in customer_ids:
        customer_recs = df[df['customer_id'] == customer_id].sort_values('recommendation_rank')
        
        if len(customer_recs) == 0:
            print(f"Customer {customer_id} not found!")
            continue
            
        customer = customer_recs.iloc[0]
        
        print(f"\n{'='*50}")
        print(f"CUSTOMER: {customer_id}")
        print(f"{'='*50}")
        print(f"Segment: {customer['customer_segment']}")
        print(f"Current Plan: {customer['current_plan']} (Rs.{customer['current_plan_cost']:.2f}/month)")
        
        print(f"\nUsage Profile:")
        print(f"  • Calls: {customer['call_minutes']} minutes/month")
        print(f"  • SMS: {customer['sms_count']} messages/month") 
        print(f"  • Data: {customer['data_gb']:.1f} GB/month")
        print(f"  • Roaming: {customer['roaming_mins']} minutes/month")
        
        print(f"\nRecommendations:")
        for _, rec in customer_recs.iterrows():
            rank = rec['recommendation_rank']
            savings = rec['potential_savings']
            savings_pct = rec['savings_percentage']
            
            print(f"  {rank}. {rec['recommended_plan']}: Rs.{rec['recommended_cost']:.2f}/month")
            if savings > 0:
                print(f"     → Save Rs.{savings:.2f}/month ({savings_pct:.1f}%)")
            elif savings == 0:
                print(f"     → Same cost (current optimal plan)")
            else:
                print(f"     → Costs Rs.{abs(savings):.2f} more/month")

def generate_summary_report(df):
    """Generate overall summary statistics"""
    
    top_recommendations = df[df['recommendation_rank'] == 1].copy()
    
    print("\n" + "="*80)
    print("COMPREHENSIVE ANALYSIS SUMMARY")
    print("="*80)
    
    total_customers = len(top_recommendations)
    customers_saving = len(top_recommendations[top_recommendations['potential_savings'] > 0])
    customers_same = len(top_recommendations[top_recommendations['potential_savings'] == 0])
    customers_more = len(top_recommendations[top_recommendations['potential_savings'] < 0])
    
    print(f"\nCustomer Analysis:")
    print(f"  • Total Customers Analyzed: {total_customers:,}")
    print(f"  • Customers Who Can Save: {customers_saving:,} ({customers_saving/total_customers*100:.1f}%)")
    print(f"  • Customers Already Optimal: {customers_same:,} ({customers_same/total_customers*100:.1f}%)")
    print(f"  • Customers Who Would Pay More: {customers_more:,} ({customers_more/total_customers*100:.1f}%)")
    
    print(f"\nSavings Potential:")
    print(f"  • Average Monthly Savings: Rs.{top_recommendations['potential_savings'].mean():.2f}")
    print(f"  • Maximum Monthly Savings: Rs.{top_recommendations['potential_savings'].max():.2f}")
    print(f"  • Total Monthly Savings (All Customers): Rs.{top_recommendations['potential_savings'].sum():,.2f}")
    print(f"  • Average Savings Percentage: {top_recommendations['savings_percentage'].mean():.1f}%")
    
    print(f"\nMost Popular Recommended Plans:")
    plan_popularity = top_recommendations['recommended_plan'].value_counts()
    for plan, count in plan_popularity.head().items():
        percentage = count/total_customers*100
        print(f"  • {plan}: {count:,} customers ({percentage:.1f}%)")
    
    print(f"\nSavings by Customer Segment:")
    segment_analysis = top_recommendations.groupby('customer_segment').agg({
        'potential_savings': 'mean',
        'savings_percentage': 'mean',
        'customer_id': 'count'
    }).round(2)
    
    for segment in segment_analysis.index:
        stats = segment_analysis.loc[segment]
        print(f"  • {segment}:")
        print(f"    - Average Savings: Rs.{stats['potential_savings']:.2f} ({stats['savings_percentage']:.1f}%)")
        print(f"    - Customer Count: {int(stats['customer_id']):,}")

# Main execution function
def main():
    """Main function to run all visualizations and analysis"""
    
    print("Loading customer recommendation data...")
    df = load_and_prepare_data()
    
    if df is None:
        return
    
    print(f"Loaded {len(df)} recommendation records for {len(df['customer_id'].unique())} customers")
    
    # Create all visualizations
    print("\nGenerating comprehensive visualizations...")
    create_comprehensive_visualizations(df)
    
    print("\nGenerating customer segment analysis...")
    create_customer_segment_analysis(df)
    
    # Show analysis results
    generate_summary_report(df)
    show_top_customers_with_savings(df)
    
    # Show detailed reports for sample customers
    sample_customers = ['C1', 'C49', 'C332', 'C437', 'C100']  # You can change these
    create_individual_customer_reports(df, sample_customers)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print("="*80)
    print("Generated files:")
    print("  • customer_recommendations_analysis.png - Main dashboard")
    print("  • customer_segment_analysis.png - Segment deep-dive")
    print("  • customer_plan_recommendations.csv - Raw data")

if __name__ == "__main__":
    main()