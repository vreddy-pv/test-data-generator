import sqlparse
import pandas as pd
from faker import Faker

class TestDataGenerator:
    def __init__(self, schema_file):
        self.schema_file = schema_file
        self.schema = self._parse_schema()
        self.faker = Faker()
        self.generated_data = {}

    def _parse_schema(self):
        with open(self.schema_file, 'r') as f:
            schema_sql = f.read()

        parsed = sqlparse.parse(schema_sql)
        schema = {}

        for statement in parsed:
            if statement.get_type() != 'CREATE':
                continue

            tokens = [t for t in statement.tokens if t.ttype is not sqlparse.tokens.Whitespace]

            table_name = None
            for token in tokens:
                if isinstance(token, sqlparse.sql.Identifier):
                    table_name = token.get_name()
                    break
            if not table_name:
                continue

            columns = []
            in_parenthesis = False
            for token in tokens:
                if token.is_group and isinstance(token, sqlparse.sql.Parenthesis):
                    column_defs = token.value.strip('()').split(',')
                    for col_def in column_defs:
                        col_def = col_def.strip()
                        if not col_def or col_def.upper().startswith('PRIMARY KEY') or col_def.upper().startswith('FOREIGN KEY'):
                            continue
                        parts = col_def.split()
                        if len(parts) >= 2:
                            col_name = parts[0]
                            col_type = parts[1].upper()
                            if '(' in col_type:
                                col_type = col_type.split('(')[0]
                            columns.append({'name': col_name, 'type': col_type})

            schema[table_name] = columns

        return schema

    def generate_test_data(self, num_rows):
        for table_name, columns in self.schema.items():
            self.generated_data[table_name] = []
            for i in range(num_rows):
                row = {}
                for column in columns:
                    col_name = column['name']
                    col_type = column['type']

                    if col_name == 'id':
                        row[col_name] = i + 1
                    elif '_id' in col_name:
                        # Simple foreign key handling
                        referenced_table = col_name.replace('_id', 's')
                        if referenced_table in self.generated_data and self.generated_data[referenced_table]:
                            row[col_name] = self.faker.random_element(elements=[r['id'] for r in self.generated_data[referenced_table]])
                        else:
                            row[col_name] = i + 1 # Fallback
                    elif col_type == 'VARCHAR':
                        if 'email' in col_name:
                            row[col_name] = self.faker.email()
                        elif 'name' in col_name:
                            row[col_name] = self.faker.name()
                        else:
                            row[col_name] = self.faker.sentence()
                    elif col_type == 'INT':
                        row[col_name] = self.faker.random_int(min=1, max=1000)
                    elif col_type == 'DECIMAL':
                        row[col_name] = self.faker.pydecimal(left_digits=3, right_digits=2, positive=True)
                    elif col_type == 'DATE':
                        row[col_name] = self.faker.date_this_decade()
                    elif col_type == 'TIMESTAMP':
                        row[col_name] = self.faker.date_time_this_decade()
                    else:
                        row[col_name] = None
                self.generated_data[table_name].append(row)
        return self.generated_data

    def write_to_sql_file(self, output_file):
        with open(output_file, 'w') as f:
            for table_name, rows in self.generated_data.items():
                for row in rows:
                    columns = ', '.join(row.keys())
                    values = ', '.join([f"'{v}'" if isinstance(v, str) else str(v) for v in row.values()])
                    f.write(f"INSERT INTO {table_name} ({columns}) VALUES ({values});\n")

    def write_to_excel_file(self, output_file):
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            for table_name, rows in self.generated_data.items():
                df = pd.DataFrame(rows)
                df.to_excel(writer, sheet_name=table_name, index=False)
        print(f'Test data written to {output_file}')
