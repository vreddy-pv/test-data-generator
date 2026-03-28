import sys
import os
import subprocess

# Get the number of rows from the command-line arguments
if len(sys.argv) > 1:
    num_rows = sys.argv[1]
else:
    # If no argument is provided, ask the user
    try:
        num_rows = input("Enter the number of rows to generate (default: 10): ")
        if not num_rows:
            num_rows = "10"
    except EOFError:
        num_rows = "10"

# Construct the absolute path to the run.sh script
# The skill script is in .claude/skills, so we need to go up two directories
skill_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(skill_dir, '..', '..'))
run_script_path = os.path.join(project_root, 'scripts', 'run.sh')

# Execute the run.sh script
print(f"Executing: {run_script_path} {num_rows}")

# We need to run this from the project root for the paths in the script to work correctly
process = subprocess.run(
    ["bash", run_script_path, num_rows],
    cwd=project_root,
    capture_output=True,
    text=True
)

# Print the output
print("--- stdout ---")
print(process.stdout)
if process.stderr:
    print("--- stderr ---")
    print(process.stderr)

# Verify that the output files were created
sql_file = os.path.join(project_root, f'test_data_{num_rows}.sql')
excel_file = os.path.join(project_root, f'test_data_{num_rows}.xlsx')

print("\n--- Verification ---")
if os.path.exists(sql_file):
    print(f"SUCCESS: SQL file created at {sql_file}")
else:
    print(f"FAILURE: SQL file not found at {sql_file}")

if os.path.exists(excel_file):
    print(f"SUCCESS: Excel file created at {excel_file}")
else:
    print(f"FAILURE: Excel file not found at {excel_file}")
