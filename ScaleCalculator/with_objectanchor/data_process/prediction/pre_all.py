"""
Author: Tang zy
Date: Oct 2024
"""
import numpy as np
import os

def process_txt_to_npy(txt_path, out_path, area_prefix='Area_5'):
    """Processes .txt files in the given path and saves as .npy files in the output path."""
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    for filename in os.listdir(txt_path):
        file_id = filename.split('.')[0]
        data = np.loadtxt(os.path.join(txt_path, filename))
        data1 = add_zero_column(data)
        save_npy_file(data1, file_id, out_path, area_prefix)


def add_zero_column(data):
    """Adds a zero column to the data."""
    zero = np.zeros(data.shape[0]).reshape(-1, 1)
    return np.concatenate([data, zero], axis=1)


def save_npy_file(data, file_id, out_path, area_prefix):
    """Adjusts the xyz coordinates and saves the data as an .npy file."""
    points_list = [data]
    data_label = np.concatenate(points_list, 0)

    xyz_min = np.amin(data_label, axis=0)[0:3]
    data_label[:, 0:3] -= xyz_min

    out_file = f'{area_prefix}_{file_id}.npy'
    out_folder = os.path.join(out_path, out_file)
    np.set_printoptions(suppress=True)
    np.save(out_folder, data_label)


if __name__ == "__main__":
    txt_path = 'E:/2023_POISE/seed/pred/plane'
    out_path = 'E:/2023_POISE/seed/pred/npy'
    process_txt_to_npy(txt_path, out_path)


