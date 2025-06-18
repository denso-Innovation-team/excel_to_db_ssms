"""
services/schema_service.py
Automatic Database Schema Management Service
"""

import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
import json
import re

logger = logging.getLogger(__name__)


class ColumnDefinition:
    """Column definition with type mapping"""

    def __init__(
        self,
        name: str,
        data_type: str,
        nullable: bool = True,
        default: Any = None,
        primary_key: bool = False,
    ):
        self.name = name
        self.data_type = data_type
        self.nullable = nullable
        self.default = default
        self.primary_key = primary_key

    def to_sql(self, db_type: str = "sqlite") -> str:
        """Generate SQL column definition"""
        sql_type = self._map_type_to_sql(self.data_type, db_type)

        parts = [f"[{self.name}]", sql_type]

        if self.primary_key:
            if db_type == "sqlite":
                parts.append("PRIMARY KEY AUTOINCREMENT")
            else:
                parts.append("IDENTITY(1,1) PRIMARY KEY")

        if not self.nullable and not self.primary_key:
            parts.append("NOT NULL")

        if self.default is not None:
            parts.append(f"DEFAULT {self._format_default(self.default, db_type)}")

        return " ".join(parts)

    def _map_type_to_sql(self, data_type: str, db_type: str) -> str:
        """Map generic types to SQL types"""
        type_mapping = {
            "sqlite": {
                "string": "TEXT",
                "integer": "INTEGER",
                "float": "REAL",
                "boolean": "BOOLEAN",
                "date": "TEXT",
                "datetime": "TEXT",
                "decimal": "REAL",
                "text": "TEXT",
            },
            "sqlserver": {
                "string": "NVARCHAR(255)",
                "integer": "INT",
                "float": "FLOAT",
                "boolean": "BIT",
                "date": "DATE",
                "datetime": "DATETIME2",
                "decimal": "DECIMAL(18,2)",
                "text": "NVARCHAR(MAX)",
            },
        }

        return type_mapping.get(db_type, type_mapping["sqlite"]).get(
            data_type.lower(), "TEXT" if db_type == "sqlite" else "NVARCHAR(255)"
        )

    def _format_default(self, value: Any, db_type: str) -> str:
        """Format default value for SQL"""
        if isinstance(value, str):
            return f"'{value}'"
        elif isinstance(value, bool):
            return "1" if value else "0"
        else:
            return str(value)


class TableSchema:
    """Complete table schema definition"""

    def __init__(self, name: str, columns: List[ColumnDefinition]):
        self.name = name
        self.columns = columns
        self.created_at = datetime.now()

    def add_column(self, column: ColumnDefinition):
        """Add column to schema"""
        self.columns.append(column)

    def get_column(self, name: str) -> Optional[ColumnDefinition]:
        """Get column by name"""
        for col in self.columns:
            if col.name == name:
                return col
        return None

    def to_create_sql(self, db_type: str = "sqlite") -> str:
        """Generate CREATE TABLE SQL"""
        column_defs = [col.to_sql(db_type) for col in self.columns]

        return f"""CREATE TABLE [{self.name}] (
    {',\\n    '.join(column_defs)}
)"""

    def to_alter_sql(
        self, existing_columns: List[str], db_type: str = "sqlite"
    ) -> List[str]:
        """Generate ALTER TABLE statements for new columns"""
        statements = []

        for col in self.columns:
            if col.name not in existing_columns:
                if db_type == "sqlite":
                    statements.append(
                        f"ALTER TABLE [{self.name}] ADD COLUMN {col.to_sql(db_type)}"
                    )
                else:
                    statements.append(
                        f"ALTER TABLE [{self.name}] ADD {col.to_sql(db_type)}"
                    )

        return statements


