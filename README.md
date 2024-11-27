# POISE

POISE (Plant Online Interactive Stereo model development Environment), comprises three components: an online platform for 3D visualization and interactive investigation of plant architecture and organ morphology; [OSTRA](https://github.com/ganlab/OSTRA) (available independently) for modelling plants in the original growth state and segmenting organs; ScaleCalculator for recovering physical scales of 3D models.

## :computer:Getting Started
### Online database
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
### Option 1: depth image
You can run the script to perform depth-based scale estimation. 
```shell
python ScaleCalculator/with_depth/main.py 
```
We have provided a sample for you to test in ScaleCalculator/with_depth/sample.

### Option 2: object anchor 
You can run the script to perform object anchor-based scale estimation. 

<details>
  <summary>Click to expand for more details</summary>

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
</details>

We have provided a sample for you to test in ScaleCalculator/with_objectanchor/test.

## :book:Citation
Please considering cite our paper if you find this work useful!
```
@misc{
}
```

## License
Free for non-profit research purposes. Please contact authors otherwise. The program itself may not be modified in any way and no redistribution is allowed.
No condition is made or to be implied, nor is any warranty given or to be implied, as to the accuracy of POISE, or that it will be suitable for any particular purpose or for use under any specific conditions, or that the content or use of PROPA will not constitute or result in infringement of third-party rights.

## :clap: Acknowledgements
Website is based on [three.js](https://github.com/mrdoob/three.js) and [3DView.Measurements](https://github.com/AwesomeTeamOne/3DView.Measurements). ScaleCalculator is based on [Open3D](https://github.com/isl-org/Open3D) and [pointnet++](https://github.com/yanx27/Pointnet_Pointnet2_pytorch). The software is developed by following author(s) and supervised by Prof. Xiangchao Gan(gan@njau.edu.cn).

Authors:

Jiexiong Xu
xu_jx@stu.njau.edu.cn
work: Website framework development, measurement tools, and ScaleCalculator with depth image.

Jiaqi Deng
2023122005@stu.njau.edu.cn
work: Website optimization.

Zhiyan Tang
2022119002@stu.njau.edu.cn
work: ScaleCalculator with object anchor.
