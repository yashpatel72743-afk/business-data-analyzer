from loader import DataLoader
from cleaner import DataCleaner
from analyzer import BusinessAnalyzer
from report import ManagementReport

def main():

    file_path = "business-data-analyzer/data/sales.csv"

    # 1. Load
    loader = DataLoader()
    df = loader.load(file_path)
    

    print("Data loaded successfully!")

    # 2. Clean
    cleaner = DataCleaner()
    cleaned_df = cleaner.clean(df)

    print("Data cleaned successfully!")

    # 3. Save cleaned data
    cleaned_df.to_csv(
        "business-data-analyzer/data/cleaned_sales.csv",
        index=False
    )

    # 4. Analyze
    analyzer = BusinessAnalyzer(cleaned_df)

    # 5. Generate report
    report = ManagementReport()

    report.generate(
        analyzer,
        "business-data-analyzer/reports/management_report.txt"
    )

    print("Management report generated!")

    print("\n===== BUSINESS SUMMARY =====")

    print(
        "Total Sales:",
        analyzer.total_sales()
    )

    print(
        "Total Profit:",
        analyzer.total_profit()
    )

    print(
        "Best Product:",
        analyzer.best_product()
    )

    print(
        "Best Region:",
        analyzer.best_region()
    )


if __name__ == "__main__":
    main()