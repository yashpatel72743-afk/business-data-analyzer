import pandas as pd

class BusinessAnalyzer:
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        
    def total_sales(self):
        return self.df["sales"].sum()
    
    def total_profit(self):
        return self.df["profit"].sum()
    
    def total_quantity(self):
        return self.df["quantity"].sum()
    
    def average_sales(self):
        return self.df["sales"].mean()
    
    def profit_margin(self):
        
        total_sales = self.total_sales()
        
        if total_sales == 0:
            return 0 
        
        return (
            self.total_profit()
            / total_sales
        ) * 100
        
    def best_product(self):
        
        product_sales = (
            self.df
            .groupby("product")["sales"]
            .sum()
        )
        
        return product_sales.idxmax()
    
    def best_region(self):
        
        region_sales = (
            self.df
            .groupby("region")["sales"]
            .sum()
        )
        
        return region_sales.idxmax()
    
    def product_summary(self):
        
        return (
            self.df
            .groupby("product")
            .agg(
                sales=("sales", "sum"),
                quantity=("quantity","sum"),
                profit=("profit", "sum")
            )
            .sort_values(
                "sales",
                ascending=False
            )
        )
        
    def region_summary(self):
        
        return(
            self.df
            .groupby("region")
            .agg(
                sales=("sales", "sum"),
                profit=("profit", "sum")
            )
            .sort_values(
                "sales",
                ascending=False
            )
        )
    