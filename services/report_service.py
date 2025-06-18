from typing import Dict, Any
import pandas as pd
from datetime import datetime
from pathlib import Path


class ReportService:
    """Service for generating reports"""

    def __init__(self, connection_service=None):
        self.connection_service = connection_service
        self.reports_dir = Path("exports/reports")
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def generate_table_report(self, table_name: str) -> Dict[str, Any]:
        """Generate report for table"""
        try:
            if not self.connection_service:
                raise ValueError("No database connection")

            # Get table data
            query = f"SELECT * FROM {table_name}"
            success, result = self.connection_service.execute_query(query)

            if not success:
                raise Exception(result)

            # Convert to DataFrame
            df = pd.DataFrame(result)

            # Generate stats
            stats = {
                "total_rows": len(df),
                "total_columns": len(df.columns),
                "null_counts": df.isnull().sum().to_dict(),
                "column_types": df.dtypes.to_dict(),
                "sample_rows": df.head(5).to_dict("records"),
            }

            # Create Excel report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.reports_dir / f"report_{table_name}_{timestamp}.xlsx"

            with pd.ExcelWriter(output_file) as writer:
                # Data sheet
                df.head(1000).to_excel(writer, sheet_name="Data", index=False)

                # Stats sheet
                stats_df = pd.DataFrame([stats])
                stats_df.to_excel(writer, sheet_name="Statistics", index=False)

            return {"success": True, "file_path": str(output_file), "statistics": stats}

        except Exception as e:
            return {"success": False, "error": str(e)}
