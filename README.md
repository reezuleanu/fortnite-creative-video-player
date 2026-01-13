# Fortnite Creative Video Player (UEFN)
## Summary
These are instructions on how to make a video player in Fornite Creative (even when UEFN will fight you)

Provided is the script for the video player in game, and some utilities in python that I needed to make along the way. The island can be loaded on consoles as well, as long as the overall size is below the limit of 400 MBs. If exceeded, it will crash on consoles and only work on PC.

https://github.com/user-attachments/assets/53381488-f4d9-40e1-8829-5378644cdcb8

## Repository structure
- inside `verse` you will find the device file you need to import into UEFN
- inside `py_utils` are python scripts meant to help you and don't need to be imported into UEFN

## Steps for getting a video into Fornite Creative
1. First, you will need a video (and optionally sound). You will need to turn your video into individual frames, at whatever framerate and compression you choose. I personally used ffmpeg for both video conversion AND audio compression. Keep in mind the 400 MBs limit. You can go above it, I could launch the island at 700 MBs on PC only, going above it could prove unstable.

My command for video to frames: `ffmpeg -i VIDEO.mp4 -q:v 31 -vf fps=10 output/PREFIX_%d.jpg`
For audio compression: `ffmpeg -i VIDEO.mp4 -vn -ac 1 16000 -sample_fmt s16 AUDIO_COMPRESSED.wav`

You can name the files whatever you want, just keep in mind the extensions, since ffmpeg uses them to infer your intent. Those commands output the worst quality video you have ever seen since 2005, as well as 16khz audio that sounds like it came fresh from a Pringles can.

2. Import all of these files into your UEFN project. The audio file should be straight forward, but if you have more than 1000 frames for your video, you will encounter something I dubbed "the virtual texture nightmare". UEFN will try to optimize textures, and this cannot be disabled like in UE5. Normally optimization is good, but it will try to batch a lot of textures into a single, virtual one, and Verse doesn't have the ability to let you programatically select individual textures from this VT (none that I found at least) like you can with individual textures.

The workaround is simple, overflow that bastard. After your 1000th texture, it will try to combine all the next textures into a single VT, but it can only do so for about 910 of them. My advice is to just import all the textures, then at the end (if UEFN doesn't crash) see what texture were batched into that VT. Then, use the `vt_overflow.py` util to duplicate those files while chaning the naming scheme in a way that UEFN cannot pick up on. Then import those, and after it's done, right click on them and do a "batch rename", where you rename them to match the naming scheme again. Afterwards, you can delete the VT.

3. Now that you have your textures, you'll need a way to iterate over them via Verse. The language is so well designed that not a single overpayed engineer thought about providing a way of accessing the textures by their name as a string, basically locking you into only using the exact variable (which you cannot iterate over).

To overcome bad design or an active rebellion against creativity, I created `textures2mappings.py`. It is a texture that takes the .verse file containing the assets (including textures) and generates a Verse dictionary where each texture variable corresponds to a string (that being their name) which can be iterated over by the video player. Make sure to impor the resulting `TextureMappings.verse` into UEFN.

4. Import the video device from `verse` and place it in your world. Make sure to modify the verse file appropriately to use whatever Material you want for the video player, as well as getting the framerate and frame naming scheme correct.

5. Load into your island and hit the play button. If nothing happens, UEFN might have gotten confused along the way, just delete the device from the map itself and drag it again, as well as making sure you are using the right Material for the video.

## CURRENT ISSUES
UEFN is so bad that right now it won't launch on my PC anymore so I need to reinstall my OS. Until I find the time/energy for it, the following known issues are unfixed:
- A stutter happens when you first play the video, getting the audio out of sync. On a second play of the video it's fine, but I need to implement something to check how long it has been since the first frame and determine if a stutter happened or not, in which case the play method would just be called again

## DISCLAIMER
This project is purely experimental and for educational/fun purposes. I am not responsible for however you decide to use this information, and any incident that may come from this is entirely due to Epic Games' verification process before publishing the island being subpar.
