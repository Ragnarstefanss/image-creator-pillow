import os
from PIL import Image
import string    
import random
import math

# specify the img directory path
parent_folder = "data"
output_location = parent_folder+"/output/"

## add here folders if you have different folders you want to use
path_1 = parent_folder+"/images/"  # data/images
path_2 = "D:/change-this/"
paths = [path_1, path_2]

def append_images(all_paths, image_choices=1000):
    images = []
    for _path in all_paths:
        # When you have gigabytes of files to choose from then the program gets heavy quickly, 
        # so this is a solution to only pick 1000 random photos which will then also be chosen a random sample of in the final output
        files = []
        for _ in range(1, image_choices):
            files.append(random.choice(os.listdir(_path)))
        ##
        for file in files:
            # make sure file is an image
            if file.endswith(('.jpg', '.png', 'jpeg')):
                img_path = _path + file
                images.append(Image.open(img_path))
    return images

images = append_images(paths)


### Pillow code that is needed
#CODE FROM python-snippets/notebook/pillow_concat.py
## LINK: https://github.com/nkmk/python-snippets/blob/4e232ef06628025ef6d3c4ed7775f5f4e25ebe19/notebook/pillow_concat.py#L136-L142
def get_concat_h_multi_resize(im_list, resample=Image.BICUBIC):
    min_height = min(im.height for im in im_list)
    im_list_resize = [im.resize((int(im.width * min_height / im.height), min_height),resample=resample)
                      for im in im_list]
    total_width = sum(im.width for im in im_list_resize)
    dst = Image.new('RGB', (total_width, min_height))
    pos_x = 0
    for im in im_list_resize:
        dst.paste(im, (pos_x, 0))
        pos_x += im.width
    return dst

def get_concat_v_multi_resize(im_list, resample=Image.BICUBIC):
    min_width = min(im.width for im in im_list)
    im_list_resize = [im.resize((min_width, int(im.height * min_width / im.width)),resample=resample)
                      for im in im_list]
    total_height = sum(im.height for im in im_list_resize)
    dst = Image.new('RGB', (min_width, total_height))
    pos_y = 0
    for im in im_list_resize:
        dst.paste(im, (0, pos_y))
        pos_y += im.height
    return dst

def get_concat_tile_resize(im_list_2d, resample=Image.BICUBIC):
    im_list_v = [get_concat_h_multi_resize(im_list_h, resample=resample) for im_list_h in im_list_2d]
    return get_concat_v_multi_resize(im_list_v, resample=resample)


def create_array_size(rows=0, columns=0):
    temp_array_size = []
    if (rows == 0 or columns == 0):
        rows = int(input("Enter column size: "))
        columns = int(input("Enter row size: "))
    for item in range(0, columns):
        temp_array_size.append(rows)
    return temp_array_size

### my implementation
def create_random_sized_array():
    r1 = random.randint(1, 6)
    r2 = random.randint(2, 4)
    return create_array_size(rows=r1, columns=r2)


def generate_files_into_array(import_images = images, array_size=[]):
    output_array = []
    for to_be_generated in array_size:
        sample_list = random.sample(import_images, k=to_be_generated)
        output_array.append(sample_list)
    return output_array


def generate_output_file_name(number_char=15):
    ran = ''.join(random.choices(string.ascii_lowercase + string.digits, k = number_char))    
    return str(output_location+ran+".jpg")


def ask_randomized_size_question(answer=""):
    if(answer == ""):
        question = input("Do you want to create a random sized array ? (type yes or no): ")
    else:
        #if we are running a for loop we don't want to ask again and again so this is a simple solution to that problem
        question = answer
    question = question.lower()
    if question == "yes":
        array_size = create_random_sized_array()
    else:
        # calls with default so the user is asked what size of array he would like it to be
        array_size = create_array_size(0, 0)
    return array_size


def run_x_times(x_times=101, rows=4, columns=2, import_images=images, output_location=output_location):
    for _ in range(1, x_times):
        #array_size = ask_randomized_size_question(answer="yes")
        array_size = create_array_size(rows, columns)
        output_array = generate_files_into_array(import_images=import_images, array_size=array_size)
        
        # Output array to randomly named file
        number_of_char = 15
        ran = ''.join(random.choices(string.ascii_lowercase + string.digits, k = number_of_char))
        generated_output_file_name = str(output_location+ran+".jpg")
        get_concat_tile_resize(output_array).save(generated_output_file_name)
    print("Output file has been created under ", output_location)

#does not work at the moment
def run_random_size_x_times(x_times=101, import_images=images, output_location=output_location):
    for _ in range(1, x_times):
        r1 = random.randint(1, 6)
        r2 = random.randint(2, 4)
        run_x_times(x_times=1, rows=r1, columns=r2, import_images=import_images, output_location=output_location)
