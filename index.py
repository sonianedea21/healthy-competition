import os
import PyPDF2
from openai import OpenAI

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the folder containing the test files
folder_path = os.path.join(current_dir, "test_files")

# Initialize the OpenAI client
client = OpenAI()

# Initialize a counter for numbering the outputs
COUNTER = 1

PROMPT = "Output ONLY the name of the person this results file is about"

# Iterate through all files in the folder
for file_name in os.listdir(folder_path):
    if file_name.startswith("."):  # Skip hidden files
        continue

    file_path = os.path.join(folder_path, file_name)

    # Read the contents of the file
    if file_name.endswith(".pdf"):
        # Extract text from PDF file

        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            TEXT = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                TEXT += page.extract_text()

    else:
        # For non-PDF files, read the contents as TEXT
        with open(file_path, "r") as file:
            TEXT = file.read()

    # Use OpenAI to find the name of the person in the TEXT
    COMPLETION = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": TEXT},
            {"role": "user", "content": PROMPT}
        ]
    )

    # Get the name of the person from the COMPLETION output
    person_name = COMPLETION.choices[0].message.content  # Assuming the AI outputs the person's name

    # Output the file name and the person's name
    print(f"{COUNTER}. {person_name}")

    # Increment the COUNTER for the next output
    COUNTER += 1