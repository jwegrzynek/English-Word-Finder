import re


def process_file(input_file: str, output_file: str):
    # Define a regular expression pattern to match special characters
    special_chars_pattern = re.compile(r'[^a-zA-Z0-9\s]')

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Remove special characters and convert to lowercase
            cleaned_line = special_chars_pattern.sub('', line).lower()
            # Write the cleaned line to the output file
            outfile.write(cleaned_line)


process_file("words.txt", "clear_words.txt")
