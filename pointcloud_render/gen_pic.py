import numpy as np
import open3d as o3d
from pathlib import Path
import csv

class Points:
    def __init__(self, frame,x,y,z):
        self.x = x 
        self.y = y 
        self.z = z
        self.frame = frame

frame = 0
point_id = 0
f = open('idle.txt')
k = f.readlines()
tmp_x = 0.0
tmp_y = 0.0
tmp_z = 0.0
tmp_id = 0
all_point = []
for element in k:
    #print(element)
    if(element == '---'):
        continue
    else:
        tmp = element.split(':')
        if(tmp[0]) == 'point_id':
            tmp_id = int(tmp[1])
            if(tmp_id<point_id):
                frame = frame+1
            point_id = tmp_id
        elif(tmp[0]) == 'x':
            tmp_x = float(tmp[1])
        elif(tmp[0]) == 'y':
            tmp_y = float(tmp[1])
        elif(tmp[0]) == 'z':
            tmp_z = float(tmp[1])
            tmp_point = Points(frame,tmp_x,tmp_y,tmp_z)
            all_point.append(tmp_point)
f.close()
total_frame = frame+1
total_point = len(all_point)

f = open('summary.txt', 'w')
f.write("Total frame:"+str(total_frame)+'\n')
f.write("Average point per frame:"+str(total_point/total_frame)+'\n')
f.close()

frame = 0
frame_list = []
tmp_list = []
for element in all_point:
    if element.frame==frame:
        tmp_list.append([element.x,element.y,element.z])
    else:
        frame_list.append(tmp_list)
        tmp_list = []
        frame = frame+1
        tmp_list.append([element.x,element.y,element.z])
frame_list.append(tmp_list)
#print(tmp_list)
Path(f'plys').mkdir(parents=True ,exist_ok=True)
output_csv = []
with open (Path(f'summary.csv'), 'w') as f:
    writer = csv.writer(f)
    for index,element in enumerate(frame_list):
        # print('-------------------------------')
        # print(element)
        writer.writerow([len(element)])
        arr = np.array(element)
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(arr)
        o3d.io.write_point_cloud(f"./plys/data_{index}.ply", pcd)


    
