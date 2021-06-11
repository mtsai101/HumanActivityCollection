## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################

import pyrealsense2 as rs
import numpy as np
import time
import cv2
import sys
import subprocess
import os
import math
import threading
from collections import namedtuple
from rs_skeleton.skeletontracker import skeletontracker
import rs_skeleton.util as cm

record_flag = False
cur_time = None
close_camera = False
activity_type = None
camera_ready = threading.Event()

def render_ids_3d(render_image, skeletons_2d, depth_map, depth_intrinsic, joint_confidence, joint_writer=None):
    thickness = 1
    text_color = (255, 255, 255)
    rows, cols, channel = render_image.shape[:3]
    distance_kernel_size = 5
    skeleton_list = []
    # calculate 3D keypoints and display them
    for skeleton_index in range(len(skeletons_2d)):
        skeleton_2D = skeletons_2d[skeleton_index]
        joints_2D = skeleton_2D.joints
        did_once = False
        joint_list = None ## record joints
        for joint_index in range(len(joints_2D)):
            if did_once == False:
                cv2.putText(
                    render_image,
                    "id: " + str(skeleton_2D.id),
                    (int(joints_2D[joint_index].x), int(joints_2D[joint_index].y - 30)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    text_color,
                    thickness,
                )
                joint_list = list()

                did_once = True
            # check if the joint was detected and has valid coordinate
            if skeleton_2D.confidences[joint_index] > joint_confidence:
                distance_in_kernel = []
                low_bound_x = max(
                    0,
                    int(
                        joints_2D[joint_index].x - math.floor(distance_kernel_size / 2)
                    ),
                )
                upper_bound_x = min(
                    cols - 1,
                    int(joints_2D[joint_index].x + math.ceil(distance_kernel_size / 2)),
                )
                low_bound_y = max(
                    0,
                    int(
                        joints_2D[joint_index].y - math.floor(distance_kernel_size / 2)
                    ),
                )
                upper_bound_y = min(
                    rows - 1,
                    int(joints_2D[joint_index].y + math.ceil(distance_kernel_size / 2)),
                )
                for x in range(low_bound_x, upper_bound_x):
                    for y in range(low_bound_y, upper_bound_y):
                        distance_in_kernel.append(depth_map.get_distance(x, y))
                median_distance = np.percentile(np.array(distance_in_kernel), 50)
                depth_pixel = [
                    int(joints_2D[joint_index].x),
                    int(joints_2D[joint_index].y),
                ]
                if median_distance > 0.3:
                    point_3d = rs.rs2_deproject_pixel_to_point(
                        depth_intrinsic, depth_pixel, median_distance
                    )
                    point_3d = np.round([float(point_3d[0]), float(-point_3d[1]), float(-point_3d[2])], 3)
                    point_str = [x for x in point_3d]
                    cv2.putText(
                        render_image,
                        str(point_3d),
                        (int(joints_2D[joint_index].x), int(joints_2D[joint_index].y)),
                        cv2.FONT_HERSHEY_DUPLEX,
                        0.4,
                        text_color,
                        thickness,
                    )
                    joint_list.append(point_str)
                else:
                    joint_list.append([])
            else:
                joint_list.append([])
        skeleton_list.append(joint_list)
        if joint_writer:
            joint_writer.write_skeleton(skeleton_list)

def get_depthcolor_map(color_image=None, depth_image=None):
    
    # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
    depth_colormap_dim = depth_colormap.shape
    color_colormap_dim = color_image.shape

    # If depth and color resolutions are different, resize color image to match depth image for display
    if depth_colormap_dim != color_colormap_dim:
        resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
        images = np.hstack((resized_color_image, depth_colormap))
    else:
        images = np.hstack((color_image, depth_colormap))

    # Show images
    # cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
    # cv2.imshow('RealSense', depth_colormap)
    # cv2.waitKey(1)
    return depth_colormap

def start_camera():
    global record_flag, cur_time, close_camera
    depth_writer = color_writer = joint_writer = None
    skeleton_trace = []

    config = rs.config()
    pipeline = rs.pipeline()

    pipeline.start()

    # # Create align object to align depth frames to color frames
    align = rs.align(rs.stream.color)
    # # Get the intrinsics information for calculation of 3D point
    # unaligned_frames = pipeline.wait_for_frames()
    # frames = align.process(unaligned_frames)
    # depth = frames.get_depth_frame()
    # depth_intrinsic = depth.profile.as_video_stream_profile().intrinsics

    # Initialize the cubemos api with a valid license key in default_license_dir()
    skeletrack = skeletontracker(cloud_tracking_api_key="")
    joint_confidence = 0.2

    ## video writer
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    window_name = "cubemos skeleton tracking with realsense D400 series"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL + cv2.WINDOW_KEEPRATIO)
    camera_ready.set()
    try:
        while True:
            
            # Wait for a coherent pair of frames: depth and color
            unaligned_frames = pipeline.wait_for_frames()
            frames = align.process(unaligned_frames)
            depth_frame = frames.get_depth_frame() ## depth frame and intrinstics should update every frame, in case some depth info. are missing
            depth_intrinsic = depth_frame.profile.as_video_stream_profile().intrinsics
            color_frame = frames.get_color_frame()

            if not depth_frame or not color_frame:
                continue

            # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())
            depth_colormap = get_depthcolor_map(color_image, depth_image)

            skeletons = skeletrack.track_skeletons(color_image)
            cm.render_result(skeletons, color_image, joint_confidence)
            color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
            
            # check record or not
            if record_flag:
                if not (depth_writer and color_writer and joint_writer):
                    depth_writer = cv2.VideoWriter(
                        f'{activity_type}_depth_{cur_time}.mp4', fourcc, 24, (640, 480), True)
                    color_writer = cv2.VideoWriter(
                        f'{activity_type}_color_{cur_time}.mp4', fourcc, 24, (640, 480), True)
                    joint_writer = cm.JointWriter(output_path = f'{activity_type}_skeleton_{cur_time}.json')

                joint_writer.time_stamp = str(int(time.time() * (10**5)))
            else:
                depth_writer = color_writer = joint_writer = None

            render_ids_3d(
                color_image, skeletons, depth_frame, depth_intrinsic, joint_confidence, joint_writer
            )
            
            if record_flag and (depth_writer and color_writer and joint_writer): 
                depth_writer.write(depth_colormap)
                color_writer.write(color_image)
                cv2.putText(color_image, "Recording", (20,30), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 255), 1,)

            if close_camera:
                break
            
            cv2.imshow(window_name, color_image)
            if cv2.waitKey(1) == 27:
                break
            
    finally:
        # Stop streaming
        pipeline.stop()
        cv2.destroyAllWindows()

def main():
    global record_flag, cur_time, close_camera, activity_type
    mmwave_proc = None
    camera_thread = threading.Thread(target=start_camera)
    camera_thread.start()
    camera_ready.wait()
    while True:
        c = input("Start(s), stop(t), or Quit(q):")
        if c == "s":
            if not mmwave_proc:
                activity_type = input("Type the activity:")
                cur_time = str(int(time.time() * (10**5)))
                output_path = f'{activity_type}_mmw_{cur_time}.txt'
                f = open(output_path, 'w')
                mmwave_proc = subprocess.Popen(["rostopic", "echo", "/ti_mmwave/radar_scan"], stdout=f)
                record_flag = True
                
        elif c == "t":
            record_flag = False
            if mmwave_proc:
                mmwave_proc.kill()
                mmwave_proc = None
                f.close()
            else:
                print("No Running mmWave Process")
            
        else:
            close_camera = True
            camera_thread.join()
            print("Quit")
            break
            
   


if __name__=="__main__":
    main()