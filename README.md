<!-- Readme Start here -->

<!-- Load logo from readme/logo.jpg -->
<div align="center">
  <img src="readme/logo.gif" alt="logo" />
</div>


<!-- Title -->
<h1 align="center" style="border: none">
Real-Time Animated Characters Detection and Recognition with YOLOv5
</h1>


<!-- Shield IO - very nice icons -->
<div align="center">

[![Contributors][contributors_shield]][contributors_url]
[![Forks][forks_shield]][forks_url]
[![Stargazers][stars_shield]][stars_url]
[![Issues][issues_shield]][issues_url]
[![MIT License][license_shield]][license_url]
[![LinkedIn][linkedin_shield]][linkedin_url]

</div>


<!-- Description -->
Examine the performance of the YOLOv5 algorithm in detecting and recognizing Tom, Jerry, and Spike.

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

## [Training Dataset]
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

## [Testing Dataset]
  - [Nano Models]
  - [Small Models]
  - [Medium Models]

## Documentation
  - [Presentation]

## Hardwares
 - CPU: [AMD Ryzen 9 5900X](https://www.amd.com/en/products/cpu/amd-ryzen-9-5900x)
 - Memory: [G.Skill Trident Z 32GB @ 3600 Mhz](https://www.amazon.com/G-Skill-TridentZ-288-Pin-3600MHz-F4-3600C17D-16GTZR/dp/B01N4V82FW)
 - GPU: [EVGA GeForce RTX 3060](https://www.evga.com/products/product.aspx?pn=12G-P5-3657-KR)
 - Storage: [Western Digital 1TB WD Blue](https://www.westerndigital.com/products/internal-drives/wd-blue-desktop-sata-hdd#WD10EZEX)

<!-- Include your major tools and frameworks -->
## Built With
- [Python]
- [Torch]
- [YOLOv5]


<!-- Collaborators information -->
## Collaborators
- [Sotheanith Sok]

## Course
- [CECS 553 - Machine Vision]


<!-- License -->
## License
This project is licensed under the MIT License - see the [LICENSE.md][license_url] file for details


<!-- Shoutout to other projects, plugin, or minor tools -->
## Acknowledgments
Special thank to
- [Best-README-Template] - the readme template.


<!-- References -->
<!-- Shield Icons-->
[contributors_shield]: https://img.shields.io/github/contributors/sotheanithsok/Real-Time-Animated-Characters-Detection-and-Recognition-with-YOLOv5.svg?style=for-the-badge
[forks_shield]: https://img.shields.io/github/forks/sotheanithsok/Real-Time-Animated-Characters-Detection-and-Recognition-with-YOLOv5.svg?style=for-the-badge
[stars_shield]: https://img.shields.io/github/stars/sotheanithsok/Real-Time-Animated-Characters-Detection-and-Recognition-with-YOLOv5.svg?style=for-the-badge
[issues_shield]: https://img.shields.io/github/issues/sotheanithsok/Real-Time-Animated-Characters-Detection-and-Recognition-with-YOLOv5.svg?style=for-the-badge
[license_shield]: https://img.shields.io/github/license/sotheanithsok/Real-Time-Animated-Characters-Detection-and-Recognition-with-YOLOv5.svg?style=for-the-badge
[linkedin_shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555

<!-- Shield URLs -->
[contributors_url]: https://github.com/sotheanithsok/Real-Time-Animated-Characters-Detection-and-Recognition-with-YOLOv5/graphs/contributors
[forks_url]: https://github.com/sotheanithsok/Real-Time-Animated-Characters-Detection-and-Recognition-with-YOLOv5/network/members
[stars_url]: https://github.com/sotheanithsok/Real-Time-Animated-Characters-Detection-and-Recognition-with-YOLOv5/stargazers
[issues_url]: https://github.com/sotheanithsok/Real-Time-Animated-Characters-Detection-and-Recognition-with-YOLOv5/issues
[license_url]: https://github.com/sotheanithsok/Real-Time-Animated-Characters-Detection-and-Recognition-with-YOLOv5/blob/master/LICENSE
[linkedin_url]: https://www.linkedin.com/in/sotheanith-sok-969ab0b3/

<!-- Other links -->
[Sotheanith Sok]: https://github.com/sotheanithsok
[Best-README-Template]: https://github.com/othneildrew/Best-README-Template

[Training Dataset]: https://youtu.be/rilFfbm7j8k
[Testing Dataset]: https://youtu.be/cqyziA30whE
[Nano Models]: https://mega.nz/file/Li5HXTba#7_Fi9IEGk0NVrF-QdCIh7FXhGh_-8vJSIV_qmBouBdg
[Small Models]: https://mega.nz/file/HqZVBZBA#ajHw8FsTsSeallv9O6upVg1V_44G6S5abCqPBPep4L8
[Medium Models]: https://mega.nz/file/6uRRDSyB#aplsy1n9Nb2NH7-Jx6wz9AnIAWMFb_iaUe5b1qIqmKY
[Presentation]: Presentation/Presentation.pdf
[Python]: https://www.python.org/
[Torch]: https://pypi.org/project/torch/
[YOLOv5]: https://github.com/ultralytics/yolov5
[CECS 553 - Machine Vision]: http://catalog.csulb.edu/preview_course_nopop.php?catoid=5&coid=40043


