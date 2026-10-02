from pathlib import Path


class ManagementReport:
    
    def generate(self, analyzer, output_file):
        
        report = f"""
        
========================================
        BUSINESS MANAGEMENT REPORT
========================================

KEY PERFORMANCE INDICATORS
----------------------------------------
    
Total Sales     : ₹{analyzer.total_sales():,.2f}

Total Profit    : ₹{analyzer.total_profit():,.2f}

Total Quantity  : {analyzer.total_quantity():,.0f}

Average Sale    : ₹{analyzer.average_sales():,.2f}

Profit Margin   : {analyzer.profit_margin():,.2f}%


BUSINESS HIGHLIGHTS
----------------------------------------

Best Product  :{analyzer.best_product()}

Best Region   :{analyzer.best_region()}


PRODUCT PERFORMANCE
----------------------------------------

{analyzer.product_summary().to_string()}


REGION PERFORMANCE
----------------------------------------

{analyzer.region_summary().to_string()}

========================================
              END OF REPORT
========================================
"""

        Path(output_file).parent.mkdir(
            parents=True,
            exist_ok=True
        )
        
        with open(
            output_file,
            "w",
            encoding="utf -8"
        ) as file:
            
            file.write(report)
            
        return report 