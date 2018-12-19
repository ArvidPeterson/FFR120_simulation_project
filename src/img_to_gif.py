import os
import imageio

png_directory_path = 'save_data/img_to_gif/'  # TODO: MAKE SURE THIS DIRECTORIES EXIST!
gif_directory_path = 'save_data/img_to_gif/gif/'

files = os.listdir(png_directory_path)
files.sort()
print(files)
file_name = 'simulation.gif'
image_list = []

for file in files:
    if file.endswith('png'):
        file_full_path = png_directory_path + file
        image_list.append(imageio.imread(file_full_path))

imageio.mimsave(gif_directory_path + file_name, image_list, duration=1)
