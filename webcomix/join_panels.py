import os
import shutil
import tempfile
import itertools
from PIL import Image
from PIL import ImageOps

"""
Code below to join panels based off this superb response. Give that dev some love.
https://stackoverflow.com/questions/64981226/how-to-concatenate-5-images-out-of-multiple-images-in-a-folder
"""

def join_panels():
    directory = self.name
    dirlist = os.listdir(directory)
    for fname in dirList:

def create_temp_directory(name):
    """
    temporary storage whilst we join panels into pages
    """
    temp_dir = tempfile.TemporaryDirectory(suffix=None, prefix=f'temp_directory_{name}', dir=None)
    return temp_dir


def divide_list_into_chunks(input_list, len_of_chunk):
    """
    Group panels from strip into chunks
    """
    for i in range(0, len(input_list), len_of_chunk):
       yield input_list[i:i + len_of_chunk]
 

def merge_images_horizontally(list_of_images, file_name):
    """
    join the comic panels into a strip
    :param list_of_images: current list of images to process
    :param file_name: file name for the new image
    :return: 
    """
    # open images using Pillow
    images = [Image.open(im) for im in list_of_images]
    # Create separate lists to store the heights and widths
    # of the images
    widths, heights = zip(*(i.size for i in images))
    width_of_new_image = min(widths)
    height_of_new_image = sum(heights)
    # create a new output image
    new_im = Image.new('RGB', (width_of_new_image, height_of_new_image))
    new_pos = 0
    counter = 0
    for im in images:
       if counter == 0:
          new_im.paste(im, (0, new_pos))
          new_pos += im.size[1]
          counter += 1
       else:
          color = "black"
          border = (0, 10, 0, 0)
          img_with_border = ImageOps.expand(im, border=border, fill=color)
          new_im.paste(img_with_border, (0, new_pos))
          new_pos += im.size[1]
     new_im.save(f'{file_name}', "JPEG", quality=75, optimize=True, progressive=True)
     return


image_directory = "sample_images"
image_directory_abspath = os.path.abspath(image_directory)
images = os.listdir(image_directory_abspath)
accepted_extensions = ('.bmp', '.gif', '.jpg', '.jpeg', '.png', '.svg', '.tiff')
valid_image_extensions = [im for im in images if im.endswith(accepted_extensions)]
image_groups = [list(g) for _, g in itertools.groupby(sorted(valid_image_extensions), lambda x: x[0:2])]
for image_group in image_groups:
   count = 0
   name_group = image_group[0][:2]
   temp_directory = create_temp_directory(name_group)
   image_list = [shutil.copy(f'{image_directory_abspath}/{item}', f'{temp_directory.name}/{item}') for item in image_group]
   max_number_of_items = 5
   chunks = list(divide_list_into_chunks(image_list, max_number_of_items))
   for chunk in chunks:
      count += 1
      if len(chunk) == 5:
        merge_images_vertically(chunk, f'{name_group}_merged_{count}.jpeg')
      else:
        new_checks = add_blank_checks(chunk, temp_directory)
        merge_images_vertically(new_checks, f'{name_group}_merged_{count}.jpeg')