# POISE

**POISE** (Plant Online Interactive Stereo model development Environment), an online platform for 3D visualization and interactive investigation of plant architecture and organ morphology with the embedded support of multilevel segmentation information.


## :computer:Getting Started
### Access Address
https://bic.njau.edu.cn/poise.html
### Local Deployment
The web deployment was tested on IIS, Apache, and nginx, while browser testing was conducted on Chrome, Edge, and Safari.
```shell
#Clone POISE
git clone --recursive https://github.com/ganlab/POISE.git
```

### Custom Component
Our online measurement feature is developed based on [three.js](https://github.com/mrdoob/three.js). You can customize measurement components in the POISE\js\3DView\measurements directory, or customize the interface in the root directory of POISE.



### :film_projector: Demo

[![Watch the video](https://img.youtube.com/vi/mZH4Jgh5X0I/hqdefault.jpg)](https://youtu.be/mZH4Jgh5X0I)

## ScaleCalculator
### with depth
You can run the script to perform depth-based scale estimation. 
```shell
python ScaleCalculator/with_depth/main.py 
```
We have provided a sample for you to test in ScaleCalculator/with_depth/sample.

### with object anchor
The training and prediction process is completed using [pointnet++](https://github.com/yanx27/Pointnet_Pointnet2_pytorch)

#### predicted object anchor point cloud.
```shell
python data_process/prediction/prediction_result.py
```
The results are in ScaleCalculator/with_objectanchor/log/sem_seg/2023_seed/visual. 

#### Estimation real-scale.

This process may involve converting .ply files to .obj files.
```shell
python data_process/prediction/plyobj2.py
```
Then,
```shell
python data_process/prediction/txt2scale.py
```

#### background segmentation.
```shell
python data_process/prediction/seg_glb.py
```

We have provided a sample for you to test in ScaleCalculator/with_objectanchor/test.

## :book:Citation
Please considering cite our paper if you find this work useful!
```
@misc{
}
```

## :clap: Acknowledgements
[three.js](https://github.com/mrdoob/three.js)
[Colmap](https://github.com/colmap/colmap)
[Open3D](https://github.com/isl-org/Open3D).
[3DView.Measurements](https://github.com/AwesomeTeamOne/3DView.Measurements)
