import re
import sqlparse
import pandas as pd
from faker import Faker
from sql_metadata.parser import Parser

class TestDataGenerator:
    def __init__(self, schema_file):
        self.schema_file = schema_file
        self.schema = self._parse_schema()
        self.faker = Faker()
        self.generated_data = {}

    def _parse_schema(self):
        with open(self.schema_file, 'r') as f:
            schema_sql = f.read()

        parser = Parser(schema_sql)
        schema = {}

        # The parser gives tables, but not always columns/types in a structured way.
        # We'll use a hybrid approach: get table names from the parser,
        # but extract column details with sqlparse from the CREATE statements.

        # Initialize schema with all tables found by the parser
        for table_name in parser.tables:
            schema[table_name] = {'columns': [], 'foreign_keys': []}

        # Parse create statements to get column details
        # sql_metadata doesn't expose column types easily, so we still need sqlparse for this.
        for statement in sqlparse.parse(schema_sql):
            if statement.get_type() != 'CREATE':
                continue

            # Find table name for the current CREATE statement
            stmt_table_name = None
            for token in statement.tokens:
                if isinstance(token, sqlparse.sql.Identifier):
                    stmt_table_name = token.get_name().strip('`"')
                    break

            if not stmt_table_name or stmt_table_name not in schema:
                continue

            # Find the parenthesis block with column definitions
            for token in statement.tokens:
                if token.is_group and isinstance(token, sqlparse.sql.Parenthesis):
                    column_defs = token.value.strip('()').split(',')
                    for col_def in column_defs:
                        col_def = col_def.strip()
                        if not col_def or col_def.upper().startswith(('PRIMARY KEY', 'FOREIGN KEY', 'CONSTRAINT')):
                            continue

                        parts = col_def.split()
                        if len(parts) >= 2:
                            col_name = parts[0].strip('`"')
                            col_type = parts[1].upper()
                            if '(' in col_type:
                                col_type = col_type.split('(')[0]
                            schema[stmt_table_name]['columns'].append({'name': col_name, 'type': col_type})

        # Use the parser to get foreign key relationships
        if hasattr(parser, 'foreign_key_references') and parser.foreign_key_references:
            for fk in parser.foreign_key_references:
                table_name = fk['table']
                fk_columns = fk['key']
                ref_table = fk['references_table']
                ref_columns = fk['references_key']

                # For now, we'll simplify and assume single-column foreign keys
                if len(fk_columns) == 1 and len(ref_columns) == 1:
                    if table_name in schema:
                        schema[table_name]['foreign_keys'].append({
                            'column': fk_columns[0].strip('`"'),
                            'references_table': ref_table.strip('`"'),
                            'references_column': ref_columns[0].strip('`"')
                        })

        return schema

    def _topological_sort(self):
        """Performs a topological sort of the tables based on foreign key dependencies."""
        dependencies = {table: [fk['references_table'] for fk in info.get('foreign_keys', [])] for table, info in self.schema.items()}
        sorted_tables = []
        visited = set()

        # In case of circular dependencies, this will break. A full implementation would need cycle detection.
        visiting = set()

        def visit(table):
            if table in visited:
                return
            if table in visiting:
                # Simple cycle detection
                print(f"Warning: Circular dependency detected involving table {table}. This may lead to incorrect generation order.")
                return

            visiting.add(table)

            if table in dependencies:
                for dep in dependencies.get(table, []):
                    # Only visit dependencies that are actually in our schema
                    if dep in self.schema:
                        visit(dep)

            visiting.remove(table)
            visited.add(table)
            sorted_tables.append(table)

        for table in self.schema.keys():
            if table not in visited:
                visit(table)

        return sorted_tables

    def generate_test_data(self, num_rows):
        sorted_tables = self._topological_sort()

        for table_name in sorted_tables:
            if table_name not in self.schema: continue

            columns = self.schema[table_name]['columns']
            self.generated_data[table_name] = []

            # Identify the primary key, assuming 'id' is a common convention
            pk_column = 'id' # Default assumption
            for col in columns:
                if 'id' in col['name'].lower() and col['name'].endswith('id'): # A slightly better heuristic
                    pk_column = col['name']
                    break

            for i in range(num_rows):
                row = {}
                # Generate primary key first
                if any(c['name'] == pk_column for c in columns):
                    row[pk_column] = i + 1

                for column in columns:
                    col_name = column['name']
                    col_type = column['type'].upper()

                    if col_name in row: # Skip if already generated (e.g., PK)
                        continue

                    # Check for foreign key
                    is_foreign_key = False
                    for fk in self.schema[table_name].get('foreign_keys', []):
                        if fk['column'] == col_name:
                            is_foreign_key = True
                            referenced_table = fk['references_table']
                            referenced_column = fk['references_column']

                            if referenced_table in self.generated_data and self.generated_data[referenced_table]:
                                ref_pks = [r[referenced_column] for r in self.generated_data[referenced_table] if referenced_column in r]
                                if ref_pks:
                                    row[col_name] = self.faker.random_element(elements=ref_pks)
                                else:
                                    row[col_name] = None # No valid parent PKs to reference
                            else:
                                row[col_name] = None # Parent table not generated yet
                            break

                    if is_foreign_key:
                        continue

                    # Generate data based on type
                    if 'VARCHAR' in col_type or 'CHAR' in col_type:
                        if 'email' in col_name.lower():
                            row[col_name] = self.faker.email()
                        elif 'name' in col_name.lower():
                            row[col_name] = self.faker.name()
                        elif 'phone' in col_name.lower():
                            row[col_name] = self.faker.phone_number()
                        else:
                            row[col_name] = self.faker.word()
                    elif col_type in ('INT', 'INTEGER', 'BIGINT', 'SMALLINT'):
                        row[col_name] = self.faker.random_int(min=1, max=1000)
                    elif col_type in ('DECIMAL', 'NUMERIC', 'FLOAT', 'DOUBLE'):
                        row[col_name] = self.faker.pydecimal(left_digits=5, right_digits=2, positive=True)
                    elif col_type == 'DATE':
                        row[col_name] = self.faker.date_this_decade()
                    elif 'TIMESTAMP' in col_type:
                        row[col_name] = self.faker.date_time_this_decade()
                    elif col_type == 'BOOLEAN':
                        row[col_name] = self.faker.boolean()
                    else:

                        row[col_name] = None

                self.generated_data[table_name].append(row)
        return self.generated_data

    def write_to_sql_file(self, output_file):
        with open(output_file, 'w', encoding='utf-8') as f:
            sorted_tables = self._topological_sort()
            for table_name in sorted_tables:
                if table_name in self.generated_data:
                    rows = self.generated_data[table_name]
                    if not rows: continue

                    f.write(f"\n-- Data for table: {table_name}\n")
                    for row in rows:
                        # Filter out null values to avoid inserting them explicitly unless necessary
                        valid_row = {k: v for k, v in row.items() if v is not None}
                        if not valid_row: continue

                        columns = ', '.join(valid_row.keys())
                        values = ', '.join([f"'{str(v).replace("'", "''")}'" if isinstance(v, str) else str(v) for v in valid_row.values()])
                        f.write(f"INSERT INTO {table_name} ({columns}) VALUES ({values});\n")

    def write_to_excel_file(self, output_file):
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            sorted_tables = self._topological_sort()
            for table_name in sorted_tables:
                 if table_name in self.generated_data:
                    df = pd.DataFrame(self.generated_data[table_name])
                    df.to_excel(writer, sheet_name=table_name, index=False)
        print(f'Test data written to {output_file}')
