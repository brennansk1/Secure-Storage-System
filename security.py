# security_testing.py

import subprocess
import os
from datetime import datetime
from fpdf import FPDF

# DEBUG flag to control printing of Bandit output to the console
DEBUG = True  # Set to False to disable Bandit output prints

def run_bandit(file_path):
    """
    Runs Bandit on the specified file and returns the raw output.
    """
    try:
        # Run Bandit with JSON output and capture both stdout and stderr
        result = subprocess.run(
            ['bandit', '-r', file_path],
            capture_output=True,
            text=True,
            check=False  # Allows Bandit to return even if issues are found
        )

        # Print Bandit's stdout and stderr when DEBUG is enabled
        if DEBUG:
            print("\n=== Bandit Output ===")
            print(result.stdout)  # Bandit's standard output
            if result.stderr:  # Print stderr if there are any errors or warnings
                print("=== Bandit Errors/Warnings ===")
                print(result.stderr)
            print("======================\n")

        # Handle the exit codes and give meaningful output
        if result.returncode == 0:
            print("Bandit scan completed successfully. No issues found.")
        elif result.returncode == 1:
            print("Bandit scan completed with issues found.")
        else:
            print("Error running Bandit:")
            print(result.stderr)
            return False, result.stdout + result.stderr

    except Exception as e:
        print(f"An unexpected error occurred while running Bandit: {e}")
        return False, ""

    # Return both stdout and stderr combined as raw output
    return True, result.stdout + result.stderr

def generate_pdf(raw_output, file_name, output_folder):
    """
    Generates a PDF report with all Bandit output.
    """
    # Initialize PDF
    pdf = FPDF()
    pdf.add_page()

    # Set title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Bandit Security Scan Report", ln=True, align='C')

    # Add file name and timestamp
    pdf.set_font("Arial", size=12)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(0, 10, f"File Scanned: {file_name}", ln=True)
    pdf.cell(0, 10, f"Scan Timestamp: {timestamp}", ln=True)

    # Add a line break
    pdf.ln(10)

    # Add Bandit raw output
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, raw_output)  # Add all raw Bandit output to the PDF

    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
            print(f"Created output folder at: {output_folder}")
        except Exception as e:
            print(f"Error creating output folder: {e}")
            return

    # Save PDF with the desired naming convention
    timestamp_pdf = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.splitext(os.path.basename(file_name))[0]
    pdf_file_name = f"{base_name}_Bandit_test_{timestamp_pdf}.pdf"
    pdf_path = os.path.join(output_folder, pdf_file_name)
    pdf.output(pdf_path)
    print(f"PDF report generated: {pdf_path}")

def main():
    # Hardcoded file path to scan
    file_path = 'config.py'  # Change this to the specific file you want to scan

    # Hardcoded output folder path for the PDF report
    output_folder = 'security_testing'  # Change this to your desired output folder

    # Validate the file path
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return

    # Run Bandit and capture the output
    success, raw_output = run_bandit(file_path)
    if not success:
        return

    # Generate PDF report with all Bandit output
    generate_pdf(raw_output, file_path, output_folder)

if __name__ == "__main__":
    main()
