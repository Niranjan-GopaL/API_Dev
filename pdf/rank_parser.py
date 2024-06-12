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




# I WANT TO EXTRACT EACH LINE IN THE PDF FILE ;
    # maybe split entire text according to \n delimeter so that we have a  list of LINES ; the problem is I DON'T KNOW IF there will be \n in the pdf extract text()
    # ALL LINES will have 2 numbers in the end <--- this is the BEST WAY TO CLASSIFY the entire text in pdf as LINES 
# 
# 1. EACH line MUST HAVE the word "OS" in it ; otherwise don't include it in the list
# 2. WE NEED ALL NUMBERS whose LINE has the word "Female" in one list [FIRST PRIORITY] ; all the other numbers in another list [SECOND PRIORITY] ;

""" THIS IS HOW EACH LINE OF PDF LOOKS LIKE
National Institute of Technology, Kurukshetra Production and Industrial Engineering (4 Years, Bachelor of Technology) OS ST Gender-Neutral 2766 2923
National Institute of Technology, Kurukshetra Production and Industrial Engineering (4 Years, Bachelor of Technology) OS ST Female-only (including Supernumerary) 3805 3805
National Institute of Technology, Manipur Civil Engineering (4 Years, Bachelor of Technology) HS OPEN Gender-Neutral 108496 208858
National Institute of Technology, Manipur Civil Engineering (4 Years, Bachelor of Technology) HS OPEN Female-only (including Supernumerary) 188427 188427
National Institute of Technology, Rourkela Bio Technology (4 Years, Bachelor of Technology) OS OBC-NCL Female-only (including Supernumerary) 18954 18954
National Institute of Technology, Rourkela Bio Technology (4 Years, Bachelor of Technology) OS SC Gender-Neutral 5815 6639
National Institute of Technology, Rourkela Bio Technology (4 Years, Bachelor of Technology) OS SC Female-only (including Supernumerary) 5361 5361
National Institute of Technology, Rourkela Bio Technology (4 Years, Bachelor of Technology) OS ST Gender-Neutral 612 612
National Institute of Technology, Rourkela Ceramic Engineering (4 Years, Bachelor of Technology) HS OPEN Gender-Neutral 45990 57029
National Institute of Technology, Rourkela Ceramic Engineering (4 Years, Bachelor of Technology) HS OPEN Female-only (including Supernumerary) 52956 53962
"""