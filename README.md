# Test Data Generator

This agent generates realistic test data based on an SQL schema file.

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

To generate test data, run the `main.py` script:

```bash
python main.py
```

By default, this will generate 10 rows of data for each table in the `sample_schema.sql` file and write the output to `test-data-generator/test_data.sql`.

To customize the number of rows, you can modify the `num_rows` parameter in `main.py`.
