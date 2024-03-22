import xml.etree.ElementTree as ET
import csv
import sys
import os

def convert_xml_to_csv(xml_file_path, csv_file_path=None):
    # Check if the XML file exists and is a file
    if not os.path.exists(xml_file_path) or not os.path.isfile(xml_file_path):
        print(f"Error: The file '{xml_file_path}' does not exist or is not a file.")
        return

    # Parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # If no CSV file path is provided, create one in the same location as the XML file
    if csv_file_path is None:
        csv_file_path = os.path.splitext(xml_file_path)[0] + '.csv'

    # Determine all possible columns from the XML file
    columns = set()
    for item in root:
        # Add attributes as columns
        columns.update(item.attrib.keys())
        # Add sub-elements as columns
        for child in item:
            columns.add(child.tag)

    # Convert columns set to list and sort to maintain order
    columns = sorted(list(columns))

    # Open a new CSV file for writing
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        # Write the headers (columns names)
        writer.writerow(['Sequence'] + columns)
        
        sequence_number = 1  # Initialize sequence number
        # Iterate over each item in the XML
        for item in root:
            row_data = [sequence_number]
            # For each column, get the attribute or sub-element's text or empty string if not present
            for col in columns:
                if col in item.attrib:
                    row_data.append(item.attrib[col])
                else:
                    child = item.find(col)
                    row_data.append(child.text if child is not None else '')
            writer.writerow(row_data)
            sequence_number += 1  # Increment the sequence number for the next row

if __name__ == '__main__':
    # Check if the XML file path is provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python script.py path_to_xml_file [path_to_csv_file]")
        sys.exit(1)
    
    # Extract the XML file path from the command-line arguments
    xml_file_path = sys.argv[1]
    
    # Extract the CSV file path if provided, else default to None
    csv_file_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Run the conversion
    convert_xml_to_csv(xml_file_path, csv_file_path)

