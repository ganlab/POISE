"""
Author: Tang zy
Date: Oct 2024
"""

import open3d as o3d
import os

def plane(input_path, out_path):
    for filename in os.listdir(input_path):
        filepath = os.path.join(input_path, filename)
        pcd = o3d.io.read_point_cloud(filepath)
        output_file_path = os.path.join(out_path, filename)
        
        plane_model, inliers = pcd.segment_plane(distance_threshold=0.02, ransac_n=6, num_iterations=10000)
        [A, B, C, D] = plane_model
        print(f"Plane equation: {A:.2f}x + {B:.2f}y + {C:.2f}z + {D:.2f} = 0")
        inlier_cloud = pcd.select_by_index(inliers)
        o3d.io.write_point_cloud(output_file_path, inlier_cloud, write_ascii=True)
        print(f"{filename} saved to {out_path}")


if __name__ == '__main__':
    input_path = "J:/2023_POISE/2023POISE_seed/test/ply"
    out_path = "J:/2023_POISE/2023POISE_seed/test/plane"
    plane(input_path,out_path)