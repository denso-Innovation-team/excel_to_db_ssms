"""
services/auto_table_generator.py
Smart Schema Creation & Relationship Detection System
เฮียตอมจัดหั้ย!!! 🚀
"""

import re
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, field
from pathlib import Path
import json
import pandas as pd

logger = logging.getLogger(__name__)


@dataclass
class ColumnSchema:
    """Enhanced column schema definition"""

    name: str
    original_name: str
    data_type: str
    max_length: Optional[int] = None
    nullable: bool = True
    default_value: Any = None
    is_primary_key: bool = False
    is_foreign_key: bool = False
    foreign_table: Optional[str] = None
    foreign_column: Optional[str] = None
    constraints: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TableSchema:
    """Complete table schema with relationships"""

    name: str
    columns: List[ColumnSchema]
    primary_keys: List[str] = field(default_factory=list)
    foreign_keys: List[Dict[str, str]] = field(default_factory=list)
    indexes: List[Dict[str, Any]] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class DataTypeDetector:
    """Advanced data type detection with statistical analysis"""

    def __init__(self):
        self.type_patterns = {
            "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            "phone": r"^[\+]?[\d\s\-\(\)]{10,}$",
            "url": r"^https?://",
            "uuid": r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            "ip_address": r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",
            "date_iso": r"^\d{4}-\d{2}-\d{2}$",
            "datetime_iso": r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}",
            "currency": r"^[\$€£¥]?\d+[\.\,]?\d*$",
            "percentage": r"^\d+[\.\,]?\d*%$",
        }

        self.sql_type_mapping = {
            "sqlite": {
                "integer": "INTEGER",
                "bigint": "INTEGER",
                "float": "REAL",
                "decimal": "REAL",
                "boolean": "BOOLEAN",
                "string": "TEXT",
                "text": "TEXT",
                "date": "DATE",
                "datetime": "DATETIME",
                "time": "TIME",
                "json": "TEXT",
                "uuid": "TEXT",
            },
            "sqlserver": {
                "integer": "INT",
                "bigint": "BIGINT",
                "float": "FLOAT",
                "decimal": "DECIMAL(18,2)",
                "boolean": "BIT",
                "string": "NVARCHAR(255)",
                "text": "NVARCHAR(MAX)",
                "date": "DATE",
                "datetime": "DATETIME2",
                "time": "TIME",
                "json": "NVARCHAR(MAX)",
                "uuid": "UNIQUEIDENTIFIER",
            },
        }

    def analyze_column(self, data: pd.Series, column_name: str) -> Dict[str, Any]:
        """Deep analysis of column data"""
        non_null_data = data.dropna()
        total_count = len(data)
        non_null_count = len(non_null_data)

        if non_null_count == 0:
            return {
                "data_type": "string",
                "nullable": True,
                "max_length": 255,
                "constraints": [],
                "metadata": {"null_ratio": 1.0},
            }

        # Convert to string for pattern analysis
        str_data = non_null_data.astype(str)

        # Statistical analysis
        stats = {
            "null_ratio": (total_count - non_null_count) / total_count,
            "unique_count": non_null_data.nunique(),
            "unique_ratio": non_null_data.nunique() / non_null_count,
            "max_length": str_data.str.len().max(),
            "min_length": str_data.str.len().min(),
            "avg_length": str_data.str.len().mean(),
        }

        # Type detection priority
        detected_type = self._detect_specific_type(str_data, stats)

        # Generate constraints and metadata
        constraints = self._generate_constraints(non_null_data, detected_type, stats)
        metadata = self._generate_metadata(non_null_data, detected_type, stats)

        return {
            "data_type": detected_type,
            "nullable": stats["null_ratio"] > 0,
            "max_length": self._calculate_optimal_length(detected_type, stats),
            "constraints": constraints,
            "metadata": {**stats, **metadata},
        }

    def _detect_specific_type(self, str_data: pd.Series, stats: Dict) -> str:
        """Detect specific data type with pattern matching"""
        sample_size = min(100, len(str_data))
        sample = str_data.head(sample_size)

        # Pattern-based detection
        for pattern_name, pattern in self.type_patterns.items():
            matches = sample.str.match(pattern, case=False).sum()
            match_ratio = matches / sample_size

            if match_ratio > 0.8:  # 80% pattern match
                type_mapping = {
                    "email": "string",
                    "phone": "string",
                    "url": "text",
                    "uuid": "uuid",
                    "ip_address": "string",
                    "date_iso": "date",
                    "datetime_iso": "datetime",
                    "currency": "decimal",
                    "percentage": "float",
                }
                return type_mapping.get(pattern_name, "string")

        # Numeric type detection
        try:
            numeric_data = pd.to_numeric(str_data, errors="coerce")
            valid_numeric = ~numeric_data.isna()
            numeric_ratio = valid_numeric.sum() / len(str_data)

            if numeric_ratio > 0.9:  # 90% numeric
                if (numeric_data == numeric_data.astype(int, errors="ignore")).all():
                    # Check integer range
                    if numeric_data.max() > 2147483647:
                        return "bigint"
                    return "integer"
                return "float"
        except:
            pass

        # Boolean detection
        unique_lower = set(str_data.str.lower().unique())
        bool_values = {"true", "false", "1", "0", "yes", "no", "y", "n"}
        if unique_lower.issubset(bool_values) and len(unique_lower) <= 2:
            return "boolean"

        # Date/time detection
        try:
            pd.to_datetime(str_data, errors="raise")
            return "datetime"
        except:
            pass

        # JSON detection
        if self._looks_like_json(sample):
            return "json"

        # String vs Text based on length
        if stats["max_length"] > 500 or stats["avg_length"] > 100:
            return "text"

        return "string"

    def _looks_like_json(self, data: pd.Series) -> bool:
        """Check if data looks like JSON"""
        try:
            sample = data.head(10)
            json_count = 0
            for value in sample:
                if value.strip().startswith(("{", "[")):
                    try:
                        json.loads(value)
                        json_count += 1
                    except:
                        pass
            return json_count / len(sample) > 0.7
        except:
            return False

    def _generate_constraints(
        self, data: pd.Series, data_type: str, stats: Dict
    ) -> List[str]:
        """Generate appropriate constraints"""
        constraints = []

        # Unique constraint
        if stats["unique_ratio"] > 0.95:
            constraints.append("UNIQUE")

        # Check constraints based on type
        if data_type in ["integer", "bigint", "float", "decimal"]:
            min_val = data.min()
            max_val = data.max()
            if min_val >= 0:
                constraints.append("CHECK (value >= 0)")

        # String length constraints
        if data_type in ["string", "text"] and stats["max_length"] > 0:
            constraints.append(f'CHECK (LENGTH(value) <= {stats["max_length"]})')

        return constraints

    def _generate_metadata(
        self, data: pd.Series, data_type: str, stats: Dict
    ) -> Dict[str, Any]:
        """Generate column metadata"""
        metadata = {
            "suggested_index": stats["unique_ratio"] > 0.7,
            "data_quality_score": self._calculate_quality_score(data, stats),
            "pattern_detected": self._detect_pattern_name(data),
            "business_meaning": self._infer_business_meaning(data.name, data_type),
        }

        # Type-specific metadata
        if data_type in ["integer", "bigint", "float"]:
            metadata.update(
                {
                    "min_value": data.min(),
                    "max_value": data.max(),
                    "mean_value": data.mean(),
                    "std_value": data.std(),
                }
            )

        return metadata

    def _calculate_optimal_length(self, data_type: str, stats: Dict) -> Optional[int]:
        """Calculate optimal column length"""
        if data_type == "string":
            # Add 20% buffer to max length, minimum 50
            return max(50, int(stats["max_length"] * 1.2))
        elif data_type == "text":
            return None  # No length limit for text
        return None

    def _calculate_quality_score(self, data: pd.Series, stats: Dict) -> float:
        """Calculate data quality score (0-1)"""
        score = 1.0

        # Penalize high null ratio
        score -= stats["null_ratio"] * 0.3

        # Reward consistent patterns
        if stats["unique_ratio"] < 0.1:  # Too many duplicates
            score -= 0.2
        elif stats["unique_ratio"] > 0.95:  # Good uniqueness
            score += 0.1

        return max(0, min(1, score))

    def _detect_pattern_name(self, data: pd.Series) -> Optional[str]:
        """Detect specific patterns in data"""
        str_data = data.astype(str).head(50)

        for pattern_name, pattern in self.type_patterns.items():
            matches = str_data.str.match(pattern, case=False).sum()
            if matches / len(str_data) > 0.8:
                return pattern_name

        return None

    def _infer_business_meaning(
        self, column_name: str, data_type: str
    ) -> Optional[str]:
        """Infer business meaning from column name"""
        name_lower = column_name.lower()

        business_patterns = {
            "id": "identifier",
            "email": "contact_information",
            "phone": "contact_information",
            "address": "location",
            "name": "personal_information",
            "date": "temporal",
            "time": "temporal",
            "amount": "financial",
            "price": "financial",
            "cost": "financial",
            "status": "categorical",
            "type": "categorical",
            "category": "categorical",
        }

        for pattern, meaning in business_patterns.items():
            if pattern in name_lower:
                return meaning

        return None


