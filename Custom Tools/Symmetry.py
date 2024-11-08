import os
import numpy as np
import open3d as o3d
from scipy.optimize import least_squares
from sklearn.decomposition import PCA
import csv

def load_mesh(mesh_path):
    try:
        mesh = o3d.io.read_triangle_mesh(mesh_path)
        mesh.compute_vertex_normals()
        voxel_size = 0.01
        point_cloud = mesh.sample_points_poisson_disk(number_of_points=5000)  # 使用泊松磁盘采样
        points = np.asarray(point_cloud.points)
        return mesh, point_cloud, points
    except Exception as e:
        print(f"Error loading mesh: {e}")
        return None, None, None

def ellipsoid_residuals(params, points):
    x0, y0, z0, a, b, c = params
    x, y, z = points[:, 0], points[:, 1], points[:, 2]
    a, b, c = np.abs([a, b, c])
    residuals = ((x - x0) / a) ** 2 + ((y - y0) / b) ** 2 + ((z - z0) / c) ** 2 - 1
    return residuals

def apply_pca(points):
    pca = PCA(n_components=3)
    points_transformed = pca.fit_transform(points)
    return points_transformed, pca

def fit_ellipsoid(points):
    points_transformed, pca = apply_pca(points)
    x0, y0, z0 = np.mean(points_transformed, axis=0)
    a, b, c = np.std(points_transformed, axis=0)
    initial_guess = np.array([x0, y0, z0, a, b, c])
    result = least_squares(ellipsoid_residuals, initial_guess, args=(points_transformed,))
    ellipsoid_params_transformed = result.x
    x0, y0, z0 = ellipsoid_params_transformed[0:3]
    a, b, c = np.abs(ellipsoid_params_transformed[3:6])
    return x0, y0, z0, a, b, c, pca

def calculate_average_distance_to_ellipsoid(points, x0, y0, z0, a, b, c):
    x, y, z = points[:, 0], points[:, 1], points[:, 2]
    distances = ((x - x0) / a) ** 2 + ((y - y0) / b) ** 2 + ((z - z0) / c) ** 2 - 1
    return np.mean(distances)

def process_all_meshes(root_dir):
    results = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file == 'texture_scene.obj':
                mesh_path = os.path.join(subdir, file)
                folder_name = os.path.basename(subdir)
                mesh, point_cloud, points = load_mesh(mesh_path)
                if points is not None:
                    x0, y0, z0, a, b, c, pca = fit_ellipsoid(points)
                    points_transformed = pca.transform(points)
                    condition = points_transformed[:, 0] >= 0
                    points_part_1 = points[condition]
                    points_part_2 = points[~condition]
                    mean_distance_part_1 = calculate_average_distance_to_ellipsoid(points_part_1, x0, y0, z0, a, b, c) if len(points_part_1) > 0 else None
                    mean_distance_part_2 = calculate_average_distance_to_ellipsoid(points_part_2, x0, y0, z0, a, b, c) if len(points_part_2) > 0 else None
                    ratio = mean_distance_part_1 / mean_distance_part_2
                    results.append([folder_name, mean_distance_part_1, mean_distance_part_2, ratio])
                print(f"{mesh_path} processed.")
    return results

def save_results_to_csv(results, output_path):
    header = [
        'folder', 'mean_distance_part_1', 'mean_distance_part_2', 'ratio'
    ]
    with open(output_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(results)

def main():
    root_dir = r'your\path'
    results = process_all_meshes(root_dir)
    output_path = r'your\path\Symmetry.csv'
    save_results_to_csv(results, output_path)

if __name__ == "__main__":
    main()