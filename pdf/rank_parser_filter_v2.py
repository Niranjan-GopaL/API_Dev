# I WANT TO EXTRACT EACH LINE IN THE PDF FILE ;
    # maybe split entire text according to \n delimeter so that we have a  list of LINES ; the problem is I DON'T KNOW IF there will be \n in the pdf extract text()
    # ALL LINES will have 2 numbers in the end <--- this is the BEST WAY TO CLASSIFY the entire text in pdf as LINES 
# 
# 1. EACH line MUST HAVE the word "OS" in it ; otherwise don't include it in the list
# 2. WE NEED ALL NUMBERS whose LINE has the word "Female" in one list [FIRST PRIORITY] ; all the other numbers in another list [SECOND PRIORITY] ;

""" THIS IS HOW EACH LINE OF PDF NEED TO LOOK LIKE
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

import PyPDF2 as pdf  # PyMuPDF
import re
import os


# pdf_path = os.path.join(os.path.dirname(__file__), 'NIT_cutoff.pdf')
# reader = pdf.PdfReader(pdf_path)
# page = reader.pages[0]
# text = page.extract_text()
# print(text)
# print("\n---------------------------------------------\n\n\n",text.split("\n"))


def extract_numbers_from_pdf(pdf_path):
    reader = pdf.PdfReader(pdf_path)
    female_numbers  = []
    other_numbers = []

    for page_num in range(102):
        page = reader.pages[page_num]
        text = page.extract_text()
        lines = text.split('\n')  

        for line in lines:
            if "OS" in line:
                numbers = re.findall(r'\b\d+\b', line)  
                numbers = [int(num) for num in numbers if int(num) > 55_000]
                if numbers:
                    if "Female" in line:
                        female_numbers.extend(numbers)
                    else:
                        other_numbers.extend(numbers)
    return female_numbers, other_numbers


def write_numbers_to_file(female_numbers, other_numbers, file_path):

    def categorize(numbers):
        dictionary = { "55-60":[], "60-70": [], "70-80": [], "80-90": [], "90-100": [], "100-150": [], "150-200": [], ">200": [], }
        
        for i in numbers:
            if i < 60_000:
                dictionary["55-60"].append(i)
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
        return dictionary

    dict_first_priority = categorize(female_numbers)
    dict_second_priority = categorize(other_numbers)

    with open(file_path, 'a') as file:
        headers = dict_first_priority.keys()
        file.write('\t'.join(headers) + '\n')

        max_length = max(len(values) for values in dict_first_priority.values())
        for i in range(max_length):
            row = []
            for key in headers:
                if i < len(dict_first_priority[key]):
                    row.append(str(dict_first_priority[key][i]))
                else:
                    row.append('')
            file.write('\t'.join(row) + '\n')


        with open(file_path, 'a') as file:
            headers = dict_second_priority.keys()
            file.write('\t'.join(headers) + '\n')

            max_length = max(len(values) for values in dict_second_priority.values())
            for i in range(max_length):
                row = []
                for key in headers:
                    if i < len(dict_second_priority[key]):
                        row.append(str(dict_second_priority[key][i]))
                    else:
                        row.append('')
                file.write('\t'.join(row) + '\n')



pdf_path = os.path.join(os.path.dirname(__file__), 'NIT_cutoff.pdf')
output_file_path = os.path.join(os.path.dirname(__file__), 'ranks_finer_v2.txt')

female_numbers, other_numbers = extract_numbers_from_pdf(pdf_path)
print("Female numbers :", female_numbers)
print("Other numbers  :", other_numbers)

write_numbers_to_file(female_numbers, other_numbers, output_file_path)
print(f"Numbers have been written to {output_file_path}")