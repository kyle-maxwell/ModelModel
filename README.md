BLENDER - Generate 2D Image from 3D Model
====================
To run the blender script, have blender locally installed.
Blender UI must be able to open (i.e. you can't ssh and run this script)
Add a folder of background images called "Background/" in the folder where the blender executable is located

Navigate to where the blender executable is, and do this:

blender.exe -b test.blend --python blenderscript.py

It will save the images in the folder specified in the init variables (change this to fit your local machine)

OVERLAY - Overlay object images with background
====================
If you ran the blender script, the object images should be in the right structure
Copy the data folder from your blender folder to where you want to train your model

Run this command:

python overlay.py {WIDTH} {HEIGHT} {BKGD_FOLDER} [data/{OBJ}...]

Where WIDTH and HEIGHT are dimensions of the object images
BKGD_FOLDER is where your background images are located
[data/{OBJ}...] are the folders where the object images are located

eg) python overlay.py 256 256 Background data/bottle data/lacroix data/shoe

This script will overwrite every train and val image in the object data folders

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
