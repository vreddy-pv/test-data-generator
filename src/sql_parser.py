import re

class SQLParser:
    def __init__(self, schema_file, db_type='h2'):
        self.schema_file = schema_file
        self.db_type = db_type

    def parse_schema(self):
        try:
            with open(self.schema_file, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            return {}

        table_regex = self._get_table_regex()
        column_regex = self._get_column_regex()
        fk_regex = re.compile(r"FOREIGN KEY \((\w+)\) REFERENCES (\w+)\((\w+)\)")

        tables = {}
        for table_match in table_regex.finditer(content):
            table_name = table_match.group(1).lower()
            columns_str = table_match.group(2)

            columns = []
            foreign_keys = []
            for line in columns_str.strip().split('\n'):
                line = line.strip().rstrip(',')
                if not line or line.lower().startswith(('primary key', ')')):
                    continue

                fk_match = fk_regex.search(line)
                if fk_match:
                    foreign_keys.append({
                        'column': fk_match.group(1).lower(),
                        'references_table': fk_match.group(2).lower(),
                        'references_column': fk_match.group(3).lower(),
                    })
                    continue

                col_match = column_regex.match(line)
                if col_match:
                    col_name = col_match.group(1).lower()
                    col_type = col_match.group(2)
                    col_constraints = col_match.group(3).strip()
                    columns.append({
                        "name": col_name,
                        "type": col_type,
                        "constraints": col_constraints
                    })
            tables[table_name] = {'columns': columns, 'foreign_keys': foreign_keys}

        return tables

    def _get_table_regex(self):
        if self.db_type == 'mysql':
            return re.compile(r"CREATE TABLE `?(\w+)`? \((.*?)\);", re.DOTALL)
        else:
            return re.compile(r"CREATE TABLE (\w+) \((.*?)\);", re.DOTALL)

    def _get_column_regex(self):
        if self.db_type == 'mysql':
            return re.compile(r"`?(\w+)`?\s+([\w\(\)]+)(.*)")
        else:
            return re.compile(r"(\w+)\s+([\w\(\)]+)(.*)")
