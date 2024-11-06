"""
Author: Tang zy
Date: Oct 2024
"""

import os

def convert_ply_to_obj(input_ply):
    """
    Convert a PLY file to an OBJ file using CloudCompare.

    Parameters:
        input_ply (str): Path to the input PLY file.
        output_obj (str): Path to the output OBJ file.
    """

    converter = "cd /d D:/BaiduNetdiskDownload/CloudCompare/CloudCompare"
    converter = converter + "&&"
    converter = converter + "CloudCompare.exe -SILENT -M_EXPORT_FMT OBJ -O "
    converter = converter + input_ply
    converter = converter + " -NO_TIMESTAMP -SAVE_MESHES"
    os.system(converter)

if __name__ == '__main__':

    root = 'E:/2023_POISE/seed/'
    for folder in os.listdir(root):
        try:
            ply_path = os.path.join(root, folder, "output", "texture_scene.ply")
            convert_ply_to_obj(ply_path)
        except:
            print('failed')
