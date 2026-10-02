from pathlib import Path
import sys

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse

import numpy as np


# =========================================================
# PROJECT PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"

sys.path.insert(0, str(SRC_DIR))


# =========================================================
# EXISTING PROJECT FILES
# =========================================================

from loader import DataLoader
from cleaner import DataCleaner
from analyzer import BusinessAnalyzer
from report import ManagementReport


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="Business Data Analyzer API",
    description="API for Business Data Analysis",
    version="1.0.0"
)


# =========================================================
# FILE PATHS
# =========================================================

SALES_FILE = BASE_DIR / "data" / "sales.csv"
CLEANED_FILE = BASE_DIR / "data" / "cleaned_sales.csv"
REPORT_FILE = BASE_DIR / "reports" / "management_report.txt"


# =========================================================
# NUMPY → PYTHON CONVERTER
# =========================================================

def convert_to_python(value):

    # NumPy integer
    if isinstance(value, np.integer):
        return int(value)

    # NumPy float
    if isinstance(value, np.floating):
        return float(value)

    # NumPy boolean
    if isinstance(value, np.bool_):
        return bool(value)

    # NumPy array
    if isinstance(value, np.ndarray):
        return [
            convert_to_python(item)
            for item in value.tolist()
        ]

    # Dictionary
    if isinstance(value, dict):
        return {
            str(key): convert_to_python(val)
            for key, val in value.items()
        }

    # List
    if isinstance(value, list):
        return [
            convert_to_python(item)
            for item in value
        ]

    # Tuple
    if isinstance(value, tuple):
        return [
            convert_to_python(item)
            for item in value
        ]

    # Normal Python value
    return value


# =========================================================
# PROCESS BUSINESS DATA
# =========================================================

def process_business_data():

    # Load data
    loader = DataLoader()

    df = loader.load(
        str(SALES_FILE)
    )

    # Clean data
    cleaner = DataCleaner()

    cleaned_df = cleaner.clean(df)

    # Save cleaned data
    cleaned_df.to_csv(
        CLEANED_FILE,
        index=False
    )

    # Analyze data
    analyzer = BusinessAnalyzer(
        cleaned_df
    )

    # Generate report
    report_generator = ManagementReport()

    report_text = report_generator.generate(
        analyzer,
        str(REPORT_FILE)
    )

    return (
        cleaned_df,
        analyzer,
        report_text
    )


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "Business Data Analyzer API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "Business Data Analyzer API"
    }


# =========================================================
# GET SALES
# =========================================================

@app.get("/sales")
def get_sales():

    try:

        loader = DataLoader()

        df = loader.load(
            str(SALES_FILE)
        )

        df = df.where(
            df.notna(),
            None
        )

        data = df.to_dict(
            orient="records"
        )

        return convert_to_python({
            "count": len(data),
            "data": data
        })

    except FileNotFoundError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# =========================================================
# ANALYZE
# =========================================================

@app.post("/analyze")
def analyze_business_data():

    try:

        cleaned_df, analyzer, report_text = (
            process_business_data()
        )

        response = {

            "message":
                "Business data analyzed successfully",

            "records_processed":
                len(cleaned_df),

            "summary": {

                "total_sales":
                    analyzer.total_sales(),

                "total_profit":
                    analyzer.total_profit(),

                "total_quantity":
                    analyzer.total_quantity(),

                "average_sales":
                    analyzer.average_sales(),

                "profit_margin":
                    analyzer.profit_margin(),

                "best_product":
                    analyzer.best_product(),

                "best_region":
                    analyzer.best_region()
            }
        }

        # Convert all NumPy values
        return convert_to_python(response)

    except FileNotFoundError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# =========================================================
# CLEANED SALES
# =========================================================

@app.get("/sales/cleaned")
def get_cleaned_sales():

    try:

        if not CLEANED_FILE.exists():

            process_business_data()

        loader = DataLoader()

        df = loader.load(
            str(CLEANED_FILE)
        )

        df = df.where(
            df.notna(),
            None
        )

        data = df.to_dict(
            orient="records"
        )

        return convert_to_python({
            "count": len(data),
            "data": data
        })

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# =========================================================
# SUMMARY
# =========================================================

@app.get("/summary")
def get_summary():

    try:

        cleaned_df, analyzer, report_text = (
            process_business_data()
        )

        response = {

            "total_sales":
                analyzer.total_sales(),

            "total_profit":
                analyzer.total_profit(),

            "total_quantity":
                analyzer.total_quantity(),

            "average_sales":
                analyzer.average_sales(),

            "profit_margin":
                analyzer.profit_margin(),

            "best_product":
                analyzer.best_product(),

            "best_region":
                analyzer.best_region()
        }

        return convert_to_python(response)

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# =========================================================
# PRODUCT SUMMARY
# =========================================================

@app.get("/summary/products")
def get_product_summary():

    try:

        cleaned_df, analyzer, report_text = (
            process_business_data()
        )

        product_summary = (
            analyzer.product_summary()
        )

        product_summary = (
            product_summary.reset_index()
        )

        product_summary = product_summary.where(
            product_summary.notna(),
            None
        )

        data = product_summary.to_dict(
            orient="records"
        )

        return convert_to_python({
            "data": data
        })

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# =========================================================
# REGION SUMMARY
# =========================================================

@app.get("/summary/regions")
def get_region_summary():

    try:

        cleaned_df, analyzer, report_text = (
            process_business_data()
        )

        region_summary = (
            analyzer.region_summary()
        )

        region_summary = (
            region_summary.reset_index()
        )

        region_summary = region_summary.where(
            region_summary.notna(),
            None
        )

        data = region_summary.to_dict(
            orient="records"
        )

        return convert_to_python({
            "data": data
        })

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# =========================================================
# GENERATE REPORT
# =========================================================

@app.post("/generate-report")
def generate_report():

    try:

        cleaned_df, analyzer, report_text = (
            process_business_data()
        )

        response = {

            "message":
                "Management report generated successfully",

            "report_file":
                str(REPORT_FILE),

            "summary": {

                "total_sales":
                    analyzer.total_sales(),

                "total_profit":
                    analyzer.total_profit(),

                "total_quantity":
                    analyzer.total_quantity(),

                "average_sales":
                    analyzer.average_sales(),

                "profit_margin":
                    analyzer.profit_margin(),

                "best_product":
                    analyzer.best_product(),

                "best_region":
                    analyzer.best_region()
            }
        }

        return convert_to_python(response)

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# =========================================================
# GET REPORT
# =========================================================

@app.get(
    "/report",
    response_class=PlainTextResponse
)
def get_report():

    try:

        if not REPORT_FILE.exists():

            process_business_data()

        with open(
            REPORT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            report = file.read()

        return report

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )