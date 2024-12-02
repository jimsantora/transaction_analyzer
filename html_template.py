from typing import List, Dict, Union, Optional

class HTMLTemplate:
    def __init__(self):
        self.css = self._load_css()
    
    def _load_css(self) -> str:
        """Load CSS file or return empty styles if not found."""
        try:
            with open('styles.css', 'r') as f:
                return f.read()
        except FileNotFoundError:
            return "/* CSS not found */"
    
    def render(self, content: str, title: str = "Transaction Analysis") -> str:
        """Render the complete HTML document."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <style>{self.css}</style>
        </head>
        <body>
            <div class="container">
                {content}
            </div>
        </body>
        </html>
        """
    
    def create_card(self, content: str, title: Optional[str] = None) -> str:
        """Create a card component with optional title."""
        header = f'<h2 class="text-xl font-semibold mb-4">{title}</h2>' if title else ""
        return f"""
        <div class="card">
            {header}
            {content}
        </div>
        """
    
    def create_table(self, headers: List[str], rows: List[List[str]]) -> str:
        """Create a formatted table."""
        header_html = "".join([f"<th>{header}</th>" for header in headers])
        rows_html = ""
        for row in rows:
            cells = "".join([f"<td>{cell}</td>" for cell in row])
            rows_html += f"<tr>{cells}</tr>"
        
        return f"""
        <table class="table">
            <thead>
                <tr>{header_html}</tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
        """
    
    def create_bar_chart(self, categories: List[Dict[str, Union[str, float, int]]]) -> str:
        """Create a bar chart visualization.
        
        Args:
            categories: List of dictionaries with keys:
                - name: str
                - amount: float
                - count: int
                - percentage: float
                - keywords: str (optional)
        """
        colors = ['violet', 'blue', 'cyan', 'emerald', 'lime', 'amber', 'red']
        charts_html = ""
        
        for idx, cat in enumerate(categories):
            color = colors[idx % len(colors)]
            charts_html += f"""
            <div class="category">
                <div class="category-header">
                    <span class="category-name">{cat['name']}</span>
                    <span class="category-amount">${cat['amount']:,.2f}</span>
                </div>
                <div class="bar-container">
                    <div class="bar bg-gradient-{color}" style="width: {cat['percentage']}%"></div>
                </div>
                <div class="text-sm text-secondary mb-1">{cat['count']} transactions</div>
                {f'<div class="tooltip">Keywords: {cat["keywords"]}</div>' if 'keywords' in cat else ''}
            </div>
            """
        
        return charts_html