class SchemaAnalyzer:
    """Analyze data to suggest schema"""

    @staticmethod
    def analyze_excel_data(
        sample_data: List[Dict[str, Any]], table_name: str
    ) -> TableSchema:
        """Analyze Excel data and suggest optimal schema"""
        if not sample_data:
            return TableSchema(table_name, [])

        # Analyze each column
        columns = []

        # Add auto-increment ID column
        columns.append(
            ColumnDefinition("id", "integer", nullable=False, primary_key=True)
        )

        # Analyze data columns
        for col_name in sample_data[0].keys():
            clean_name = SchemaAnalyzer._clean_column_name(col_name)
            data_type = SchemaAnalyzer._detect_column_type(sample_data, col_name)
            nullable = SchemaAnalyzer._detect_nullable(sample_data, col_name)

            columns.append(ColumnDefinition(clean_name, data_type, nullable))

        return TableSchema(table_name, columns)

    @staticmethod
    def _clean_column_name(name: str) -> str:
        """Clean column name for database compatibility"""
        clean = re.sub(r"[^\w\s]", "_", str(name).strip())
        clean = re.sub(r"\s+", "_", clean)
        clean = re.sub(r"_+", "_", clean)
        clean = clean.strip("_").lower()

        if not clean or clean.isdigit():
            clean = "column"

        # Handle reserved words
        reserved = {
            "index",
            "order",
            "group",
            "select",
            "from",
            "where",
            "table",
            "user",
        }
        if clean in reserved:
            clean = f"{clean}_col"

        return clean

    @staticmethod
    def _detect_column_type(data: List[Dict], column: str) -> str:
        """Detect optimal column type from sample data"""
        values = [row.get(column) for row in data if row.get(column) is not None]

        if not values:
            return "string"

        # Type detection logic
        all_integers = True
        all_floats = True
        all_booleans = True
        all_dates = True

        for value in values:
            str_val = str(value).strip().lower()

            # Check integer
            try:
                int(float(str_val))
                if "." in str_val:
                    all_integers = False
            except (ValueError, TypeError):
                all_integers = False
                all_floats = False

            # Check float
            try:
                float(str_val)
            except (ValueError, TypeError):
                all_floats = False

            # Check boolean
            if str_val not in ["true", "false", "1", "0", "yes", "no", "y", "n"]:
                all_booleans = False

            # Check date
            if not SchemaAnalyzer._looks_like_date(str_val):
                all_dates = False

        # Return most specific type
        if all_booleans and len(set(str(v).lower() for v in values)) <= 4:
            return "boolean"
        elif all_integers:
            return "integer"
        elif all_floats:
            return "float"
        elif all_dates:
            return "datetime"
        else:
            # Check for long text
            max_length = max(len(str(v)) for v in values)
            return "text" if max_length > 255 else "string"

    @staticmethod
    def _detect_nullable(data: List[Dict], column: str) -> bool:
        """Detect if column should be nullable"""
        total = len(data)
        null_count = sum(
            1
            for row in data
            if row.get(column) is None or str(row.get(column, "")).strip() == ""
        )
        return null_count > 0

    @staticmethod
    def _looks_like_date(value: str) -> bool:
        """Check if value looks like date"""
        import re

        date_patterns = [
            r"^\d{4}-\d{2}-\d{2}$",
            r"^\d{2}/\d{2}/\d{4}$",
            r"^\d{2}-\d{2}-\d{4}$",
        ]
        return any(re.match(pattern, value) for pattern in date_patterns)


