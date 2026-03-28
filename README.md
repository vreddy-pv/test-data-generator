# Test Data Generator

This is a Python-based agent that generates realistic test data from an SQL schema file. It is designed to be an independent tool that can be used with any project that requires a database.

## Features

-   **Independent and Adaptable**: The agent is not tied to any specific project and can be used with any SQL schema.
-   **Realistic Data**: Uses the `Faker` library to generate realistic data for a variety of data types.
-   **SQL Schema Parsing**: Parses `CREATE TABLE` statements from a `.sql` file to understand the database structure.
-   **H2 Database Support**: The initial version is designed to work with H2 database syntax.
-   **Foreign Key Awareness**: Has a basic understanding of foreign key relationships to generate consistent data.
-   **Customizable**: Allows you to specify the number of rows to generate.
-   **Excel Output**: Generates an Excel file with each table on a separate sheet.

## Setup

1.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    ```

2.  **Activate the virtual environment:**
    -   **Windows:**
        ```bash
        .venv\Scripts\activate
        ```
    -   **macOS/Linux:**
        ```bash
        source .venv/bin/activate
        ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To generate test data, you can use the `run.sh` script in the `scripts` directory:

```bash
./scripts/run.sh [number_of_rows]
```

-   `[number_of_rows]` is an optional argument to specify the number of rows to generate for each table. If not provided, it defaults to 10.

This will generate a SQL file named `test_data_[number_of_rows].sql` and an Excel file named `test_data_[number_of_rows].xlsx` in the `test-data-generator` directory, which you can then use to populate your database or for other testing purposes.

## How It Works

1.  **Schema Parsing**: The agent reads the `sample_schema.sql` file (or any other provided schema file) and uses the `sqlparse` library to parse the `CREATE TABLE` statements.
2.  **Data Generation**: It then uses the `Faker` library to generate data for each column based on its data type.
3.  **SQL Output**: Finally, it writes the generated data as a series of `INSERT` statements to a `.sql` file.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them with descriptive messages.
4.  Push your changes to your fork.
5.  Create a pull request.

### Future Enhancements

-   Add support for other SQL dialects (e.g., PostgreSQL, MySQL, SQLite).
-   Improve foreign key handling to support more complex relationships.
-   Add more sophisticated data generation options.
