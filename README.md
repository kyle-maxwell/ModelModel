BLENDER - Generate 2D Image from 3D Model
====================
To run the blender script, have blender locally installed.
Blender UI must be able to open (i.e. you can't ssh and run this script) (DOES IT ACTUALLY??)

blender.exe -b models/test.blend --python blenderscript.py

models/test.blend is the 3d Model you want to generate images of.

You can specifiy the number of angles to capture images from by changing NUM_ANGLES.
It will generate NUM_ANGLES^2 Model Images and save them into data/models/test/


OVERLAY - Overlay object images with background
====================
If you ran the blender script as stated above, the object images should be in the right structure

Run this command:

python overlay.py {WIDTH} {HEIGHT} {BKGD_FOLDER} data/models/

Where WIDTH and HEIGHT are dimensions of the object images
BKGD_FOLDER is where your background images are located
data/models/ contains the folders in which all of the Model Images are saved

You can specify the amount of overlays per Model Image by changing 'num_overlays' in overlay.py
This script will overwrite every Model Image in the object data folders.

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
