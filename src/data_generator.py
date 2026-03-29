from faker import Faker
import random
from collections import defaultdict

class DataGenerator:
    def __init__(self, tables, db_type='h2'):
        self.tables = tables
        self.db_type = db_type
        self.faker = Faker()
        self.generated_data = {}
        self.generated_pks = defaultdict(list)

    def generate_data(self, num_rows):
        sorted_tables = self._topological_sort()

        for table_name in sorted_tables:
            table_info = self.tables[table_name]
            columns = table_info['columns']
            data = []
            for i in range(num_rows):
                row = {}
                pk_val = None
                for col in columns:
                    val = self._generate_column_data(col, table_info, i + 1)
                    row[col['name']] = val
                    if self._is_primary_key(col):
                        pk_val = val

                if pk_val is not None:
                    self.generated_pks[table_name].append(pk_val)

                data.append(row)
            self.generated_data[table_name] = data

        return self.generated_data

    def _generate_column_data(self, column, table_info, row_index):
        col_name = column['name'].lower()

        # Check for foreign key
        for fk in table_info['foreign_keys']:
            if fk['column'] == col_name:
                ref_table = fk['references_table']
                if self.generated_pks[ref_table]:
                    return random.choice(self.generated_pks[ref_table])

        if self._is_primary_key(column):
            return row_index

        col_type = column['type'].upper()
        if 'VARCHAR' in col_type or 'TEXT' in col_type:
            if 'email' in col_name:
                return self.faker.email()
            elif 'first_name' in col_name:
                return self.faker.first_name()
            elif 'last_name' in col_name:
                return self.faker.last_name()
            elif 'name' in col_name:
                return self.faker.name()
            else:
                return self.faker.bs()
        elif 'DECIMAL' in col_type or 'NUMERIC' in col_type:
            return round(self.faker.pyfloat(left_digits=4, right_digits=2, positive=True), 2)
        elif 'INT' in col_type or 'BIGINT' in col_type or 'SERIAL' in col_type:
            return self.faker.random_int(min=1, max=100)
        elif 'DATE' in col_type:
            return self.faker.date_this_year()
        elif 'TIMESTAMP' in col_type:
            return self.faker.iso8601()
        else:
            return None

    def _is_primary_key(self, column):
        return 'PRIMARY KEY' in column['constraints'].upper()

    def _topological_sort(self):
        in_degree = {u: 0 for u in self.tables}
        graph = {u: [] for u in self.tables}

        for u in self.tables:
            for fk in self.tables[u]['foreign_keys']:
                v = fk['references_table']
                if v in self.tables:
                    graph[v].append(u)
                    in_degree[u] += 1

        queue = [u for u in self.tables if in_degree[u] == 0]
        sorted_list = []

        while queue:
            u = queue.pop(0)
            sorted_list.append(u)
            for v in graph[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

        if len(sorted_list) != len(self.tables):
            raise Exception("Circular dependency detected in schema")

        return sorted_list
