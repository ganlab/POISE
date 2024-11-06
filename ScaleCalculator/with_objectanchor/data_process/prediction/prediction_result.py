
"""
Author: Tang zy
Date: Oct 2024
"""

import os
import glob
import numpy as np


def add_prediction(plant, label):
    data = np.loadtxt(plant)
    labels = np.loadtxt(label)
    data = np.column_stack((data, labels))
    return data

def no_green(data):
    xyz = data[:, :3]
    rgb_colors = data[:, 3:6]
    labels = data[:, 6]

    green_range = [(50, 150), (0, 255), (0, 50)]
    is_in_green_range = np.logical_and(np.logical_and(rgb_colors[:, 0] >= green_range[0][0], rgb_colors[:, 0] <= green_range[0][1]),
                                    np.logical_and(rgb_colors[:, 1] >= green_range[1][0], rgb_colors[:, 1] <= green_range[1][1]),
                                    np.logical_and(rgb_colors[:, 2] >= green_range[2][0], rgb_colors[:, 2] <= green_range[2][1]))

    xyz = xyz[~is_in_green_range]
    rgb_colors = rgb_colors[~is_in_green_range]
    labels = labels[~is_in_green_range]
    data_without_green = np.column_stack((xyz, rgb_colors, labels))
    return data_without_green
   
def makedir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def prediction_result(dir_path, result_folder):
    plane_folder = os.path.join(dir_path, "plane")
    plane_files = glob.glob(os.path.join(plane_folder, "*.txt"))
    result_path = os.path.join(dir_path, "PN_result")
    makedir(result_path)
    out_path = os.path.join(dir_path, "no_green")
    makedir(out_path)

    for plane in plane_files:
        filename = os.path.basename(plane)
        print(filename)
        label_file = os.path.join(result_folder, "Area_5_" + filename)
        result_data = add_prediction(plane, label_file)
        # result_out_path = os.path.join(result_path, filename)
        # np.savetxt(result_out_path, result_data, fmt='%.8f %.8f %.8f %d %d %d %d')
        condition = result_data[:, -1] != 2
        anchor_data = result_data[condition]
        no_green_data = no_green(anchor_data)
        out_nogreen_path = os.path.join(out_path, filename)
        np.savetxt(out_nogreen_path, no_green_data, fmt='%.8f %.8f %.8f %d %d %d %d')

if __name__ == '__main__':
    
    dir_path = "J:/2023_POISE/2023POISE_seed/pointnet2/test/"
    result_folder = "J:/2023_POISE/2023POISE_seed/pointnet2/log/sem_seg/2023_seed/visual"
    prediction_result(dir_path,result_folder)


        