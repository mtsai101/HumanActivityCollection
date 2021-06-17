# HumanActivityCollection

This repositories includes point cloud collection by TI mmWave IWR1443BOOST, RGB-D image collection by Intel RealSense, human body join and skeleton estimation by Cubemos. 

## Operating System: Ubuntu 18.04 LTS
 

## Devices:
```
TI mmWave IWR1443BOOST ES2.0 EVM
Intel(R) RealSense(TM) Depth Camera 435
```

## Requirements
Launch your virtual environment (Recommend)
```
python3 -m venv venv
source venv/bin/activate
```
Please follow the documents below to settle down the all tools or packages.
### [TI mmWave and ROS visualization](https://hackmd.io/kmnOAiLEQkSf0WQ2C_sClQ)
### [IntelRease X Cubemos](https://hackmd.io/U6MzT9rPS82ut7Q6Tfsd3Q)



## How To Run
We have integrate both sensor collection into collect.py
```python
python3 collect.py
```
**Type s:** start the recording
  - Type the activity name: *ActivityName*
  - 
**Type t:** stop and save the recording

**Type q:** stop and save the recording; close the window

The red text "Recording" is shown during the recording

<img width="400" src="https://user-images.githubusercontent.com/15339223/121655354-2143d000-cad1-11eb-9c30-0eef02665fcd.png">

The results would be written into the follwing files:
- < ActivityName > _ color _ < timestamp >.mp4
- < ActivityName > _ depth _ < timestamp >.mp4
- < ActivityName > _ mmw _ < timestamp >.txt
- < ActivityName > _ skeleton _ < timestamp >.txt
Sample results can be found [here](https://drive.google.com/drive/folders/1DeQZuqLcInEF_YPhyaLtGXcPwgi5_Nl3?usp=sharing)

## Data Format

### RGB & Depth
#### RGB with human joints and skeleton visualization: < ActivityName > _ color _ < timestamp >.mp4
The video is stored in 24 fps. The frame rate can be adjusted in collect.py

<img width="400" src="https://user-images.githubusercontent.com/15339223/121656025-a62ee980-cad1-11eb-96ad-a751651e987a.png">

#### Depth Heatmap: < ActivityName > _ depth _ < timestamp >.mp4
The video is stored in 24 fps. The frame rate can be adjusted in collect.py

<img width="370" src="https://user-images.githubusercontent.com/15339223/121656107-b777f600-cad1-11eb-8df6-734ad9f5327d.png">

#### mmWave: < ActivityName > _ mmw _ < timestamp >.txt
The message format follows [radar-lab/ti_mmwave_rospkg](https://github.com/radar-lab/ti_mmwave_rospkg)
```
header: 
  seq: 6264
  stamp: 
    secs: 1538888235
    nsecs: 712113897
  frame_id: "ti_mmwave"   # Frame ID used for multi-sensor scenarios
point_id: 17              # Point ID of the detecting frame (Every frame starts with 0)
x: 8.650390625            # Point x coordinates in m (front from antenna)
y: 6.92578125             # Point y coordinates in m (left/right from antenna, right positive)
z: 0.0                    # Point z coordinates in m (up/down from antenna, up positive)
range: 11.067276001       # Radar measured range in m
velocity: 0.0             # Radar measured range rate in m/s
doppler_bin: 8            # Doppler bin location of the point (total bins = num of chirps)
bearing: 38.6818885803    # Radar measured angle in degrees (right positive)
intensity: 13.6172780991  # Radar measured intensity in dB
```

#### Human Body Joints: < ActivityName > _ skeleton _ < timestamp >.txt
We store the human body joints of each frame is json format, and attach the next new coming frame right after. 

There are totally **18** body joints in a complete skeleton.
- **Sample collection:**
```json
{"162219366570749": [[
    [0.066, -0.176, -2.054],
    [0.066, -0.365, -2.047],
    [-0.083, -0.36, -2.02],
    [-0.216, -0.513, -2.0],
    [-0.137, -0.457, -1.784],
    [0.223, -0.364, -2.118],
    [0.281, -0.44, -1.749],
    [0.262, -0.483, -1.838],
    [-0.013, -0.48, -1.286],
    [],
    [],
    [0.109, -0.466, -1.249],
    [],
    [],
    [0.044, -0.143, -2.11],
    [0.102, -0.134, -1.987],
    [0.006, -0.192, -2.089],
    [0.146, -0.18, -2.103]]]
  }
```
- **Mapping of list element to the body joints:**
 
<img height="600" src="https://i.imgur.com/yeCLJQE.png">

Reference: [Skeleton Tracking SDKのPython版サンプルのコードを読んでみた[Windows編]](https://dev.classmethod.jp/articles/skeleton-tracking-sdk-by-python)
