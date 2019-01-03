## How to train classifier  
  
https://coding-robin.de/2013/07/22/train-your-own-opencv-haar-classifier.html

You should do the following steps in order to train a classifier:  
- get some positive images with the feature which you want to classify - should be no background images (1)
- get as many as possible negative images (2)
- merge positive images with the negative one in order to create some positive samples with background. (3)
- train the classifier. (4)
- use the classifier. (5)
  
  
Structure of out project:  
Let's take door cascade training for example.  

Storage structure:  
- ```build_classifier/door/sample_positive_images``` - there you could find positive images with doors rotated by an predefined angle
- ```build_classifier/door/negative_images_for_crop``` - there you could find some full images from where the door images were removed.
- ```build_classifier/door/sample_negative_images``` - there you could find some cropped negative images, cropped using crop_negative_images.py script
- ```build_classifier/door/samples``` - there you could find some mixed images between negative and positive ones by create_samples.py script.
  
1) ```crop_negative_images.py``` - this script is used to crop negative images from some full images which does not contains the 
positive images. - the output images are automatically uploaded to remote server.
2) ```create_sample.py``` - after cropping negative images, you should mix them with selected positive images, this script is
used for doing that. - the output images are automatically uploaded to remote server.
3) ```build_classifier.py``` - call this script with -p=schedule parameter in order to start building the cascade classifier on
AI server or call it with -p=get_results in order to get the results from AI server.
4) ```view_vec_file.py``` - call this in order to view images from copped.vec files