import open3d as o3d
import numpy as np
import pandas as pd
import os
from scipy.optimize import least_squares
from sklearn.decomposition import PCA

def load_mesh(mesh_path):
    try:
        mesh = o3d.io.read_triangle_mesh(mesh_path)
        mesh.compute_vertex_normals()
        voxel_size = 0.01
        point_cloud = mesh.sample_points_poisson_disk(number_of_points=5000)
        points = np.asarray(point_cloud.points)
        return mesh, points
    except Exception as e:
        print(f"Error loading mesh: {e}")
        return None, None

def ellipsoid_residuals(params, points):
    x0, y0, z0, a, b, c = params
    x, y, z = points[:, 0], points[:, 1], points[:, 2]
    a, b, c = np.abs([a, b, c])
    residuals = ((x - x0) / a) ** 2 + ((y - y0) / b) ** 2 + ((z - z0) / c) ** 2 - 1
    return residuals

def apply_pca(points):
    pca = PCA(n_components=3)
    pca.fit(points)
    points_transformed = pca.transform(points)
    return points_transformed, pca

def fit_ellipsoid(points):
    points_transformed, pca = apply_pca(points)
    x0, y0, z0 = np.mean(points_transformed, axis=0)
    a, b, c = np.std(points_transformed, axis=0)
    initial_guess = np.array([x0, y0, z0, a, b, c])
    result = least_squares(ellipsoid_residuals, initial_guess, args=(points_transformed,))
    ellipsoid_params_transformed = result.x
    a, b, c = ellipsoid_params_transformed[3], ellipsoid_params_transformed[4], ellipsoid_params_transformed[5]
    return x0, y0, z0, a, b, c, pca

def point_to_ellipsoid_distance(point, center, rotation_matrix, axes_lengths):
    transformed_point = np.dot(rotation_matrix.T, point - center)
    x, y, z = transformed_point / axes_lengths
    return abs(np.sqrt(x**2 + y**2 + z**2) - 1)

def batch_process(root_dir):
    results = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file == 'texture_scene.obj':
                file_path = os.path.join(subdir, file)
                mesh, points = load_mesh(file_path)
                if points is not None:
                    x0, y0, z0, a, b, c, pca = fit_ellipsoid(points)
                    distances = []
                    for point in points:
                        distance = point_to_ellipsoid_distance(point, np.array([x0, y0, z0]), pca.components_.T, np.array([a, b, c]))
                        distances.append(distance)
                    average_distance = np.mean(distances)
                    folder_name = os.path.basename(subdir)
                    results.append((folder_name, average_distance))

    results_df = pd.DataFrame(results, columns=['folder', 'mean_distance'])
    results_df.to_csv(os.path.join(root_dir, 'ShapeRegularity.csv'), index=False)

def main():
    root_dir = r"your\path"
    batch_process(root_dir)

if __name__ == "__main__":
    main()
