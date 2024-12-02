from html_template import HTMLTemplate
from categories import TRANSACTION_CATEGORIES
from categorize import categorize_transaction
import os

def generate_flow_diagram(df, output_format='html'):
    """Generate a modern HTML/CSS spending visualization with keyword tooltips."""
    # Add category column
    df['Category'] = df['Description'].apply(categorize_transaction)
    
    # Calculate total outflow by category
    category_flows = df[df['Amount'] < 0].groupby('Category').agg({
        'Amount': ['sum', 'count']
    }).reset_index()
    
    category_flows.columns = ['Category', 'Total_Amount', 'Transaction_Count']
    category_flows['Total_Amount'] = abs(category_flows['Total_Amount'])
    category_flows = category_flows.sort_values('Total_Amount', ascending=False)
    
    if output_format == 'html':
        template = HTMLTemplate()
        total_amount = category_flows['Total_Amount'].sum()
        max_amount = category_flows['Total_Amount'].max()
        
        # Format data for bar chart
        categories = []
        colors = ['violet', 'blue', 'cyan', 'emerald', 'lime', 'amber', 'red']
        
        for idx, row in category_flows.iterrows():
            color = colors[idx % len(colors)]
            keywords = TRANSACTION_CATEGORIES.get(row['Category'], ['Other'])
            categories.append({
                'name': row['Category'],
                'amount': row['Total_Amount'],
                'count': row['Transaction_Count'],
                'percentage': (row['Total_Amount'] / max_amount) * 100,
                'keywords': ', '.join(keywords)
            })
        
        # Generate visualization content
        header = f'<h1 class="text-2xl font-semibold text-center mb-4">Spending Analysis</h1>'
        total_spent = f'<div class="text-lg text-center text-secondary mb-8">Total Spending: ${total_amount:,.2f}</div>'
        bar_chart = template.create_bar_chart(categories)
        
        content = f"""
            {header}
            {total_spent}
            <div class="card">
                {bar_chart}
            </div>
        """
        
        return template.render(content)
    else:
        return category_flows.to_string()

if __name__ == "__main__":
    import pandas as pd
    # Test code can be added here