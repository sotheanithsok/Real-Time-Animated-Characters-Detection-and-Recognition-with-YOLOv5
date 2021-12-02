<p align="center">
  <img src="Presentation/demo.gif" alt="animated" />
</p>

<h1 align="center"> Real-Time Animated Characters Detection and Recognition with YOLOv5</h1>

## Description
Examine the performance of the YOLOv5 algorithm in detecting and recognizing Tom, Jerry, and Spike.

## Dataset
 - Source: [Tom & Jerry | Triple Trouble | Classic Cartoon Compilation | WB Kids](https://youtu.be/rilFfbm7j8k)
 - Images: 1000
   - Has an object: 931
   - No object: 69
 - Object Instances:
   - Tom: 562
   - Spike: 538
   - Jerry: 490
 - Split Ratio:
   - Train: 70%
   - Validation: 21%
   - Test: 9%   

## Performances
| Model  	| Input Size 	| Batch Size 	| Dataset Size 	| Val mAP@.5 	| Test mAP@.5 	|
|--------	|------------	|------------	|--------------	|------------	|-------------	|
| Nano   	| 640x640    	| 16         	| 25%          	| 0.964      	| 0.989       	|
| Nano   	| 640x640    	| 16         	| 50%          	| 0.969      	| 0.953       	|
| Nano   	| 640x640    	| 16         	| 75%          	| 0.989      	| 0.982       	|
| Nano   	| 640x640    	| 16         	| 100%         	| 0.989      	| 0.977       	|
| Small  	| 640x640    	| 16         	| 25%          	| 0.989      	| 0.921       	|
| Small  	| 640x640    	| 16         	| 50%          	| 0.983      	| 0.935       	|
| Small  	| 640x640    	| 16         	| 75%          	| 0.977      	| 0.98        	|
| Small  	| 640x640    	| 16         	| 100%         	| 0.98       	| 0.985       	|
| Medium 	| 640x640    	| 16         	| 25%          	| 0.946      	| 0.914       	|
| Medium 	| 640x640    	| 16         	| 50%          	| 0.984      	| 0.982       	|
| Medium 	| 640x640    	| 16         	| 75%          	| 0.971      	| 0.992       	|
| Medium 	| 640x640    	| 16         	| 100%         	| 0.983      	| 0.986       	|

## Hardwares
 - CPU: [AMD Ryzen 9 5900X](https://www.amd.com/en/products/cpu/amd-ryzen-9-5900x)
 - Memory: [G.Skill Trident Z 32GB @ 3600 Mhz](https://www.amazon.com/G-Skill-TridentZ-288-Pin-3600MHz-F4-3600C17D-16GTZR/dp/B01N4V82FW)
 - GPU: [EVGA GeForce RTX 3060](https://www.evga.com/products/product.aspx?pn=12G-P5-3657-KR)
 - Storage: [Western Digital 1TB WD Blue](https://www.westerndigital.com/products/internal-drives/wd-blue-desktop-sata-hdd#WD10EZEX)

## Quick Links
 - [640p Dataset](https://mega.nz/file/z3YCWBYC#n6Klmpr3XB6ula_WOSriem5W0gnNgEZk3tZBVm5wDQ8)
 - [1280p Dataset](https://mega.nz/file/uyAwFZaK#9lZAk6_Pn0W9yB40KlfZx7e5WjYgTjdzIVogt6qv1jA)
 - [Detection Demo Videos](https://drive.google.com/drive/folders/1lrzEbeN1YUsLuAcWPxh-CivSbFcn73Ns?usp=sharing)
 - [Presentation](https://github.com/sotheanith/Real-Time-Animated-Characters-Detection-and-Recognition-with-YOLOv5/blob/main/Presentation/Presentation.pdf)
 - [Train Video](https://youtu.be/rilFfbm7j8k)
 - [Test Video](https://youtu.be/cqyziA30whE)

## Source Codes
 - [videos.py](https://github.com/sotheanith/Real-Time-Animated-Characters-Detection-and-Recognition-with-YOLOv5/blob/main/videos.py)
 - [extract.py](https://github.com/sotheanith/Real-Time-Animated-Characters-Detection-and-Recognition-with-YOLOv5/blob/main/extract.py)
 - [dataset.py](https://github.com/sotheanith/Real-Time-Animated-Characters-Detection-and-Recognition-with-YOLOv5/blob/main/datasets.py)
 - [yolov5.py](https://github.com/sotheanith/Real-Time-Animated-Characters-Detection-and-Recognition-with-YOLOv5/blob/main/yolov5.py)
 - [train.py](https://github.com/sotheanith/Real-Time-Animated-Characters-Detection-and-Recognition-with-YOLOv5/blob/main/train.py)
 - [detect.py](https://github.com/sotheanith/Real-Time-Animated-Characters-Detection-and-Recognition-with-YOLOv5/blob/main/detect.py)
 - [settings.json](https://github.com/sotheanith/Real-Time-Animated-Characters-Detection-and-Recognition-with-YOLOv5/blob/main/settings.json)
 - [requirements.txt](https://github.com/sotheanith/Real-Time-Animated-Characters-Detection-and-Recognition-with-YOLOv5/blob/main/requirements.txt)

## Prerequisites
 - [Python](https://www.python.org/)
 - [OpenCV](https://pypi.org/project/opencv-python/)
 - [Mega.py](https://pypi.org/project/mega.py/)
 - [Torch](https://pypi.org/project/torch/)
 - [PyTube](https://pypi.org/project/pytube/)
 - [ruamel.yaml](https://pypi.org/project/ruamel.yaml/)
 - [urllib3](https://pypi.org/project/urllib3/)
 - [YOLOv5](https://github.com/ultralytics/yolov5)

## Authors
 - [Sotheanith Sok](https://github.com/sotheanith)

## Course
 - [CECS 553 - Machine Vision](http://catalog.csulb.edu/preview_course_nopop.php?catoid=5&coid=40043)
