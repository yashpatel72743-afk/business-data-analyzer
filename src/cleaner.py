import pandas as pd

class DataCleaner:
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        
        df = df.copy()
        
        # Row remove krva
        df = df.dropna(how="all")
        
        # duplicate rows remove krva
        df = df.drop_duplicates()
        
        # column names srkha krva
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ","_")
        )
        
        # text columns cleam krva
        for column in df.select_dtypes(include="object").columns:
            df[column] = df[column].astype(str).str.strip()
            
            
        if "data" in df.columns:
            df["data"] = pd.to_datetime(
                df["data"],
                errors="coerce"
            )

        numberic_columns = [
            "sales",
            "quantity",
            "profit"
        ]
        
        for column in numberic_columns:
            if column in df.columns:
                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce"
                )
                        
        required_columns = [
            "sales",
            "quantity",
            "profit"
        ]
        
        existing_columns = [
            col for col in required_columns
            if col in df.columns
        ]
        
        df = df.dropna(subset=existing_columns)
        
        return df