import numpy as np
import open3d as o3d
from pathlib import Path
import shutil
import csv
import time
import json
import re
import ast
import sys

from open3d.j_visualizer import geometry_to_json
keypoint_ids = [(1, 2),(1, 5),(2, 3),(3, 4),(5, 6),(6, 7),(1, 8),(8, 9),
(9, 10),(1, 11),(11, 12),(12, 13),(1, 0),(0, 14),(14, 16),(0, 15),(15, 17)]
tripod_height = 1

class Points:
    def __init__(self, frame,x,y,z):
        self.x = x 
        self.y = y 
        self.z = z
        self.frame = frame

def fill_missing_point(ele):
    if not ele:
        return np.array([np.nan, np.nan, np.nan])
    # transform = np.matmul(np.array([[1,0,0],[0,0,-1],[0,1,0]]),(np.array(ele).reshape(3,1)))
    # return transform.reshape(3,)
    ele[1] += tripod_height ## add the height of tirpod (m)
    return ele

def render_skeleton():
    f = open('../ioio_skeleton_162158040837904.json')
    r = f.readlines()
    m = re.findall("\{.*?\}", r[0])
    
    vis = o3d.visualization.Visualizer()
    vis.create_window()

    geometry = o3d.geometry.PointCloud()
    line_set = o3d.geometry.LineSet()
    # # The x, y, z axis will be rendered as red, green, and blue arrows respectively
    frame = o3d.geometry.TriangleMesh.create_coordinate_frame(1.0)

    vis.add_geometry(frame)
    vis.add_geometry(geometry)
    vis.add_geometry(line_set)
    ctr = vis.get_view_control()
    # ctr.set_lookat([0,1,1]) # the point that the camera look at
    # ctr.set_front([0.5,-1,0]) #the point that the camera stand
    # ctr.set_up([0,1,0]) ## [x,y,z] boolean is up # default is 0,1,0
    ctr.set_zoom(2.0)

 
    for data in m:
        # skeleton per timestamp
        for _, joints in json.loads(data).items():
            points = np.array(list(map(fill_missing_point,joints[0])))
            line_list = []
            for l in keypoint_ids:
                if joints[0][l[0]] and joints[0][l[1]]:
                    line_list.append(list(l))
            colors = [[1, 0, 0] for i in range(len(line_list))]
        
        
        geometry.points = o3d.utility.Vector3dVector(points)
        line_set.points = o3d.utility.Vector3dVector(points)
        line_set.lines = o3d.utility.Vector2iVector(line_list)
        line_set.colors = o3d.utility.Vector3dVector(colors)
        
        vis.update_geometry(geometry)
        vis.update_geometry(line_set)
        vis.update_renderer()
        vis.poll_events()
        time.sleep(0.05)
        
        
def generate_mmw_points():
    def create_points_in_frame(frame, arr):
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(arr)
        o3d.io.write_point_cloud(f"./plys/frame_{frame}.ply", pcd)
    frame = -1
    point_id = -1
    f = open('dataset/0514/45_eat_fork__mmw_162097647180488.txt')
    tmp_x = 0.0; tmp_y = 0.0; tmp_z = 0.0; tmp_id = 0
    all_points = []; frame_list = []
    ## mkdir for storing .ply file
    shutil.rmtree(f'plys')
    Path(f'plys').mkdir(parents=True ,exist_ok=True)
    # parse the raw txt
    for element in f.readlines():
        if(element == '---'):
            continue
        else:
            tmp = element.split(':')
            if(tmp[0]) == 'point_id' and int(tmp[1])==0:
                if frame_list:
                    create_points_in_frame(frame, frame_list)
                frame += 1
                frame_list = []
            elif(tmp[0]) == 'x':
                tmp_x = float(tmp[1])
            elif(tmp[0]) == 'y':
                tmp_y = float(tmp[1])
            elif(tmp[0]) == 'z': # if read z, got a point, then append
                tmp_z = float(tmp[1])
                frame_list.append([tmp_x, tmp_y, tmp_z])
    create_points_in_frame(frame, frame_list)
    f.close()

def render_mmw():
    
    
    vis = o3d.visualization.Visualizer()
    vis.create_window(width=640, height=480)

    geometry = o3d.geometry.PointCloud()

    # The x, y, z axis will be rendered as red, green, and blue arrows respectively
    frame = o3d.geometry.TriangleMesh.create_coordinate_frame(1.0)

    vis.add_geometry(frame)
    vis.add_geometry(geometry)
  
    ctr = vis.get_view_control()
    # ctr.set_lookat([0.25,0.25,1])
    # ctr.set_front([-0.25,0,0.1])
    # ctr.set_up([0,0,1]) ## [x,y,z] boolean is up
    ctr.set_zoom(1.25)

    index = 0
    os.path()
    while index<1072:
        try:
            pcd= o3d.io.read_point_cloud(f'./plys/frame_{index}.ply')
            new_points = np.asarray(pcd.points)
            geometry.points = o3d.utility.Vector3dVector(new_points)
            R = geometry.get_rotation_matrix_from_xyz((np.pi *3 / 2, 0, 0))
            geometry.rotate(R, center=(0, 0, 0))
            vis.update_geometry(geometry)
            vis.update_renderer()
            vis.poll_events()

            time.sleep(0.05)
            index += 1
            
        except Exception as e:
            print(e)
        
        
    # vis.destroy_window()
    
if __name__=="__main__":
    render_mmw()
    # generate_mmw_points()
    # render_skeleton()