import main

path_1 = "C:/change-this-1/"
path_2 = "C:/change-this-2/"
path_3 = "C:/change-this-3/"
all_paths = [path_1, path_2, path_3]

#running
images = main.append_images(all_paths, image_choices=1000)

main.run_x_times(x_times=100, rows=3, columns=2, import_images=images, output_location="data/output/")
