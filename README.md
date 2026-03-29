# Test Data Generator

An independent agent that generates realistic test data based on an SQL schema file. This agent now supports H2, MySQL, and PostgreSQL dialects.

## Features

*   Parses SQL schema files (`CREATE TABLE` statements) for H2, MySQL, and PostgreSQL.
*   Generates realistic data for various SQL data types using the Faker library.
*   Outputs the generated data as both SQL `INSERT` statements and an Excel file.

## Usage

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the agent:**
    ```bash
    python src/main.py <path_to_your_schema.sql> --db-type <h2|mysql|postgres> [--rows <number_of_rows>]
    ```

    **Arguments:**
    *   `schema_file`: Path to your SQL schema file.
    *   `--db-type`: The dialect of your SQL schema. (default: `h2`)
    *   `--rows`: The number of rows to generate per table. (default: `10`)

3.  **Run the demo script:**

    You can also use the provided runner script to generate data for the sample schemas:
    ```bash
    ./run.sh
    ```

    This will generate the following files:
    *   `sample_schema_data.sql` and `sample_schema_data.xlsx` (for H2)
    *   `sample_schema_mysql_data.sql` and `sample_schema_mysql_data.xlsx` (for MySQL)
    *   `sample_schema_postgres_data.sql` and `sample_schema_postgres_data.xlsx` (for PostgreSQL)
