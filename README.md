# HumanActivityCollection

This repositories includes point cloud collection by TI mmWave IWR1443BOOST, RGB-D image collection by Intel RealSense, human body join and skeleton estimation by Cubemos. 




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
- < ActivityName > _ color _ < timestamp >.json
- < ActivityName > _ depth _ < timestamp >.json
- < ActivityName > _ mmw _ < timestamp >.txt
- < ActivityName > _ skeleton _ < timestamp >.txt

