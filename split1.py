import os

from PIL import Image

def divide_image(image_path, num_rows, num_columns):
    # Load the image
    image = Image.open(image_path)
    
    # Get the width and height of the image
    width, height = image.size

    # Calculate the height and width of each question section
    question_height = height // num_rows
    question_width = width // num_columns

    # Create a directory to store the divided question images
    
    output_dir = 'public/Extracted_Images'
    os.makedirs(output_dir, exist_ok=True)
    nem = 1
    images_list = []



    # Divide the image and save each question section
    for i in range(num_rows):
        for j in range(num_columns):
            # Calculate the coordinates of the question section
            top = i * question_height
            bottom = top + question_height
            left = j * question_width
            right = left + question_width

            # Crop the image to get the question section
            question_image = image.crop((left, top, right, bottom))
            images_list.append(f"{output_dir}/question{nem}.jpg")


            # Save the question section as a separate image
            question_image.save(f"{output_dir}/question{nem}.jpg")
            nem += 1

    print("Image divided into questions successfully.")
    return images_list


