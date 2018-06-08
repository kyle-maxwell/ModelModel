BLENDER - Generate 2D Image from 3D Model
====================
To run the blender script, have blender locally installed.

Run this command:


blender.exe -b models/test.blend --python blenderscript.py

models/test.blend is the 3d Model you want to generate images of.

You can specifiy the number of angles to capture images from by changing NUM_ANGLES.
It will generate NUM_ANGLES^2 Model Images and save them into data/models/test/


OVERLAY - Overlay object images with background
====================

```python
python overlay.py {blender.exe} {folder containing models}
```
This script will generate images from 'blenderscript.py' and then add backgrounds to those using images from ImageNet.
Expects 'fall11_urls.txt' to be in the current directory. This file contains a list of url's to use as backgrounds for the blender generated images.
It writes all of the images into './data/models/{Model_name}/' and deletes whatever was in these folders originally.
For each model it is, currently set to generate images with the model in 15^2 different positions, with 10 unique backgrounds for each position. This amounts to 2250 images for each model.

VIDEO SPLIT - Generate images from video
====================
Name video files either "empty_{objectname}" (for videos without object) or "{objectname} _ #".

Run program as

```python
python VideoSplit.py {video_filename} ... {video_filename}
```
This will generate a folder for images of the object called "objectname" and a folder called empty_pics.

MODEL PREDICT - Predicts images from folders
====================
Create directories as you wish in your local filesystem.
Run program as
```python
python ModelPredict {weight_selected} {directory_name/}
```
This will display the image it predicted on, titled with the Object name (also prints to terminal)
