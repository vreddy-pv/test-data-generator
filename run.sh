#!/bin/bash

# This script installs the necessary dependencies and runs the test data generator
# with the sample SQL schemas for H2, MySQL, and PostgreSQL.

# Install dependencies
pip install -r requirements.txt

# Run the data generator for each database type

echo "Generating data for H2..."
python src/main.py sample_schema.sql --db-type h2

echo "\nGenerating data for MySQL..."
python src/main.py sample_schema_mysql.sql --db-type mysql

echo "\nGenerating data for PostgreSQL..."
python src/main.py sample_schema_postgres.sql --db-type postgres

echo "\nDone."
