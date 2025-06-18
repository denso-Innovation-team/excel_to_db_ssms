from typing import Dict, Any, List
import pandas as pd
from pathlib import Path
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ExportService:
    """Data export service"""

    def __init__(self):
        self.export_dir = Path("exports")
        self.export_dir.mkdir(exist_ok=True)

    def export_to_excel(self, data: List[Dict], filename: str) -> Dict[str, Any]:
        """Export data to Excel file"""
        try:
            df = pd.DataFrame(data)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{filename}_{timestamp}.xlsx"
            output_path = self.export_dir / filename

            with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
                # Write data
                df.to_excel(writer, sheet_name="Data", index=False)

                # Add summary sheet
                summary = pd.DataFrame(
                    [
                        {
                            "Total Rows": len(df),
                            "Total Columns": len(df.columns),
                            "Export Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "File Size": f"{output_path.stat().st_size / 1024:.1f} KB",
                        }
                    ]
                )
                summary.to_excel(writer, sheet_name="Summary", index=False)

            return {
                "success": True,
                "file_path": str(output_path),
                "row_count": len(df),
            }

        except Exception as e:
            logger.error(f"Export error: {e}")
            return {"success": False, "error": str(e)}

    def export_to_csv(self, data: List[Dict], filename: str) -> Dict[str, Any]:
        """Export data to CSV file"""
        try:
            df = pd.DataFrame(data)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{filename}_{timestamp}.csv"
            output_path = self.export_dir / filename

            df.to_csv(output_path, index=False, encoding="utf-8-sig")

            return {
                "success": True,
                "file_path": str(output_path),
                "row_count": len(df),
            }

        except Exception as e:
            logger.error(f"Export error: {e}")
            return {"success": False, "error": str(e)}
