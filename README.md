BLENDER - Generate 2D Image from 3D Model
====================
To run the blender script, have blender locally installed

Navigate to where the executable is, and do this:


blender.exe test.blend -b --python blenderscript.py


It will save the images in the folder specified at the top of blenderscript.py (change this to fit your local machine)

VIDEO SPLIT - Generate images from video
====================
Name video files either "empty_{objectname}" (for videos without object) or "{objectname} _ #".

Run program as

```python
python VideoSplit.py {video_filename} ... {video_filename}
```
This will generate a folder for images of the object called "objectname" and a folder called empty_pics.