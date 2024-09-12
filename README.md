# Ren'Py UI elements for GVH fan games

## GVH-style choice menu

This just makes the choice menus styled more like the ones in GVH.  To use them:
1. Copy the file `gvhchoice.rpy` into your game folder, and copy the folder `images/gvhchoice` into your `images` folder.
2. Thats... really it.  Choice menus are called the same way as before.

Some special effects are available by adding some control characters to the choice text, for example:
```renpy

menu:
    "Normal button":
        # ...
    "~ Wobbly button effect ~":
        # ...
    "/ Parallelogram button /":
        # ...
    "Fake choice that statics out -> Real choice":
        # ...
    "* Button with bubbles rising up *":
        # ...
    "(( Button that thumps when hovered ))":
        # ...
```

More special effects are planned (just takes time to get them working in Ren'Py!).  Suggestions are welcome.

## Texting overlay

This redirects the character dialogue into a texting interface.  To use it:
1. Copy the file `texting.rpy` into your game folder, and copy the folder `images/texting` into your `images` folder.
2. To activate texting mode, use `show screen texting()`.  Optionally, you can add a chat title at the top, and specify which character's point of view (pov) this is from.  For example:
```renpy
fang "Time to check my phone"
show screen texting ("WORM CHAT", pov=fang)
fang "Hey guys"
reed "Sup?"
trish "Sup?"
pause
hide screen texting
fang "Well, that was fun."
```
3. You can add icons for the people texting.  Just create a 90x90 image with the character's name and the word "icon", e.g. *reedicon.png*.
4. Optionally, if you specify a character for the point of view, and that character's image has a `texting` attribute, then that attribute will be triggered while that person is writing a text.

**Notes**
- This will override any custom "say" screen you may have.
- Word wrapping sometime acts weird in the chat bubbles, causing them to extend across the texting area and get cut off.  If this happens, you may need to add your own line breaks (`\n`) to manually wrap things at an earlier point in the line.
- This interface can only handle 1 or 2 lines in the text bubble, so need to keep things short and sweet.

## Rhythm game

This provides a UI for a rhythm game in Ren'Py, using similar controls to GVH.

### How to use

1. Copy the file `rhythmgame.rpy` into your game folder, and copy the folder `images/rhythmgame` into your `images` folder.
2. Pick a short name for the rhythm game.  In this example, *mygame* will be used, but you can replace that with whatever fits.
3. Copy a music file into `audio/*mygame*.mp3`
4. Within your script, activate the screen in *beat recording* mode by adding the line `show screen rhythmgame("mygame",mode="record")`.  You may need to add a pause statement so your script doesn't end prematurely while the recording is happening.
5. Run your script, and when the rhythm controls show up and the music starts playing, tap out your beats using the arrow keys, and W,A,S,D,Q keys.  There's no visuals at this stage, so you'll just have to use your imagination for what's happening.  Once you're done, hit space to end the recording.
6. *You can skip the next few steps if you don't need lyrics to show up.*  Create a file `audio/*mygame*.lyrics.txt` with the line-by-line lyrics you want to show up at the bottom of the screen.
7. Modify the line in your script to `show screen rhythmgame("mygame",mode="lyrics")`
8.  Run the script again to enter *lyric cue* mode.  Whenever you want the next line of lyrics to show up, hit the **N** key.  Hit the spacebar when you're done with the lyrics, or just close the script.
9.  Change that line in your script to `show screen rhythmgame("mygame",mode="play")`, and you should be good to go!

You can have different scenes show up while the game is going, to add some
montages or something.

**Notes**

- If you do have sequences of animations going on while the rhythmgame screen is active, you should stop the user from skipping through the animations if they press the spacebar by accident.  One way is to use hard pauses for delays, e.g. instead of `pause 5.0` use `$ renpy.pause (5.0, hard=True)`.
- Some stuff is hard-coded assuming you've set up your game in the 1920x1080 resolution.
