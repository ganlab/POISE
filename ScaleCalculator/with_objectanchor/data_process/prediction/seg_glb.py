"""
Author: Tang zy
Date: Oct 2024
"""

import pandas as pd
import numpy as np
import time
import os
import open3d as o3d

def seg(dir_path, df, threshold):
    root = os.path.join(dir_path, "seed")
    list = df.index.tolist()
    for folder in os.listdir(root):
        if folder in list:
            try:
                mesh_path = os.path.join(root, folder, "output", "texture_scene.obj")
                ply_path = os.path.join(root, folder, "output", "dense_scene.ply")
                folder_name = os.path.basename(folder)
                mesh = o3d.io.read_triangle_mesh(mesh_path, enable_post_processing=True, print_progress=True)
                ply = o3d.io.read_point_cloud(ply_path)
                vertices = np.asarray(mesh.vertices)
                plane_model, inliers = ply.segment_plane(distance_threshold=0.02, ransac_n=6, num_iterations=10000)
                [A, B, C, D] = plane_model
                distances = (A * vertices[:, 0] + B * vertices[:, 1] + C * vertices[:, 2] + D) / np.sqrt(
                    A ** 2 + B ** 2 + C ** 2)
                selected_indices = np.where(distances > threshold )[0]
                mesh.remove_vertices_by_index(selected_indices)

                print('read')
                scale_factor = df.loc[folder_name, 'ratio 1']
                # scale_factor_two = df.loc[folder_name, 'ratio 2']
                # scale_factor = (scale_factor_one + scale_factor_two) / 2
                mesh.scale(scale_factor, center=mesh.get_center())
                vis = o3d.visualization.Visualizer()
                vis.create_window()
                vis.add_geometry(mesh)
                vis.poll_events()
                vis.update_renderer()
                img_path = os.path.join(dir_path, "dis_file/seed_png")
                os.makedirs(img_path, exist_ok=True)
                image_path = os.path.join(img_path, "{}.png".format(folder_name))
                vis.capture_screen_image(image_path)
                time.sleep(2)
                vis.destroy_window()
                obj_path = os.path.join(root, folder, "output", 'texture_scene_0.obj')
                o3d.io.write_triangle_mesh(obj_path, mesh, write_vertex_normals=True, write_vertex_colors=True,
                                           write_triangle_uvs=True)
                print(folder_name + ' succeed...')
            except:
                print(folder_name + ' failed...')

if __name__ == '__main__':
    dir_path = "J:/2023_POISE/2023POISE_seed/pointnet2/test"
    csv_path = os.path.join(dir_path, "dis_file/dis.csv")
    df = pd.read_csv(csv_path, encoding='gbk', index_col='number')
    threshold = -0.04
    seg(dir_path, df, threshold)



