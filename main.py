import sys
import os
from core import TestDataGenerator

if __name__ == '__main__':
    num_rows = 10
    if len(sys.argv) > 1:
        try:
            num_rows = int(sys.argv[1])
        except ValueError:
            print("Invalid number of rows provided. Using default (10).")

    # Get the directory of the main.py script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(script_dir, 'sample_schema.sql')
    output_sql_path = os.path.join(script_dir, f'test_data_{num_rows}.sql')
    output_excel_path = os.path.join(script_dir, f'test_data_{num_rows}.xlsx')

    generator = TestDataGenerator(schema_path)
    generator.generate_test_data(num_rows=num_rows)
    generator.write_to_sql_file(output_sql_path)
    generator.write_to_excel_file(output_excel_path)
