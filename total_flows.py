from datetime import datetime, timedelta
import pandas as pd
from html_template import HTMLTemplate

def get_total_flows(df, output_format='text'):
    """Calculate and display total money flows with monthly and yearly averages."""
    months = (df['Date'].max() - df['Date'].min()).days / 30.44
    years = months / 12
    
    deposits = df[df['Amount'] > 0]['Amount'].sum()
    withdrawals = abs(df[df['Amount'] < 0]['Amount'].sum())
    net = deposits - withdrawals
    
    if output_format == 'html':
        template = HTMLTemplate()
        
        # Format rows with proper currency formatting
        rows = [
            ['Deposits', f'${deposits:,.2f}', f'${deposits/months:,.2f}', f'${deposits/years:,.2f}'],
            ['Withdrawals', f'${withdrawals:,.2f}', f'${withdrawals/months:,.2f}', f'${withdrawals/years:,.2f}'],
            ['Net Flow', f'${net:,.2f}', f'${net/months:,.2f}', f'${net/years:,.2f}']
        ]
        
        headers = ['Type', 'Total', 'Monthly Average', 'Yearly Average']
        
        # Create content with proper spacing and typography
        header = '<h2 class="text-xl font-semibold mb-4">Total Money Flows</h2>'
        table = template.create_table(headers, rows)
        
        content = f"""
            <div class="card">
                {header}
                <div class="overflow-x-auto">
                    {table}
                </div>
            </div>
        """
        
        return content
    else:
        # Text output remains unchanged
        print("\nTotal Flows:")
        print(f"                   Total      Monthly Avg    Yearly Avg")
        print(f"Deposits:     ${deposits:,.2f}   ${deposits/months:,.2f}   ${deposits/years:,.2f}")
        print(f"Withdrawals:  ${withdrawals:,.2f}   ${withdrawals/months:,.2f}   ${withdrawals/years:,.2f}")
        print(f"Net Flow:     ${net:,.2f}   ${net/months:,.2f}   ${net/years:,.2f}")

def create_test_data(days=30):
    """Create a test DataFrame spanning the specified number of days."""
    dates = [datetime.now() - timedelta(days=x) for x in range(days)]
    
    data = {
        'Date': dates,
        'Time': ['12:00:00'] * days,
        'Amount': [100, -50, 75, -25] * (days // 4),  # Mix of deposits and withdrawals
        'Type': ['Deposit', 'Withdrawal'] * (days // 2),
        'Description': ['Test transaction'] * days
    }
    
    return pd.DataFrame(data)

def test_total_flows():
    """Run tests for the total_flows functionality."""
    print("\nRunning tests...")
    
    # Test 1: Basic calculation test
    print("\nTest 1: Basic calculation test")
    df = pd.DataFrame({
        'Date': [datetime(2024, 1, 1), datetime(2024, 1, 31)],
        'Amount': [100, -50]
    })
    get_total_flows(df)
    
    # Test 2: Zero sums test
    print("\nTest 2: Zero sums test")
    df = pd.DataFrame({
        'Date': [datetime(2024, 1, 1), datetime(2024, 1, 31)],
        'Amount': [100, -100]
    })
    get_total_flows(df)
    
    # Test 3: HTML output test
    print("\nTest 3: HTML output test")
    df = create_test_data(30)
    html_output = get_total_flows(df, 'html')
    print("HTML output length:", len(html_output))
    print("HTML output contains table:", 'table' in html_output)
    
    # Test 4: Longer period test
    print("\nTest 4: Three-month period test")
    df = create_test_data(90)
    get_total_flows(df)

if __name__ == "__main__":
    test_total_flows()
    print("\nAll tests completed!")