class RelationshipDetector:
    """Automatic foreign key and relationship detection"""

    def __init__(self):
        self.confidence_threshold = 0.8
        self.naming_patterns = {
            "foreign_key": [r"(.+)_id$", r"(.+)id$", r"fk_(.+)$", r"ref_(.+)$"],
            "primary_key": [r"^id$", r"^(.+)_id$", r"^pk_", r"^primary_"],
        }

    def detect_relationships(
        self, tables_data: Dict[str, pd.DataFrame]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Detect relationships between tables"""
        relationships = {}

        # Get all potential keys
        potential_keys = self._identify_potential_keys(tables_data)

        for table_name, df in tables_data.items():
            table_relationships = []

            for column in df.columns:
                # Check if column looks like foreign key
                fk_candidates = self._find_foreign_key_candidates(
                    column, df[column], tables_data, table_name
                )

                for candidate in fk_candidates:
                    confidence = self._calculate_relationship_confidence(
                        df[column], tables_data[candidate["table"]][candidate["column"]]
                    )

                    if confidence >= self.confidence_threshold:
                        table_relationships.append(
                            {
                                "type": "foreign_key",
                                "column": column,
                                "references_table": candidate["table"],
                                "references_column": candidate["column"],
                                "confidence": confidence,
                                "relationship_type": self._infer_relationship_type(
                                    df,
                                    column,
                                    tables_data[candidate["table"]],
                                    candidate["column"],
                                ),
                            }
                        )

            relationships[table_name] = table_relationships

        return relationships

    def _identify_potential_keys(
        self, tables_data: Dict[str, pd.DataFrame]
    ) -> Dict[str, Dict[str, Any]]:
        """Identify potential primary and foreign keys"""
        keys = {}

        for table_name, df in tables_data.items():
            table_keys = {"primary": [], "foreign": []}

            for column in df.columns:
                col_data = df[column]

                # Primary key detection
                if self._looks_like_primary_key(column, col_data):
                    table_keys["primary"].append(
                        {
                            "column": column,
                            "confidence": self._calculate_pk_confidence(
                                column, col_data
                            ),
                        }
                    )

                # Foreign key detection
                if self._looks_like_foreign_key(column):
                    table_keys["foreign"].append(
                        {
                            "column": column,
                            "referenced_table": self._extract_referenced_table(column),
                        }
                    )

            keys[table_name] = table_keys

        return keys

    def _looks_like_primary_key(self, column_name: str, data: pd.Series) -> bool:
        """Check if column looks like primary key"""
        # Name-based detection
        for pattern in self.naming_patterns["primary_key"]:
            if re.match(pattern, column_name.lower()):
                # Data-based validation
                return (
                    data.nunique() == len(data)  # Unique
                    and data.notna().all()  # No nulls
                    and len(data) > 0  # Has data
                )

        return False

    def _looks_like_foreign_key(self, column_name: str) -> bool:
        """Check if column name suggests foreign key"""
        for pattern in self.naming_patterns["foreign_key"]:
            if re.match(pattern, column_name.lower()):
                return True
        return False

    def _extract_referenced_table(self, column_name: str) -> Optional[str]:
        """Extract referenced table name from FK column name"""
        for pattern in self.naming_patterns["foreign_key"]:
            match = re.match(pattern, column_name.lower())
            if match:
                return match.group(1)
        return None

    def _find_foreign_key_candidates(
        self,
        column: str,
        data: pd.Series,
        all_tables: Dict[str, pd.DataFrame],
        current_table: str,
    ) -> List[Dict[str, str]]:
        """Find potential foreign key targets"""
        candidates = []

        # Extract potential table name from column
        potential_table = self._extract_referenced_table(column)

        for table_name, df in all_tables.items():
            if table_name == current_table:
                continue

            # Check if table name matches potential reference
            if potential_table and potential_table in table_name.lower():
                # Look for matching columns
                for col in df.columns:
                    if self._looks_like_primary_key(col, df[col]):
                        candidates.append({"table": table_name, "column": col})

            # Also check for exact column name matches
            if column in df.columns:
                candidates.append({"table": table_name, "column": column})

        return candidates

    def _calculate_relationship_confidence(
        self, fk_data: pd.Series, pk_data: pd.Series
    ) -> float:
        """Calculate confidence score for relationship"""
        # Remove nulls for comparison
        fk_non_null = fk_data.dropna()
        pk_non_null = pk_data.dropna()

        if len(fk_non_null) == 0 or len(pk_non_null) == 0:
            return 0.0

        # Check value overlap
        fk_values = set(fk_non_null.astype(str))
        pk_values = set(pk_non_null.astype(str))

        overlap = len(fk_values.intersection(pk_values))
        overlap_ratio = overlap / len(fk_values) if len(fk_values) > 0 else 0

        # Data type compatibility
        type_compatible = self._check_type_compatibility(fk_data, pk_data)

        # Calculate confidence
        confidence = (overlap_ratio * 0.7) + (type_compatible * 0.3)
        return confidence

    def _check_type_compatibility(self, data1: pd.Series, data2: pd.Series) -> float:
        """Check if data types are compatible"""
        try:
            # Try to convert both to same type
            pd.to_numeric(data1, errors="raise")
            pd.to_numeric(data2, errors="raise")
            return 1.0  # Both numeric
        except:
            pass

        # String comparison
        if data1.dtype == "object" and data2.dtype == "object":
            return 0.8

        return 0.5  # Partial compatibility

    def _infer_relationship_type(
        self, table1: pd.DataFrame, col1: str, table2: pd.DataFrame, col2: str
    ) -> str:
        """Infer relationship type (1:1, 1:M, M:M)"""
        # Count unique values
        table1_unique = table1[col1].nunique()
        table2_unique = table2[col2].nunique()

        table1_count = len(table1)
        table2_count = len(table2)

        # Determine relationship type
        if table1_unique == table1_count and table2_unique == table2_count:
            return "1:1"
        elif table1_unique < table1_count and table2_unique == table2_count:
            return "M:1"
        elif table1_unique == table1_count and table2_unique < table2_count:
            return "1:M"
        else:
            return "M:M"

    def _calculate_pk_confidence(self, column_name: str, data: pd.Series) -> float:
        """Calculate primary key confidence"""
        confidence = 0.0

        # Name-based confidence
        if column_name.lower() == "id":
            confidence += 0.3
        elif "_id" in column_name.lower():
            confidence += 0.2

        # Data-based confidence
        if data.nunique() == len(data):  # Unique
            confidence += 0.4
        if data.notna().all():  # No nulls
            confidence += 0.3

        return confidence


class IndexSuggestionEngine:
    """Intelligent index suggestion system"""

    def __init__(self):
        self.index_types = {
            "primary": "PRIMARY KEY",
            "unique": "UNIQUE INDEX",
            "regular": "INDEX",
            "composite": "COMPOSITE INDEX",
            "partial": "PARTIAL INDEX",
        }

    def suggest_indexes(
        self, table_schema: TableSchema, sample_data: pd.DataFrame
    ) -> List[Dict[str, Any]]:
        """Suggest optimal indexes for table"""
        suggestions = []

        # Primary key index (automatic)
        pk_columns = [col.name for col in table_schema.columns if col.is_primary_key]
        if pk_columns:
            suggestions.append(
                {
                    "type": "primary",
                    "columns": pk_columns,
                    "name": f"PK_{table_schema.name}",
                    "rationale": "Primary key constraint",
                    "priority": "critical",
                }
            )

        # Foreign key indexes
        fk_columns = [col.name for col in table_schema.columns if col.is_foreign_key]
        for fk_col in fk_columns:
            suggestions.append(
                {
                    "type": "regular",
                    "columns": [fk_col],
                    "name": f"IDX_{table_schema.name}_{fk_col}",
                    "rationale": "Foreign key lookup optimization",
                    "priority": "high",
                }
            )

        # Unique constraints
        for col in table_schema.columns:
            if "UNIQUE" in col.constraints:
                suggestions.append(
                    {
                        "type": "unique",
                        "columns": [col.name],
                        "name": f"UQ_{table_schema.name}_{col.name}",
                        "rationale": "Unique constraint enforcement",
                        "priority": "high",
                    }
                )

        # High-selectivity columns
        for col in table_schema.columns:
            if col.metadata.get("unique_ratio", 0) > 0.8:
                suggestions.append(
                    {
                        "type": "regular",
                        "columns": [col.name],
                        "name": f"IDX_{table_schema.name}_{col.name}",
                        "rationale": f"High selectivity ({col.metadata['unique_ratio']:.2%})",
                        "priority": "medium",
                    }
                )

        # Composite indexes for common query patterns
        text_columns = [
            col.name
            for col in table_schema.columns
            if col.data_type in ["string", "text"]
        ]
        if len(text_columns) >= 2:
            suggestions.append(
                {
                    "type": "composite",
                    "columns": text_columns[:2],
                    "name": f"IDX_{table_schema.name}_search",
                    "rationale": "Text search optimization",
                    "priority": "low",
                }
            )

        return suggestions


class AutoTableGenerator:
    """Main auto table generation service"""

    def __init__(self, connection_service=None):
        self.connection_service = connection_service
        self.type_detector = DataTypeDetector()
        self.relationship_detector = RelationshipDetector()
        self.index_engine = IndexSuggestionEngine()

        # Configuration
        self.config = {
            "auto_create_indexes": True,
            "detect_relationships": True,
            "optimize_data_types": True,
            "generate_constraints": True,
            "backup_existing": True,
        }

        # State tracking
        self.generated_schemas = {}
        self.generation_history = []

    def analyze_excel_data(
        self, excel_data: Dict[str, pd.DataFrame]
    ) -> Dict[str, TableSchema]:
        """Analyze Excel data and generate optimal schemas"""
        schemas = {}

        logger.info(
            f"🔍 Analyzing {len(excel_data)} Excel sheets for schema generation"
        )

        # Step 1: Analyze individual tables
        for sheet_name, df in excel_data.items():
            logger.info(f"📊 Analyzing sheet: {sheet_name}")
            schema = self._analyze_single_table(sheet_name, df)
            schemas[sheet_name] = schema

        # Step 2: Detect relationships
        if self.config["detect_relationships"] and len(excel_data) > 1:
            logger.info("🔗 Detecting relationships between tables")
            relationships = self.relationship_detector.detect_relationships(excel_data)
            schemas = self._apply_relationships(schemas, relationships)

        # Step 3: Generate indexes
        if self.config["auto_create_indexes"]:
            logger.info("⚡ Generating index suggestions")
            for table_name, schema in schemas.items():
                schema.indexes = self.index_engine.suggest_indexes(
                    schema, excel_data[table_name]
                )

        self.generated_schemas = schemas
        return schemas

    def _analyze_single_table(self, table_name: str, df: pd.DataFrame) -> TableSchema:
        """Analyze single table and generate schema"""
        # Clean table name
        clean_table_name = self._clean_table_name(table_name)

        # Analyze columns
        columns = []
        for col_name in df.columns:
            logger.debug(f"  📋 Analyzing column: {col_name}")

            analysis = self.type_detector.analyze_column(df[col_name], col_name)

            column_schema = ColumnSchema(
                name=self._clean_column_name(col_name),
                original_name=col_name,
                data_type=analysis["data_type"],
                max_length=analysis["max_length"],
                nullable=analysis["nullable"],
                constraints=analysis["constraints"],
                metadata=analysis["metadata"],
            )

            # Detect primary key
            if self._is_primary_key_candidate(col_name, df[col_name]):
                column_schema.is_primary_key = True
                column_schema.nullable = False

            columns.append(column_schema)

        # Create table schema
        schema = TableSchema(
            name=clean_table_name,
            columns=columns,
            primary_keys=[col.name for col in columns if col.is_primary_key],
            metadata={
                "original_name": table_name,
                "row_count": len(df),
                "column_count": len(df.columns),
                "created_at": datetime.now().isoformat(),
            },
        )

        return schema

    def _apply_relationships(
        self,
        schemas: Dict[str, TableSchema],
        relationships: Dict[str, List[Dict[str, Any]]],
    ) -> Dict[str, TableSchema]:
        """Apply detected relationships to schemas"""
        for table_name, table_relationships in relationships.items():
            if table_name not in schemas:
                continue

            schema = schemas[table_name]

            for rel in table_relationships:
                if rel["type"] == "foreign_key":
                    # Find column and mark as FK
                    for col in schema.columns:
                        if (
                            col.name == rel["column"]
                            or col.original_name == rel["column"]
                        ):
                            col.is_foreign_key = True
                            col.foreign_table = rel["references_table"]
                            col.foreign_column = rel["references_column"]

                            # Add to table FK list
                            schema.foreign_keys.append(
                                {
                                    "column": col.name,
                                    "references_table": rel["references_table"],
                                    "references_column": rel["references_column"],
                                    "confidence": rel["confidence"],
                                }
                            )
                            break

        return schemas

    def generate_create_statements(
        self, schemas: Dict[str, TableSchema], db_type: str = "sqlite"
    ) -> Dict[str, str]:
        """Generate CREATE TABLE statements"""
        statements = {}

        for table_name, schema in schemas.items():
            sql = self._generate_create_sql(schema, db_type)
            statements[table_name] = sql

        return statements

    def _generate_create_sql(self, schema: TableSchema, db_type: str) -> str:
        """Generate CREATE TABLE SQL for specific database"""
        type_mapping = self.type_detector.sql_type_mapping[db_type]

        # Column definitions
        column_defs = []

        for col in schema.columns:
            col_def = f"[{col.name}] {type_mapping[col.data_type]}"

            # Length specification
            if col.max_length and col.data_type == "string" and db_type == "sqlserver":
                col_def = f"[{col.name}] NVARCHAR({col.max_length})"

            # Nullable
            if not col.nullable:
                col_def += " NOT NULL"

            # Default value
            if col.default_value is not None:
                col_def += f" DEFAULT {col.default_value}"

            # Primary key
            if col.is_primary_key and db_type == "sqlite":
                col_def += " PRIMARY KEY AUTOINCREMENT"
            elif col.is_primary_key and db_type == "sqlserver":
                col_def += " IDENTITY(1,1) PRIMARY KEY"

            column_defs.append(col_def)

        # Foreign key constraints
        fk_constraints = []
        for fk in schema.foreign_keys:
            fk_constraint = (
                f"FOREIGN KEY ([{fk['column']}]) "
                f"REFERENCES [{fk['references_table']}]([{fk['references_column']}])"
            )
            fk_constraints.append(fk_constraint)

        # Combine all parts
        all_defs = column_defs + fk_constraints

        sql = f"""CREATE TABLE [{schema.name}] (
    {',\\n    '.join(all_defs)}
);"""

        return sql

    def create_tables_automatically(
        self, excel_data: Dict[str, pd.DataFrame], options: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Automatically create tables from Excel data"""
        options = options or {}
        results = {
            "created_tables": [],
            "failed_tables": [],
            "warnings": [],
            "schemas": {},
            "execution_time": 0,
        }

        start_time = datetime.now()

        try:
            # Step 1: Analyze and generate schemas
            logger.info("🚀 Starting automatic table generation")
            schemas = self.analyze_excel_data(excel_data)
            results["schemas"] = {
                name: self._schema_to_dict(schema) for name, schema in schemas.items()
            }

            # Step 2: Create tables in dependency order
            creation_order = self._determine_creation_order(schemas)

            for table_name in creation_order:
                schema = schemas[table_name]

                try:
                    # Backup existing table if requested
                    if options.get("backup_existing", True):
                        self._backup_existing_table(table_name)

                    # Generate and execute CREATE statement
                    db_type = self._get_database_type()
                    create_sql = self._generate_create_sql(schema, db_type)

                    # Drop existing table if replace mode
                    if options.get("replace_existing", False):
                        self._drop_table_if_exists(table_name)

                    # Execute CREATE TABLE
                    success = self._execute_create_table(create_sql, table_name)

                    if success:
                        results["created_tables"].append(
                            {
                                "table_name": table_name,
                                "columns": len(schema.columns),
                                "relationships": len(schema.foreign_keys),
                                "indexes": len(schema.indexes),
                            }
                        )

                        # Create indexes
                        if self.config["auto_create_indexes"]:
                            self._create_indexes(schema)

                        logger.info(f"✅ Created table: {table_name}")
                    else:
                        results["failed_tables"].append(table_name)

                except Exception as e:
                    logger.error(f"❌ Failed to create table {table_name}: {e}")
                    results["failed_tables"].append(table_name)
                    results["warnings"].append(f"Table {table_name}: {str(e)}")

            # Step 3: Generate summary report
            results["execution_time"] = (datetime.now() - start_time).total_seconds()

            # Save generation history
            self._save_generation_history(results)

            logger.info(
                f"🎉 Table generation completed: {len(results['created_tables'])} created, {len(results['failed_tables'])} failed"
            )

        except Exception as e:
            logger.error(f"💥 Auto table generation failed: {e}")
            results["warnings"].append(f"Generation failed: {str(e)}")

        return results

    def get_schema_suggestions(
        self, excel_data: Dict[str, pd.DataFrame]
    ) -> Dict[str, Any]:
        """Get schema suggestions without creating tables"""
        suggestions = {
            "tables": {},
            "relationships": [],
            "indexes": [],
            "optimizations": [],
            "warnings": [],
        }

        # Analyze schemas
        schemas = self.analyze_excel_data(excel_data)

        for table_name, schema in schemas.items():
            suggestions["tables"][table_name] = {
                "columns": [self._column_to_dict(col) for col in schema.columns],
                "primary_keys": schema.primary_keys,
                "foreign_keys": schema.foreign_keys,
                "suggested_indexes": [
                    self._index_to_dict(idx) for idx in schema.indexes
                ],
                "metadata": schema.metadata,
            }

        # Relationship suggestions
        if len(excel_data) > 1:
            relationships = self.relationship_detector.detect_relationships(excel_data)
            for table, rels in relationships.items():
                for rel in rels:
                    if rel.get("confidence", 0) >= 0.7:
                        suggestions["relationships"].append(
                            {
                                "from_table": table,
                                "from_column": rel["column"],
                                "to_table": rel["references_table"],
                                "to_column": rel["references_column"],
                                "confidence": rel["confidence"],
                                "type": rel.get("relationship_type", "unknown"),
                            }
                        )

        # Performance optimizations
        suggestions["optimizations"] = self._generate_optimization_suggestions(schemas)

        return suggestions

    def _determine_creation_order(self, schemas: Dict[str, TableSchema]) -> List[str]:
        """Determine optimal table creation order based on dependencies"""
        # Simple topological sort based on foreign keys
        remaining = set(schemas.keys())
        ordered = []

        while remaining:
            # Find tables with no dependencies to remaining tables
            independent = []
            for table_name in remaining:
                schema = schemas[table_name]
                dependencies = {fk["references_table"] for fk in schema.foreign_keys}

                if not dependencies.intersection(remaining):
                    independent.append(table_name)

            if not independent:
                # Circular dependency - add remaining in alphabetical order
                independent = sorted(remaining)

            ordered.extend(independent)
            remaining -= set(independent)

        return ordered

    def _backup_existing_table(self, table_name: str):
        """Backup existing table before replacement"""
        if not self.connection_service:
            return

        try:
            # Check if table exists
            tables = self.connection_service.get_tables()
            if table_name not in tables:
                return

            # Create backup
            backup_name = (
                f"{table_name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            backup_sql = f"CREATE TABLE [{backup_name}] AS SELECT * FROM [{table_name}]"

            success, result = self.connection_service.execute_query(backup_sql)
            if success:
                logger.info(f"📋 Created backup table: {backup_name}")

        except Exception as e:
            logger.warning(f"⚠️ Failed to backup table {table_name}: {e}")

    def _drop_table_if_exists(self, table_name: str):
        """Drop table if it exists"""
        if not self.connection_service:
            return

        try:
            drop_sql = f"DROP TABLE IF EXISTS [{table_name}]"
            self.connection_service.execute_query(drop_sql)
            logger.info(f"🗑️ Dropped existing table: {table_name}")
        except Exception as e:
            logger.warning(f"⚠️ Failed to drop table {table_name}: {e}")

    def _execute_create_table(self, create_sql: str, table_name: str) -> bool:
        """Execute CREATE TABLE statement"""
        if not self.connection_service:
            logger.error("❌ No database connection available")
            return False

        try:
            success, result = self.connection_service.execute_query(create_sql)
            return success
        except Exception as e:
            logger.error(f"❌ Failed to execute CREATE TABLE for {table_name}: {e}")
            return False

    def _create_indexes(self, schema: TableSchema):
        """Create suggested indexes for table"""
        for index in schema.indexes:
            if index.get("priority") in ["critical", "high"]:
                try:
                    index_sql = self._generate_index_sql(index, schema.name)
                    success, result = self.connection_service.execute_query(index_sql)
                    if success:
                        logger.info(f"⚡ Created index: {index['name']}")
                except Exception as e:
                    logger.warning(f"⚠️ Failed to create index {index['name']}: {e}")

    def _generate_index_sql(self, index: Dict[str, Any], table_name: str) -> str:
        """Generate CREATE INDEX SQL"""
        index_type = index["type"]
        columns_str = ", ".join([f"[{col}]" for col in index["columns"]])

        if index_type == "unique":
            return f"CREATE UNIQUE INDEX [{index['name']}] ON [{table_name}] ({columns_str})"
        else:
            return f"CREATE INDEX [{index['name']}] ON [{table_name}] ({columns_str})"

    def _get_database_type(self) -> str:
        """Get current database type"""
        if hasattr(self.connection_service, "current_config"):
            config = self.connection_service.current_config
            return config.get("type", "sqlite") if config else "sqlite"
        return "sqlite"

    def _clean_table_name(self, name: str) -> str:
        """Clean table name for database compatibility"""
        # Remove special characters and spaces
        clean = re.sub(r"[^\w]", "_", str(name).strip())
        clean = re.sub(r"_+", "_", clean)
        clean = clean.strip("_").lower()

        # Ensure valid identifier
        if not clean or clean[0].isdigit():
            clean = f"table_{clean}"

        # Handle reserved words
        reserved = {"table", "index", "view", "trigger", "user", "order", "group"}
        if clean in reserved:
            clean = f"{clean}_tbl"

        return clean

    def _clean_column_name(self, name: str) -> str:
        """Clean column name for database compatibility"""
        clean = re.sub(r"[^\w\s]", "_", str(name).strip())
        clean = re.sub(r"\s+", "_", clean)
        clean = re.sub(r"_+", "_", clean)
        clean = clean.strip("_").lower()

        if not clean or clean[0].isdigit():
            clean = f"col_{clean}"

        # Handle reserved words
        reserved = {"index", "order", "group", "select", "from", "where"}
        if clean in reserved:
            clean = f"{clean}_col"

        return clean

    def _is_primary_key_candidate(self, column_name: str, data: pd.Series) -> bool:
        """Check if column is suitable as primary key"""
        # Name-based check
        name_indicators = ["id", "key", "pk"]
        if any(indicator in column_name.lower() for indicator in name_indicators):
            # Data validation
            return (
                data.nunique() == len(data)  # Unique values
                and data.notna().all()  # No null values
                and len(data) > 0  # Has data
            )
        return False

    def _generate_optimization_suggestions(
        self, schemas: Dict[str, TableSchema]
    ) -> List[Dict[str, Any]]:
        """Generate performance optimization suggestions"""
        suggestions = []

        for table_name, schema in schemas.items():
            # Large text columns suggestion
            for col in schema.columns:
                if col.data_type == "text" and col.metadata.get("avg_length", 0) < 100:
                    suggestions.append(
                        {
                            "type": "data_type_optimization",
                            "table": table_name,
                            "column": col.name,
                            "suggestion": f"Consider using VARCHAR({col.max_length}) instead of TEXT",
                            "impact": "storage_optimization",
                        }
                    )

                # Missing index suggestions
                if col.metadata.get("unique_ratio", 0) > 0.8 and not any(
                    col.name in idx["columns"] for idx in schema.indexes
                ):
                    suggestions.append(
                        {
                            "type": "index_suggestion",
                            "table": table_name,
                            "column": col.name,
                            "suggestion": f"Add index on {col.name} for better query performance",
                            "impact": "query_performance",
                        }
                    )

        return suggestions

    def _schema_to_dict(self, schema: TableSchema) -> Dict[str, Any]:
        """Convert schema to dictionary"""
        return {
            "name": schema.name,
            "columns": [self._column_to_dict(col) for col in schema.columns],
            "primary_keys": schema.primary_keys,
            "foreign_keys": schema.foreign_keys,
            "indexes": [self._index_to_dict(idx) for idx in schema.indexes],
            "metadata": schema.metadata,
        }

    def _column_to_dict(self, col: ColumnSchema) -> Dict[str, Any]:
        """Convert column to dictionary"""
        return {
            "name": col.name,
            "original_name": col.original_name,
            "data_type": col.data_type,
            "max_length": col.max_length,
            "nullable": col.nullable,
            "is_primary_key": col.is_primary_key,
            "is_foreign_key": col.is_foreign_key,
            "foreign_table": col.foreign_table,
            "foreign_column": col.foreign_column,
            "constraints": col.constraints,
            "metadata": col.metadata,
        }

    def _index_to_dict(self, idx: Dict[str, Any]) -> Dict[str, Any]:
        """Convert index to dictionary"""
        return {
            "type": idx["type"],
            "columns": idx["columns"],
            "name": idx["name"],
            "rationale": idx["rationale"],
            "priority": idx["priority"],
        }

    def _save_generation_history(self, results: Dict[str, Any]):
        """Save generation history for auditing"""
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "created_tables": results["created_tables"],
            "failed_tables": results["failed_tables"],
            "execution_time": results["execution_time"],
            "schemas_generated": len(results.get("schemas", {})),
        }

        self.generation_history.append(history_entry)

        # Save to file
        try:
            history_file = Path("logs/table_generation_history.json")
            history_file.parent.mkdir(exist_ok=True)

            with open(history_file, "w", encoding="utf-8") as f:
                json.dump(self.generation_history, f, indent=2, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Failed to save generation history: {e}")

    def get_generation_history(self) -> List[Dict[str, Any]]:
        """Get table generation history"""
        return self.generation_history.copy()

    def cleanup(self):
        """Cleanup service resources"""
        self.generated_schemas.clear()
        logger.info("🧹 Auto table generator cleanup completed")
