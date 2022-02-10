import os
from PIL import Image
import string    
import random
import math

# specify the img directory path
images = []
path = "data/images/"

# list files in img directory
files = os.listdir(path)

for file in files:
    # make sure file is an image
    if file.endswith(('.jpg', '.png', 'jpeg')):
        img_path = path + file
        images.append(Image.open(img_path))


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


### my implementation
def create_random_sized_array(nr_of_images=4):
    if nr_of_images > len(images):
        print("error occured: number of images chosen", nr_of_images, "total available images in folder", len(images))

    array_size = []
    images_left = nr_of_images
    for items in range(images_left):
        if images_left > 0:
            number = random.randint(0, round(images_left))
            if(number > 0):
                array_size.append(number)
                images_left -= number

    if sum(array_size)==nr_of_images:
        # if we get correct amount of images that user asked for then we return 
        return array_size
    else:
        # if the array length does NOT match the amount user wanted then we need to re-run it
        create_random_sized_array(nr_of_images)

def generate_files_into_array(n_items):
    output_array = []
    random_sized_array = create_random_sized_array(n_items)
    for to_be_generated in random_sized_array:
        sample_list = random.sample(images, k=to_be_generated)
        output_array.append(sample_list)
    return output_array


def generate_output_file_name(number_char=15):
    ran = ''.join(random.choices(string.ascii_lowercase + string.digits, k = number_char))    
    return str("data/output/"+ran+".jpg")

# choose how many pictures to use
number_of_pic_to_use = 0 ##change here, otherwise we will ask in terminal
if(number_of_pic_to_use == 0):
    number_of_pic_to_use = int(input("Enter how many images you want to use:"))
output_array = generate_files_into_array(number_of_pic_to_use)

# Output array to randomly named file
get_concat_tile_resize(output_array).save(generate_output_file_name())
print("Output file has been created under data/output")
