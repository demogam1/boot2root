import tarfile
import re
import os

# Define the path to extract the contents
file_path = 'fun'  # Update with the path to your tar file
extracted_path = 'extracted_files'
output_file_path = 'extracted_source_code.c'

# Extract the tar file
with tarfile.open(file_path, 'r:*') as tar:
    tar.extractall(path=extracted_path)

# Function to read raw content of a pcap file
def read_raw_pcap(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    return raw_data

# Function to search for file comments in a pcap file and return the content
def search_file_comments(raw_data):
    pattern = re.compile(r'//file(\d+)', re.MULTILINE)
    matches = pattern.findall(raw_data)
    return matches

# Read and concatenate the contents of all extracted files for a comprehensive search
def get_file_comments_from_pcaps(pcap_files_list):
    file_comments = {}
    for pcap_file in pcap_files_list:
        raw_data = read_raw_pcap(pcap_file)
        ascii_representation = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in raw_data)
        comments = search_file_comments(ascii_representation)
        for comment in comments:
            file_comments[int(comment)] = ascii_representation
    
    return file_comments

# List all pcap files in the extracted directory
extracted_files_list = []
for root, dirs, files in os.walk(extracted_path):
    for file in files:
        if file.endswith(".pcap"):
            extracted_files_list.append(os.path.join(root, file))

# Search for file comments in all pcap files
file_comments = get_file_comments_from_pcaps(extracted_files_list)

# Sort comments by their sequence number and combine their contents
sorted_comments = dict(sorted(file_comments.items()))
combined_content = '\n'.join(sorted_comments.values())

# Save the combined content to a file
with open(output_file_path, 'w') as output_file:
    output_file.write(combined_content)

print(f"The extracted source code has been saved to {output_file_path}")

