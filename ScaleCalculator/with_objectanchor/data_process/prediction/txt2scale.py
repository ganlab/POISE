"""
Author: Tang zy
Date: Oct 2024
"""
# Calculate the length of the anchor using obb

import os
import math
import time
import numpy as np
import open3d as o3d
import csv


def get_point_on_circle(x0, y0, r, theta):
    x = x0 + r * math.cos(theta)
    y = y0 + r * math.sin(theta)
    return x, y


def eu_3(a, b):
    distance = np.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2)
    return distance


def get_mean_dists(pcd, centroid, num_mean):
    centroid_cloud = o3d.geometry.PointCloud()
    centroid_cloud.points = o3d.utility.Vector3dVector([centroid])
    # Calculate the distance between point cloud and centroid
    dists = pcd.compute_point_cloud_distance(centroid_cloud)
    dists = np.asarray(dists)
    dists.sort()
    mean_dists = np.mean(dists[:-num_mean:-1])
    return mean_dists


def get_ball_points(centroid, mean_dists):
    center_x = centroid[0]
    center_y = centroid[1]
    radius = mean_dists
    num_points = 300
    cir_points = []
    for i in range(num_points):
        theta = i * (2 * math.pi / num_points)
        x, y = get_point_on_circle(center_x, center_y, radius, theta)
        cir_points.append((x, y))
    circle = np.asarray(cir_points)
    new_col = np.full((circle.shape[0], 1), centroid[2])
    ball = np.hstack((cir_points, new_col))
    return ball


def get_ball_cloud(ball, x):
    ball_cloud = o3d.geometry.PointCloud()
    ball_cloud.points = o3d.utility.Vector3dVector(ball)
    color = np.zeros(np.asarray(ball_cloud.points).shape)
    color[:, x] = 1
    ball_cloud.colors = o3d.utility.Vector3dVector(color)
    return ball_cloud

"""Filter out the points with label=a and rotate them to the optimal viewing angle"""
def rotation(input_path, filename, a):
    data = np.loadtxt(os.path.join(input_path, filename), dtype=float, comments='v ', usecols=(0, 1, 2, 3, 4, 5, 6))
    cords = data[:, 0:3]
    colors = data[:, 3:6] / 255
    labels = data[:, 6]
    idx = np.where(labels == a)[0]
    label_cords = cords[idx]
    label_colors = colors[idx]
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(label_cords)
    pcd.colors = o3d.utility.Vector3dVector(label_colors)
    voxel_size = 0.005  
    down_pcd = pcd.voxel_down_sample(voxel_size)
    pcd_new = down_pcd
    plane_model, inliers = pcd_new.segment_plane(distance_threshold=0.02, ransac_n=6, num_iterations=10000)
    [A, B, C, D] = plane_model
    inlier_cloud = pcd_new.select_by_index(inliers)

    plane_norm = np.array([A, B, C])
    xoy_norm = np.array([0, 0, 1])
    norm_wall = np.array(plane_norm, dtype=np.float32)
    norm_pro = np.array(xoy_norm, dtype=np.float32)
    theta = math.acos(norm_wall.dot(norm_pro) / (np.linalg.norm(norm_wall) * np.linalg.norm(norm_pro)))
    vcross = np.cross(norm_wall, norm_pro)
    vcross_normalize = 1 / np.linalg.norm(vcross) * vcross

    Rot = np.zeros((3, 3), dtype=np.float32)
    Rot[0][0] = math.cos(theta) + (1 - math.cos(theta)) * (vcross_normalize[0] ** 2)
    Rot[0][1] = vcross_normalize[0] * vcross_normalize[1] * (1 - math.cos(theta)) - vcross_normalize[2] * math.sin(
        theta)
    Rot[0][2] = vcross_normalize[1] * math.sin(theta) + vcross_normalize[0] * vcross_normalize[2] * (
                1 - math.cos(theta))
    Rot[1][0] = vcross_normalize[2] * math.sin(theta) + vcross_normalize[0] * vcross_normalize[1] * (
                1 - math.cos(theta))
    Rot[1][1] = math.cos(theta) + (1 - math.cos(theta)) * (vcross_normalize[1] ** 2)
    Rot[1][2] = -vcross_normalize[0] * math.sin(theta) + vcross_normalize[1] * vcross_normalize[2] * (
            1 - math.cos(theta))
    Rot[2][0] = -vcross_normalize[1] * math.sin(theta) + vcross_normalize[0] * vcross_normalize[2] * (
            1 - math.cos(theta))
    Rot[2][1] = vcross_normalize[0] * math.sin(theta) + vcross_normalize[1] * vcross_normalize[2] * (
            1 - math.cos(theta))
    Rot[2][2] = math.cos(theta) + (1 - math.cos(theta)) * (vcross_normalize[2] ** 2)
    rot = np.matrix(Rot)
    rotation_pcd = inlier_cloud.rotate(rot)
    return rotation_pcd

