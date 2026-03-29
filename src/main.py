import argparse
import os
from sql_parser import SQLParser
from data_generator import DataGenerator
from output_writer import OutputWriter

def main():
    parser = argparse.ArgumentParser(description="Generate test data from an SQL schema.")
    parser.add_argument("schema_file", help="Path to the SQL schema file.")
    parser.add_argument("--db-type", type=str, default='h2', choices=['h2', 'mysql', 'postgres'], help="The type of database schema.")
    parser.add_argument("--rows", type=int, default=10, help="Number of rows to generate per table.")
    args = parser.parse_args()

    schema_file = args.schema_file
    db_type = args.db_type
    num_rows = args.rows

    if not os.path.exists(schema_file):
        print(f"Error: Schema file not found at {schema_file}")
        return

    print(f"Parsing {db_type} schema from {schema_file}...")
    sql_parser = SQLParser(schema_file, db_type)
    tables = sql_parser.parse_schema()

    if not tables:
        print("No tables found in the schema.")
        return

    print(f"Generating {num_rows} rows for {len(tables)} tables...")
    data_generator = DataGenerator(tables, db_type)
    generated_data = data_generator.generate_data(num_rows)

    output_writer = OutputWriter(generated_data)

    output_basename = os.path.splitext(os.path.basename(schema_file))[0]
    sql_output_file = f"{output_basename}_data.sql"
    excel_output_file = f"{output_basename}_data.xlsx"

    print(f"Writing SQL INSERT statements to {sql_output_file}...")
    output_writer.write_sql_inserts(sql_output_file)

    print(f"Writing data to Excel in {excel_output_file}...")
    output_writer.write_excel(excel_output_file)

    print("Done.")

if __name__ == "__main__":
    main()
