import PyPDF2 as pdf  # PyMuPDF
import re
import os


def extract_numbers_from_pdf(pdf_path):
    # Open the PDF file
    reader = pdf.PdfReader(pdf_path)
    extracted_numbers = []

    # Regex pattern to find 5-digit numbers starting with 6
    # pattern = re.compile(r'\b6\d{4}\b')
    
    pattern = re.compile(r'\b\d+\b')


    # Iterate through each page
    for page_num in range(102):
        page = reader.pages[page_num]
        text = page.extract_text()

        # Find all matching patterns
        matches = pattern.findall(text)
        # Convert matches to integers and filter out those greater than 62000
        for match in matches:
            number = int(match)
            if number > 62000:
                extracted_numbers.append(number)

    return extracted_numbers

def write_numbers_to_file(numbers, file_path):
    with open(file_path, 'w') as file:
        for number in numbers:
            file.write(f"{number}\n")


# Paths 
pdf_path = os.path.join(os.path.dirname(__file__), 'NIT_cutoff.pdf')
output_file_path = os.path.join(os.path.dirname(__file__), 'ranks.txt')
filter_output_file_path = os.path.join(os.path.dirname(__file__), 'filter_ranks.txt')

# Path to your PDF file
numbers = extract_numbers_from_pdf(pdf_path)
print("Extracted numbers:", numbers)

# Write numbers to file
write_numbers_to_file(numbers, output_file_path)
print(f"Numbers have been written to {output_file_path}")

dictionary = {
    "60-70" : [],
    "70-80" : [],
    "80-90" : [],
    "90-100" : [],
    "100-150" : [],
    "150-200" : [],
    ">200" : [],
}

for i in numbers:
    if i < 70_000:
        dictionary["60-70"].append(i)
    elif i < 80_000:
        dictionary["70-80"].append(i)
    elif i < 90_000:
        dictionary["80-90"].append(i)
    elif i < 100_000:
        dictionary["90-100"].append(i)
    elif i < 150_000:
        dictionary["100-150"].append(i)
    elif i < 200_000:
        dictionary["150-200"].append(i)
    else:
        dictionary[">200"].append(i)

# Printing the dictionary to a file in a table manner ; each keys as column and values as rows

def filtered_ranks_numbers_to_file(file_path):
    with open(file_path, 'w') as file:
        # Write the headers
        headers = dictionary.keys()
        file.write('\t'.join(headers) + '\n')

        # Write the rows
        max_length = max(len(values) for values in dictionary.values())
        for i in range(max_length):
            row = []
            for key in headers:
                if i < len(dictionary[key]):
                    row.append(str(dictionary[key][i]))
                else:
                    row.append('')
            file.write('\t'.join(row) + '\n')

filtered_ranks_numbers_to_file(filter_output_file_path)
print(f"Numbers have been written to {filter_output_file_path}")