class SchemaService:
    """Database schema management service"""

    def __init__(self, connection_service):
        self.connection_service = connection_service
        self.schema_cache = {}
        self.schema_history_file = Path("logs/schema_history.json")
        self.schema_history_file.parent.mkdir(exist_ok=True)

    def analyze_and_create_table(
        self, table_name: str, excel_data: List[Dict[str, Any]], mode: str = "create"
    ) -> Tuple[bool, str]:
        """Analyze Excel data and create/update table schema"""
        try:
            # Analyze data to create schema
            schema = SchemaAnalyzer.analyze_excel_data(excel_data, table_name)

            # Get database type
            db_type = self._get_database_type()

            if mode == "create" or not self._table_exists(table_name):
                return self._create_table(schema, db_type)
            elif mode == "update":
                return self._update_table_schema(schema, db_type)
            else:
                return False, f"Invalid mode: {mode}"

        except Exception as e:
            logger.error(f"Schema creation failed: {e}")
            return False, str(e)

    def _get_database_type(self) -> str:
        """Get current database type"""
        if hasattr(self.connection_service, "current_config"):
            config = self.connection_service.current_config
            return config.get("type", "sqlite") if config else "sqlite"
        return "sqlite"

    def _table_exists(self, table_name: str) -> bool:
        """Check if table exists"""
        try:
            tables = self.connection_service.get_tables()
            return table_name.lower() in [t.lower() for t in tables]
        except Exception:
            return False

    def _create_table(self, schema: TableSchema, db_type: str) -> Tuple[bool, str]:
        """Create new table"""
        try:
            create_sql = schema.to_create_sql(db_type)
            success, result = self.connection_service.execute_query(create_sql)

            if success:
                self._log_schema_change("CREATE", schema.name, schema)
                self.schema_cache[schema.name] = schema
                return True, f"Table '{schema.name}' created successfully"
            else:
                return False, f"Failed to create table: {result}"

        except Exception as e:
            return False, str(e)

    def _update_table_schema(
        self, new_schema: TableSchema, db_type: str
    ) -> Tuple[bool, str]:
        """Update existing table schema"""
        try:
            # Get existing columns
            existing_columns = self._get_existing_columns(new_schema.name)

            # Generate ALTER statements
            alter_statements = new_schema.to_alter_sql(existing_columns, db_type)

            if not alter_statements:
                return True, "No schema changes needed"

            # Execute ALTER statements
            for statement in alter_statements:
                success, result = self.connection_service.execute_query(statement)
                if not success:
                    return False, f"Failed to alter table: {result}"

            self._log_schema_change("ALTER", new_schema.name, new_schema)
            self.schema_cache[new_schema.name] = new_schema

            return (
                True,
                f"Table '{new_schema.name}' updated with {len(alter_statements)} new columns",
            )

        except Exception as e:
            return False, str(e)

    def _get_existing_columns(self, table_name: str) -> List[str]:
        """Get existing column names"""
        try:
            schema = self.connection_service.get_table_schema(table_name)
            return [col.get("name", "") for col in schema]
        except Exception:
            return []

    def get_table_schema_info(self, table_name: str) -> Dict[str, Any]:
        """Get comprehensive table schema information"""
        try:
            if table_name in self.schema_cache:
                schema = self.schema_cache[table_name]
                return {
                    "table_name": schema.name,
                    "columns": [
                        {
                            "name": col.name,
                            "type": col.data_type,
                            "nullable": col.nullable,
                            "primary_key": col.primary_key,
                            "default": col.default,
                        }
                        for col in schema.columns
                    ],
                    "created_at": schema.created_at.isoformat(),
                    "source": "cache",
                }

            # Get from database
            db_schema = self.connection_service.get_table_schema(table_name)
            return {
                "table_name": table_name,
                "columns": db_schema,
                "source": "database",
            }

        except Exception as e:
            return {"error": str(e)}

    def suggest_schema_improvements(
        self, table_name: str, sample_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Suggest schema improvements based on data analysis"""
        try:
            suggestions = {"optimization": [], "data_quality": [], "performance": []}

            # Analyze current schema
            current_schema = self.get_table_schema_info(table_name)
            if "error" in current_schema:
                return current_schema

            # Analyze sample data
            for column_data in current_schema["columns"]:
                col_name = column_data["name"]
                if col_name == "id":  # Skip ID column
                    continue

                values = [
                    row.get(col_name)
                    for row in sample_data
                    if row.get(col_name) is not None
                ]

                if not values:
                    continue

                # Check for better data types
                suggested_type = SchemaAnalyzer._detect_column_type(
                    sample_data, col_name
                )
                current_type = column_data["type"]

                if suggested_type != current_type and self._is_type_upgrade(
                    current_type, suggested_type
                ):
                    suggestions["optimization"].append(
                        f"Column '{col_name}': Consider changing from {current_type} to {suggested_type}"
                    )

                # Check for indexing opportunities
                unique_ratio = len(set(values)) / len(values) if values else 0
                if unique_ratio > 0.8:
                    suggestions["performance"].append(
                        f"Column '{col_name}': High uniqueness ({unique_ratio:.2%}) - consider adding index"
                    )

                # Check data quality
                null_ratio = sum(
                    1 for v in values if v is None or str(v).strip() == ""
                ) / len(sample_data)
                if null_ratio > 0.5:
                    suggestions["data_quality"].append(
                        f"Column '{col_name}': High null ratio ({null_ratio:.2%}) - consider data validation"
                    )

            return suggestions

        except Exception as e:
            return {"error": str(e)}

    def _is_type_upgrade(self, current: str, suggested: str) -> bool:
        """Check if suggested type is an upgrade"""
        type_hierarchy = {
            "string": 1,
            "integer": 2,
            "float": 2,
            "boolean": 2,
            "datetime": 3,
            "text": 1,
        }

        return type_hierarchy.get(suggested, 0) > type_hierarchy.get(current, 0)

    def backup_schema(self, table_name: str) -> bool:
        """Create backup of table schema"""
        try:
            schema_info = self.get_table_schema_info(table_name)
            if "error" in schema_info:
                return False

            backup_file = Path(
                f"backups/schema_{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            backup_file.parent.mkdir(exist_ok=True)

            with open(backup_file, "w", encoding="utf-8") as f:
                json.dump(schema_info, f, indent=2, ensure_ascii=False)

            logger.info(f"Schema backup created: {backup_file}")
            return True

        except Exception as e:
            logger.error(f"Schema backup failed: {e}")
            return False

    def _log_schema_change(self, action: str, table_name: str, schema: TableSchema):
        """Log schema changes for audit trail"""
        try:
            change_record = {
                "timestamp": datetime.now().isoformat(),
                "action": action,
                "table_name": table_name,
                "columns": [
                    {
                        "name": col.name,
                        "type": col.data_type,
                        "nullable": col.nullable,
                        "primary_key": col.primary_key,
                    }
                    for col in schema.columns
                ],
            }

            # Load existing history
            history = []
            if self.schema_history_file.exists():
                with open(self.schema_history_file, "r", encoding="utf-8") as f:
                    history = json.load(f)

            history.append(change_record)

            # Keep last 100 changes
            history = history[-100:]

            # Save updated history
            with open(self.schema_history_file, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Failed to log schema change: {e}")

    def get_schema_history(self, table_name: str = None) -> List[Dict[str, Any]]:
        """Get schema change history"""
        try:
            if not self.schema_history_file.exists():
                return []

            with open(self.schema_history_file, "r", encoding="utf-8") as f:
                history = json.load(f)

            if table_name:
                history = [h for h in history if h.get("table_name") == table_name]

            return history

        except Exception as e:
            logger.error(f"Failed to get schema history: {e}")
            return []

    def validate_data_against_schema(
        self, table_name: str, data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Validate data against table schema"""
        try:
            schema_info = self.get_table_schema_info(table_name)
            if "error" in schema_info:
                return schema_info

            validation_results = {"valid": True, "errors": [], "warnings": []}

            columns = {col["name"]: col for col in schema_info["columns"]}

            for row_idx, row in enumerate(data):
                for col_name, col_info in columns.items():
                    if col_name == "id":  # Skip auto-increment ID
                        continue

                    value = row.get(col_name)

                    # Check nullable constraint
                    if not col_info["nullable"] and (
                        value is None or str(value).strip() == ""
                    ):
                        validation_results["errors"].append(
                            f"Row {row_idx + 1}: Column '{col_name}' cannot be null"
                        )
                        validation_results["valid"] = False

                    # Type validation (basic)
                    if value is not None and not self._validate_type(
                        value, col_info["type"]
                    ):
                        validation_results["warnings"].append(
                            f"Row {row_idx + 1}: Column '{col_name}' type mismatch"
                        )

            return validation_results

        except Exception as e:
            return {"error": str(e)}

    def _validate_type(self, value: Any, expected_type: str) -> bool:
        """Basic type validation"""
        try:
            if expected_type == "integer":
                int(value)
            elif expected_type == "float":
                float(value)
            elif expected_type == "boolean":
                str(value).lower() in ["true", "false", "1", "0", "yes", "no"]
            # String types are always valid
            return True
        except (ValueError, TypeError):
            return False