def comp_dist(pcd, i, a, png_path):
    points = np.asarray(pcd.points)
    points[:, 2] = 1
    points[0][2] = 1.0001
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd = pcd.voxel_down_sample(0.01)
    color = np.zeros(np.asarray(pcd.points).shape)
    pcd.colors = o3d.utility.Vector3dVector(color)
    
    obb = pcd.get_oriented_bounding_box()
    obb.color = (1, 0, 0)
    obb_center = obb.get_center()
    points_obb = np.asarray(obb.get_box_points())
    data = points_obb[points_obb[:, 2].argsort()]
    obb_plane = data[:4, :]
    
    centroid = pcd.get_center()
    # The point cloud is black, the bounding box vertices are blue, the centroid is red, and the bounding box center is green.
    key_points_plane = np.concatenate((obb_plane, [centroid], [obb_center]), axis=0)
    key_point_cloud = o3d.geometry.PointCloud()
    key_point_cloud.points = o3d.utility.Vector3dVector(key_points_plane)
    color_obb = [[0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [1, 0, 0], [0, 1, 0]]
    key_point_cloud.colors = o3d.utility.Vector3dVector(color_obb)
   
    dis_center = get_mean_dists(pcd, obb_center, 10)
    distance = 2 * dis_center
    ball_center = get_ball_points(obb_center, dis_center)
    ball_cloud_center = get_ball_cloud(ball_center, 1)
    
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(obb)
    vis.add_geometry(key_point_cloud)
    vis.add_geometry(ball_cloud_center)
    vis.add_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()
    time.sleep(1)
    obb_png_path = os.path.join(png_path, "{}_{}.png".format(i,a))
    vis.capture_screen_image(obb_png_path)
    time.sleep(1)
    
    vis.destroy_window()
    time.sleep(1)
    return distance

def scale_seed(file_path, png_path, fieldnames):
    with open(file_path, mode='w', newline='') as result_file:
        writer = csv.DictWriter(result_file, fieldnames=fieldnames)
        writer.writeheader()
        for filename in os.listdir(input_path):
            try:
                if filename.endswith(".txt"):
                    print(filename + ' starting')
                    i = filename.split('.')[0]
                    pcd0 = rotation(input_path, filename, 0)
                    distance0 = comp_dist(pcd0, i, 0,png_path)
                    pcd1 = rotation(input_path, filename, 1)
                    distance1 = comp_dist(pcd1, i, 1,png_path)
                    # print('The diagonal distance is :' + str(distance1))
                    ratio0 = actual_diag0 / distance0
                    ratio1 = actual_diag1 / distance1
                    values = [i, distance0, actual_diag0, ratio0, distance1, actual_diag1, ratio1]
                    writer.writerow({field: value for field, value in zip(fieldnames, values)})
                    print(filename + ' succeed...')
            except:
                print(filename + ' failed...')
    result_file.close()

if __name__ == '__main__':
    dir_path = "J:/2023_POISE/2023POISE_seed/pointnet2/test/"
    input_path = os.path.join(dir_path,"no_green")
    png_path = os.path.join(dir_path, "dis_file", "obb_png")
    os.makedirs(png_path, exist_ok=True)
    actual_diag0 = 18
    actual_diag1 = 30
    file_path = os.path.join(dir_path, "dis_file", "dis.csv")
    fieldnames = ['number', 'anchor 1 pc length', 'anchor 1 true length', 'ratio 1', 'anchor 2 pc length',
                  'anchor 2 true length', 'ratio 2']
    scale_seed(file_path, png_path, fieldnames)
