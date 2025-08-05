#!/usr/bin/env python3
"""
PDF Generation Script for Final Report
Converts FINAL_REPORT.md to PDF format for submission
"""

import markdown
import pdfkit
import os
from datetime import datetime

def generate_pdf():
    """Generate PDF from FINAL_REPORT.md"""
    
    print("🔄 Generating PDF from FINAL_REPORT.md...")
    
    # Read the markdown file
    with open('FINAL_REPORT.md', 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_content, extensions=['tables', 'fenced_code'])
    
    # Add CSS styling for better PDF appearance
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Brent Oil Price Change Point Analysis - Final Report</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                line-height: 1.6;
                margin: 40px;
                color: #333;
            }}
            h1, h2, h3 {{
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
            }}
            h1 {{
                font-size: 28px;
                text-align: center;
                color: #2c3e50;
            }}
            h2 {{
                font-size: 22px;
                margin-top: 30px;
            }}
            h3 {{
                font-size: 18px;
                margin-top: 25px;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            th {{
                background-color: #3498db;
                color: white;
                font-weight: bold;
            }}
            tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
            code {{
                background-color: #f4f4f4;
                padding: 2px 4px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }}
            pre {{
                background-color: #f4f4f4;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
            }}
            img {{
                max-width: 100%;
                height: auto;
                display: block;
                margin: 20px auto;
                border: 1px solid #ddd;
            }}
            .highlight {{
                background-color: #fff3cd;
                padding: 15px;
                border-left: 4px solid #ffc107;
                margin: 20px 0;
            }}
            .footer {{
                text-align: center;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                color: #666;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        {html_content}
        <div class="footer">
            <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            <p>Brent Oil Price Change Point Analysis - Final Report</p>
            <p>Birhan Energies Data Science Team</p>
        </div>
    </body>
    </html>
    """
    
    # Write HTML to temporary file
    with open('temp_report.html', 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    try:
        # Convert HTML to PDF using wkhtmltopdf
        pdfkit.from_file('temp_report.html', 'FINAL_REPORT.pdf', 
                        options={
                            'page-size': 'A4',
                            'margin-top': '0.75in',
                            'margin-right': '0.75in',
                            'margin-bottom': '0.75in',
                            'margin-left': '0.75in',
                            'encoding': "UTF-8",
                            'no-outline': None
                        })
        
        print("✅ PDF generated successfully: FINAL_REPORT.pdf")
        
        # Clean up temporary file
        os.remove('temp_report.html')
        
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        print("📝 Alternative: Use online markdown to PDF converters or browser print function")
        
        # Keep HTML file as backup
        print("📄 HTML version saved as: temp_report.html")
        print("💡 You can open this in a browser and use 'Print to PDF'")

if __name__ == "__main__":
    generate_pdf() 