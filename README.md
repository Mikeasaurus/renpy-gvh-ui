# Ren'Py UI elements for GVH fan games

## Rhythm game

This provides a UI for a rhythm game in Ren'Py, using similar controls to GVH.

### How to use

1. Copy the file `rhythmgame.rpy` into your script folder, and copy the folder `images/rhythmgame` into your `images` folder.
2. Pick a short name for the rhythm game.  In this example, *mygame* will be used, but you can replace that with whatever fits.
3. Copy a music file into `audio/*mygame*.mp3`
4. Within your script, activate the screen in *beat recording* mode by adding the line `show scene rhythmgame("mygame",mode="record")`.  You may need to add a pause statement so your script doesn't end prematurely which the recording is happening.
4. Run your script, and when the rhythm controls show up and the music starts playing, tap out your game using the arrow keys, and W,A,S,D,Q keys.  There's no visuals at this stage, so you'll just have to use your imagination for what's happening.  Once you're done, hit space to end the recording.
5. You should have a file `*mygame*.rhythm.txt` in the root directory of Ren'Py... or somewhere... good luck.  Move that file to your `audio` folder alongside the mp3 file.
6. *You can skip the next few steps if you don't need lyrics to show up.*  Create a file `audio/*mygame*.lyrics.txt` with the line-by-line lyrics you want to show up at the bottom of the screen.
7. Modify the line in your script to `show scene rhythmgame("mygame",mode="lyrics")`
8.  Run the script again to enter *lyric cue* mode.  Whenever you want the next line of lyrics to show up, hit the **N** key.  Hit the spacebar when you're done with the lyrics, or just close the script.
10.  You should have the file `*mygame*.lyrics-cue.txt` in your root Ren'Py directory.  Move this to your `audio` folder.
11.  Change that line in your script to `show scene rhythmgame("mygame",mode="play")`, and you should be good to go!

You can have different scenes show up while the game is going, to add some
montages or something.

