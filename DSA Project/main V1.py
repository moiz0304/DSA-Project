''' 
Currently this code is sending pictures to the LLM (BARD) and getting their descriptions, then storing those descriptions in a
CSV file whilst ensuring that no image or its description is repeated.
'''
# problems with this code:
# 1. The formatting of the description can differ, can go onto the next line which will mess CSV writing functionality
from bardapi import Bard
from bardapi import BardCookies
from keys import cookie_dict
import csv

# Initialize Bard and LinkedList to store image names
bard = BardCookies(cookie_dict=cookie_dict)
image_names_set = set()  # Use a set to store unique image names

# Open the CSV file for reading and writing
with open('data/data.csv', 'a', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Load existing image names into the set
    try:
        with open('data/data.csv', 'r') as existing_csv:
            reader = csv.reader(existing_csv)
            for row in reader:
                image_names_set.add(row[0])  # Assuming image names are in the first column
    except FileNotFoundError:
        pass  # If the file doesn't exist, ignore the exception

    # Provide the image file path
    image_path = 'pic13.jpg'

    # Read the image content
    image = open(image_path, 'rb').read()

    # Ask Bard for a description
    bard_answer = bard.ask_about_image('Give a one-line Image Description in English', image)
    description = bard_answer['content']

    # Check if the image name is not in the set
    if image_path not in image_names_set:
        # Store the image name and description in the CSV file
        csv_writer.writerow([image_path, description])
        image_names_set.add(image_path)

    print(description)