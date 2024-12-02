import pandas as pd
import numpy as np
from thefuzz import fuzz
from datetime import datetime
import argparse
import sys
from tqdm import tqdm
from normalize_company import normalize_company_with_fuzzy, build_company_groups, should_exact_match
from total_flows import get_total_flows
from flow_diagram import generate_flow_diagram
from html_template import HTMLTemplate

def group_similar_companies(companies):
    groups = {}
    processed = set()
    
    for name in tqdm(companies, desc="Grouping similar companies"):
        if name in processed:
            continue
            
        if should_exact_match(name):
            groups[name] = [name]
            processed.add(name)
            continue
            
        group = [name]
        processed.add(name)
        
        for other in companies:
            if other not in processed and not should_exact_match(other) and fuzz.ratio(name, other) > 85:
                group.append(other)
                processed.add(other)
                
        groups[name] = group
    
    return groups

def analyze_transactions(df, output_format='text'):
    print("Starting transaction analysis...")
    
    # Clean column names
    df.columns = df.columns.str.strip()
    
    # Convert amount to numeric if not already
    df['Amount'] = pd.to_numeric(df['Amount'])
    
    # Convert date to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Normalize company names
    tqdm.pandas(desc="Normalizing company names")
    company_groups = build_company_groups(df['Description'].tolist())
    df['Normalized_Description'] = df['Description'].progress_apply(lambda x: normalize_company_with_fuzzy(x, company_groups))
    
    # Group similar company names, preserving exact matches for transfers
    unique_companies = df['Normalized_Description'].unique()
    company_groups = group_similar_companies(unique_companies)
    
    print("Creating company mappings...")
    company_mapping = {}
    for main_name, variations in company_groups.items():
        for variation in variations:
            if should_exact_match(variation):
                company_mapping[variation] = variation
            else:
                company_mapping[variation] = main_name
    
    df['Company'] = df['Normalized_Description'].map(company_mapping)
    
    print("Calculating final metrics...")
    months = (df['Date'].max() - df['Date'].min()).days / 30.44
    years = months / 12
    
    spending = df.groupby('Company').agg({
        'Amount': ['sum', 'count']
    }).reset_index()
    
    spending.columns = ['Company', 'Total_Amount', 'Transaction_Count']
    spending['Total_Amount'] = abs(spending['Total_Amount'])
    spending['Monthly_Average'] = spending['Total_Amount'] / months
    spending['Yearly_Average'] = spending['Total_Amount'] / years
    
    spending = spending.sort_values('Total_Amount', ascending=False).head(40)
    
    print("Analysis complete!")
    
    if output_format == 'html':
        template = HTMLTemplate()
        
        # Format the spending data for the table
        headers = ['Company', 'Total Amount', 'Monthly Average', 'Yearly Average', 'Transaction Count']
        rows = []
        for _, row in spending.iterrows():
            rows.append([
                row['Company'],
                f'${row["Total_Amount"]:,.2f}',
                f'${row["Monthly_Average"]:,.2f}',
                f'${row["Yearly_Average"]:,.2f}',
                str(row["Transaction_Count"])
            ])
        
        # Create the spending table section
        spending_table = template.create_card(
            title="Top 40 Companies by Transaction Volume",
            content=template.create_table(headers, rows)
        )
        
        # Get the flows analysis
        flows_section = get_total_flows(df, output_format)
        
        # Get the flow diagram
        flow_diagram = generate_flow_diagram(df, output_format)
        
        # Combine all sections
        content = f"""
            <h1 class="text-2xl font-semibold text-center mb-6">Transaction Analysis</h1>
            {spending_table}
            {flows_section}
            {flow_diagram}
        """
        
        return template.render(content)
    else:
        return spending.to_string(float_format=lambda x: '${:,.2f}'.format(x) if isinstance(x, float) else x)

def main():
    parser = argparse.ArgumentParser(description='Analyze transaction data')
    parser.add_argument('file', help='CSV file containing transaction data')
    parser.add_argument('--format', choices=['text', 'html'], default='text',
                      help='Output format (default: text)')
    parser.add_argument('--output', help='Output file (optional)')
    
    args = parser.parse_args()
    
    print(f"Reading data from {args.file}...")
    df = pd.read_csv(args.file)
    print("Columns found:", df.columns.tolist())
    
    result = analyze_transactions(df, args.format)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(result)
        print(f"Results written to {args.output}")
    else:
        print(result)

if __name__ == "__main__":
    main()