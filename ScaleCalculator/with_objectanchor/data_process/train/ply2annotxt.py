"""
Author: Tang zy
Date: Oct 2024
"""

# Process training data for seed
# According to pointnet2, ply is converted into three txt files according to the label, and a whole txt file
import os
import numpy as np
import plyfile


def makedir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def deal_ply(ply_folder):
    filenames = [f for f in os.listdir(ply_folder) if f.endswith('.ply')]
    for filename in filenames:
        plydata = plyfile.PlyData.read(os.path.join(ply_folder, filename))
        vertices = plydata['vertex'].data
        x = vertices['x']
        y = vertices['y']
        z = vertices['z']
        red = vertices['red']
        green = vertices['green']
        blue = vertices['blue']
        scalar_label = vertices['scalar_Constant']

        data = np.column_stack((x, y, z, red.astype(int), green.astype(int), blue.astype(int)))

        output_folder = filename.split('.')[0]
        out_path = os.path.join(txt_folder, output_folder)
        os.makedirs(out_path, exist_ok=True)
        out_file = os.path.join(out_path, '{}.txt'.format(output_folder))
        np.savetxt(out_file, data[:, :6], fmt='%.8f %.8f %.8f %d %d %d')

        data_1 = np.column_stack((x, y, z, red.astype(int),
                                green.astype(int), blue.astype(int), scalar_label.astype(int)))
        
        data_zeros = data_1[data_1[:, -1] == 0]
        data_ones = data_1[data_1[:, -1] == 1]
        data_twos = data_1[data_1[:, -1] == 2]

        out_clip = '{}_{}.txt'.format('clip', '1')
        out_one = '{}_{}.txt'.format('one', '1')
        out_two = '{}_{}.txt'.format('two', '1')

        annotations_path = os.path.join(out_path, 'annotations')
        os.makedirs(annotations_path, exist_ok=True)
        out_clip_path = os.path.join(annotations_path, out_clip)
        out_one_path = os.path.join(annotations_path, out_one)
        out_two_path = os.path.join(annotations_path, out_two)

        np.savetxt(out_clip_path, data_zeros[:, :6], fmt='%.8f %.8f %.8f %d %d %d')
        np.savetxt(out_one_path, data_ones[:, :6], fmt='%.8f %.8f %.8f %d %d %d')
        np.savetxt(out_two_path, data_twos[:, :6], fmt='%.8f %.8f %.8f %d %d %d')
        
if __name__ == '__main__':
        
    ply_folder = '/media/xujx/Elements/OSTRA_POISE/seed/label_plane'
    txt_folder = '/media/xujx/6AE0580BE057DC3F/2023_POISE/seed/Area_1'
    makedir(txt_folder)
    deal_ply(ply_folder)
    
