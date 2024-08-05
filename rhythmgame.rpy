# Code for rhythm minigames

# General notes:
# - Assumes a screen resolution of 1920x1080.

# State of button presses.
# If this value is > 0 when a note lands, then it was a successful hit.
# Note: could in theory have a value > 1 if the user was hovering their mouse
#       over the pad while pressing the corresponding arrow key.
default leftpressed = 0
default rightpressed = 0
default uppressed = 0

# The amount of time before game actually starts.
# (To allow time for some intro animation for the controls)
default rhythmgame_leadin = 2.0

# Indicates if rhythm game has started yet (to show control movement).
default rhythmgame_started = False

# The amount of time a beat is visible on the screen.
# (how much time the user has to react).
default beat_leadtime = 2.0

# The amount of grace time before/after the time to hit the note.
default beat_gracetime = 0.13

# The set of on-screen beats currently displayed.
# The keys are the ids, the values are the timing (position) within the music.
default onscreen_leftbeats = dict()
default onscreen_rightbeats = dict()
default onscreen_upbeats = dict()
default onscreen_Wbeats = dict()
default onscreen_Abeats = dict()
default onscreen_Sbeats = dict()
default onscreen_Dbeats = dict()
default onscreen_Qbeats = dict()
default onscreen_Ebeats = dict()

# Note: disable arrow key mappings for the quick menu, or it spazzes out
# during the minigame.
init python:
    config.keymap['focus_left'] = []
    config.keymap['focus_right'] = []
    config.keymap['focus_up'] = []
    renpy.add_layer("rhythmgame",above="master",menu_clear=True)

# Locations of the landing pads for the notes coming from the three directions.
transform leftish:
    xpos 795 ypos 845
transform rightish:
    xpos 1035 ypos 845
transform upish:
    xpos 915 ypos 725
# Filler circle in the middle of the landing pads.
transform centreish:
    xpos 915 ypos 845

# Count number of WASD pads used (for indexing a location to use).
default wasd_count = 0
# Locations to put WASD pads (cycle through these),
default wasd_xpos = [400,800,1200,1600,1600,1200,800,400]
default wasd_ypos = [200,200,200,200,600,600,600,600]

# Factor out the starting / ending positions for beats.
default left_beat_x0 = -136
default left_beat_x1 = 772
default right_beat_x0 = 1920
default right_beat_x1 = 1012
default up_beat_y0 = -136
default up_beat_y1 = 702
default qe_beat_x0 = 200
default qe_beat_x1 = 1720
default qe_beat_y0 = -200
default qe_beat_y1 = 800

# Animation for the beats
image beat:
    "beat1"
    pause 0.1
    "beat2"
    pause 0.1
    "beat3"
    pause 0.1
    repeat

image wpad:
    "w1"
    pause 0.1
    "w2"
    pause 0.1
    "w3"
    pause 0.1
    repeat
image apad:
    "a1"
    pause 0.1
    "a2"
    pause 0.1
    "a3"
    pause 0.1
    repeat
image spad:
    "s1"
    pause 0.1
    "s2"
    pause 0.1
    "s3"
    pause 0.1
    repeat
image dpad:
    "d1"
    pause 0.1
    "d2"
    pause 0.1
    "d3"
    pause 0.1
    repeat
image wasd_ring:
    "ring1"
    pause 0.1
    "ring2"
    pause 0.1
    "ring3"
    pause 0.1
    repeat    

image chevron:
    "chevron1"
    pause 0.1
    "chevron2"
    pause 0.1
    "chevron3"
    pause 0.1
    repeat
image chevron_q:
    "chevronq"
image chevron_e:
    "chevrone"

# Locations to draw the beats
transform reallyleft:
    xpos left_beat_x0 ypos 822
    linear beat_leadtime xpos left_beat_x1
transform reallyright:
    xpos right_beat_x0 ypos 822
    linear beat_leadtime xpos right_beat_x1
transform reallyup:
    xpos 892 ypos up_beat_y0
    linear beat_leadtime ypos up_beat_y1
# Sliding centre circle around a bit to show the selected direction better.
transform slide_left:
    easein 0.15 xanchor 0.5
transform slide_right:
    easein 0.15 xanchor -0.5
transform slide_up:
    easein 0.15 yanchor 0.5
transform slide_back:
    easein 0.15 xanchor 0.0 yanchor 0.0
# Circle closing in on WASD pads
transform closing_in:
    alpha 1.0 zoom 5.0
    linear beat_leadtime zoom 1.0
# Chevrons coming down
transform reallyup_q:
    xpos qe_beat_x0 ypos qe_beat_y0
    xanchor 0.5 yanchor 0.5
    linear beat_leadtime ypos qe_beat_y1
transform reallyup_e:
    xpos qe_beat_x1 ypos qe_beat_y0
    xanchor 0.5 yanchor 0.5
    linear beat_leadtime ypos qe_beat_y1
# Fading out for hits / misses
transform briefly:
    easeout 0.1 zoom 2.0 alpha 0.0

default rhythmfile = None   # For saving beat patterns (in "record" mode)
default lyricfile = None    # For saving lyric display times (in "lyric" mode)
default rhythms = None      # List of beat timings (loaded from rhythm file)
default lyric_infile = None # For reading each line of lyrics (in "lyric" mode)

screen rhythmgame(name,mode="play"):
    layer "rhythmgame"
    #modal True
    python:
        # Set up the screen
        def start(name,mode):
            # Seed the random number generator to make it deterministic.
            renpy.random.seed(0)
            # Turn off quick menu at bottom, it's too distracting!
            global quick_menu
            quick_menu = False
            ###
        # Animation for introducing the centre circle
        def show_centrecircle():
            renpy.show("centrecircle",layer="rhythmgame",at_list=[centreish],tag="centrecircle")
            renpy.hide("hit",layer="rhythmgame")
            renpy.show("hit",layer="rhythmgame",at_list=[Transform(xpos=892+68,ypos=822+68,xanchor=0.5,yanchor=0.5),briefly])
            ###
        # Animation for introducing the left landing pad
        def show_leftcircle():
            renpy.show("smallcircle1",layer="rhythmgame",at_list=[leftish],tag="leftcircle")
            xpos = left_beat_x1
            renpy.hide("hit",layer="rhythmgame")
            renpy.show("hit",layer="rhythmgame",at_list=[Transform(xpos=xpos+68,ypos=822+68,xanchor=0.5,yanchor=0.5),briefly])
            ###
        # Animation for introducing the up landing pad
        def show_upcircle():
            renpy.show("smallcircle3",layer="rhythmgame",at_list=[upish],tag="upcircle")
            ypos = up_beat_y1
            renpy.hide("hit",layer="rhythmgame")
            renpy.show("hit",layer="rhythmgame",at_list=[Transform(xpos=892+68,ypos=ypos+68,xanchor=0.5,yanchor=0.5),briefly])
            ###
        # Animation for introducing the right landing pad
        def show_rightcircle():
            renpy.show("smallcircle2",layer="rhythmgame",at_list=[rightish],tag="rightcircle")
            xpos = right_beat_x1
            renpy.hide("hit",layer="rhythmgame")
            renpy.show("hit",layer="rhythmgame",at_list=[Transform(xpos=xpos+68,ypos=822+68,xanchor=0.5,yanchor=0.5),briefly])
            ###
        # Start playing the song
        def start_music(name,mode):
            global rhythmgame_started
            # Open rhythm file for recording?
            if mode == "record":
                global rhythmfile
                rhythmfile = open(name+".rhythm.txt",'wt')
            if mode == "lyrics":
                global lyricfile, lyric_infile
                lyric_infile = renpy.open_file("audio/"+name+".lyrics.txt")
                lyricfile = open(name+".lyrics-cue.txt",'wt')
            # Start the music
            renpy.music.play(name+".mp3",loop=False)
            rhythmgame_started = True  # Can animate button presses now.
        # Handle left button press
        def pressleft(mode=None):
            global rhythmgame_started, leftpressed
            if not rhythmgame_started: return
            leftpressed += 1
            pos = renpy.music.get_pos() or 0.0
            if mode == "record":
                rhythmfile.write("%s left\n"%pos)
            renpy.show("bigcircle",layer="rhythmgame",at_list=[leftish],tag="leftbigcircle")
            renpy.show("centrecircle",layer="rhythmgame",at_list=[slide_left])
            # Check if a beat was hit
            for beat_id, final_pos in list(onscreen_leftbeats.items()):
                if pos + beat_gracetime >= final_pos and pos - beat_gracetime <= final_pos:
                    renpy.hide("leftbeat%03d"%beat_id,layer="rhythmgame")
                    del onscreen_leftbeats[beat_id]
                    # Compute the position of the beat when it was hit.
                    xpos = int(left_beat_x1 - (left_beat_x1-left_beat_x0)*(final_pos-pos)/beat_leadtime)
                    renpy.hide("hit",layer="rhythmgame")
                    renpy.show("hit",layer="rhythmgame",at_list=[Transform(xpos=xpos+68,ypos=822+68,xanchor=0.5,yanchor=0.5),briefly])
            ###
        def unpressleft():
            global leftpressed
            if not rhythmgame_started: return
            leftpressed -= 1
            if leftpressed <= 0:
                leftpressed = 0
                renpy.hide("leftbigcircle",layer="rhythmgame")
                ###
            renpy.show("centrecircle",layer="rhythmgame",at_list=[slide_back])
        # Handle right button press
        def pressright(mode=None):
            global rhythmgame_started, rightpressed
            if not rhythmgame_started: return
            rightpressed += 1
            pos = renpy.music.get_pos() or 0.0
            if mode == "record":
                rhythmfile.write("%s right\n"%renpy.music.get_pos())
            renpy.show("bigcircle",layer="rhythmgame",at_list=[rightish],tag="rightbigcircle")
            renpy.show("centrecircle",layer="rhythmgame",at_list=[slide_right])
            # Check if a beat was hit
            for beat_id, final_pos in list(onscreen_rightbeats.items()):
                if pos + beat_gracetime >= final_pos and pos - beat_gracetime <= final_pos:
                    renpy.hide("rightbeat%03d"%beat_id,layer="rhythmgame")
                    del onscreen_rightbeats[beat_id]
                    # Compute the position of the beat when it was hit.
                    xpos = int(right_beat_x1 - (right_beat_x1-right_beat_x0)*(final_pos-pos)/beat_leadtime)
                    renpy.hide("hit",layer="rhythmgame")
                    renpy.show("hit",layer="rhythmgame",at_list=[Transform(xpos=xpos+68,ypos=822+68,xanchor=0.5,yanchor=0.5),briefly])
            ###
        def unpressright():
            global rhythmgame_started, rightpressed
            if not rhythmgame_started: return
            rightpressed -= 1
            if rightpressed <= 0:
                rightpressed = 0
                renpy.hide("rightbigcircle",layer="rhythmgame")
                ###
            renpy.show("centrecircle",layer="rhythmgame",at_list=[slide_back])
        # Handle up button press
        def pressup(mode=None):
            global rhythmgame_started, uppressed
            if not rhythmgame_started: return
            uppressed += 1
            pos = renpy.music.get_pos() or 0.0
            if mode == "record":
                rhythmfile.write("%s up\n"%renpy.music.get_pos())
            renpy.show("bigcircle",layer="rhythmgame",at_list=[upish],tag="upbigcircle")
            renpy.show("centrecircle",layer="rhythmgame",at_list=[slide_up])
            # Check if a beat was hit
            for beat_id, final_pos in list(onscreen_upbeats.items()):
                if pos + beat_gracetime >= final_pos and pos - beat_gracetime <= final_pos:
                    renpy.hide("upbeat%03d"%beat_id,layer="rhythmgame")
                    del onscreen_upbeats[beat_id]
                    # Compute the position of the beat when it was hit.
                    ypos = int(up_beat_y1 - (up_beat_y1-up_beat_y0)*(final_pos-pos)/beat_leadtime)
                    renpy.hide("hit",layer="rhythmgame")
                    renpy.show("hit",layer="rhythmgame",at_list=[Transform(xpos=892+68,ypos=ypos+68,xanchor=0.5,yanchor=0.5),briefly])
            ###
        def unpressup():
            global rhythmgame_started, uppressed
            if not rhythmgame_started: return
            uppressed -= 1
            if uppressed <= 0:
                uppressed = 0
                renpy.hide("upbigcircle",layer="rhythmgame")
                ###
            renpy.show("centrecircle",layer="rhythmgame",at_list=[slide_back])
        # Handle W button press
        def pressW(mode=None):
            pos = renpy.music.get_pos() or 0.0
            if mode == "record":
                rhythmfile.write("%s W\n"%pos)
            # Check if a beat was hit
            for beat_id, (final_pos, xpos, ypos) in list(onscreen_Wbeats.items()):
                if pos + beat_gracetime >= final_pos and pos - beat_gracetime <= final_pos:
                    renpy.hide("wpad%03d"%beat_id,layer="rhythmgame")
                    renpy.hide("ring%03d"%beat_id,layer="rhythmgame")
                    del onscreen_Wbeats[beat_id]
                    renpy.hide("hit_pad",layer="rhythmgame")
                    renpy.show("hit",tag="hit_pad",layer="rhythmgame",at_list=[Transform(xpos=xpos,ypos=ypos,xanchor=0.5,yanchor=0.5),briefly])
            ###
        # Handle A button press
        def pressA(mode=None):
            pos = renpy.music.get_pos() or 0.0
            if mode == "record":
                rhythmfile.write("%s A\n"%pos)
            # Check if a beat was hit
            for beat_id, (final_pos, xpos, ypos) in list(onscreen_Abeats.items()):
                if pos + beat_gracetime >= final_pos and pos - beat_gracetime <= final_pos:
                    renpy.hide("apad%03d"%beat_id,layer="rhythmgame")
                    renpy.hide("ring%03d"%beat_id,layer="rhythmgame")
                    del onscreen_Abeats[beat_id]
                    renpy.hide("hit_pad",layer="rhythmgame")
                    renpy.show("hit",tag="hit_pad",layer="rhythmgame",at_list=[Transform(xpos=xpos,ypos=ypos,xanchor=0.5,yanchor=0.5),briefly])
            ###
        # Handle S button press
        def pressS(mode=None):
            pos = renpy.music.get_pos() or 0.0
            if mode == "record":
                rhythmfile.write("%s S\n"%pos)
            # Check if a beat was hit
            for beat_id, (final_pos, xpos, ypos) in list(onscreen_Sbeats.items()):
                if pos + beat_gracetime >= final_pos and pos - beat_gracetime <= final_pos:
                    renpy.hide("spad%03d"%beat_id,layer="rhythmgame")
                    renpy.hide("ring%03d"%beat_id,layer="rhythmgame")
                    del onscreen_Sbeats[beat_id]
                    renpy.hide("hit_pad",layer="rhythmgame")
                    renpy.show("hit",tag="hit_pad",layer="rhythmgame",at_list=[Transform(xpos=xpos,ypos=ypos,xanchor=0.5,yanchor=0.5),briefly])
            ###
        # Handle D button press
        def pressD(mode=None):
            pos = renpy.music.get_pos() or 0.0
            if mode == "record":
                rhythmfile.write("%s D\n"%pos)
            # Check if a beat was hit
            for beat_id, (final_pos, xpos, ypos) in list(onscreen_Dbeats.items()):
                if pos + beat_gracetime >= final_pos and pos - beat_gracetime <= final_pos:
                    renpy.hide("dpad%03d"%beat_id,layer="rhythmgame")
                    renpy.hide("ring%03d"%beat_id,layer="rhythmgame")
                    del onscreen_Dbeats[beat_id]
                    renpy.hide("hit_pad",layer="rhythmgame")
                    renpy.show("hit",tag="hit_pad",layer="rhythmgame",at_list=[Transform(xpos=xpos,ypos=ypos,xanchor=0.5,yanchor=0.5),briefly])
            ###
        # Handle Q button press
        def pressQ(mode=None):
            pos = renpy.music.get_pos() or 0.0
            if mode == "record":
                rhythmfile.write("%s QE\n"%pos)
            # Check if a beat was hit
            for beat_id, final_pos in list(onscreen_Qbeats.items()):
                if pos + beat_gracetime >= final_pos and pos - beat_gracetime <= final_pos:
                    renpy.hide("qpad%03d"%beat_id,layer="rhythmgame")
                    renpy.hide("qkey%03d"%beat_id,layer="rhythmgame")
                    renpy.hide("qbeat%03d"%beat_id,layer="rhythmgame")
                    del onscreen_Qbeats[beat_id]
                    # Compute the position of the beat when it was hit.
                    ypos = int(qe_beat_y1 - (qe_beat_y1-qe_beat_y0)*(final_pos-pos)/beat_leadtime)
                    renpy.hide("hit_q",layer="rhythmgame")
                    renpy.show("hit",tag="hit_q",layer="rhythmgame",at_list=[Transform(xpos=qe_beat_x0,ypos=ypos,xanchor=0.5,yanchor=0.5),briefly])
            ###
        # Handle E button press
        def pressE(mode=None):
            pos = renpy.music.get_pos() or 0.0
            # Check if a beat was hit
            for beat_id, final_pos in list(onscreen_Ebeats.items()):
                if pos + beat_gracetime >= final_pos and pos - beat_gracetime <= final_pos:
                    renpy.hide("epad%03d"%beat_id,layer="rhythmgame")
                    renpy.hide("ekey%03d"%beat_id,layer="rhythmgame")
                    renpy.hide("ebeat%03d"%beat_id,layer="rhythmgame")
                    del onscreen_Ebeats[beat_id]
                    # Compute the position of the beat when it was hit.
                    ypos = int(qe_beat_y1 - (qe_beat_y1-qe_beat_y0)*(final_pos-pos)/beat_leadtime)
                    renpy.hide("hit_e",layer="rhythmgame")
                    renpy.show("hit",tag="hit_e",layer="rhythmgame",at_list=[Transform(xpos=qe_beat_x1,ypos=ypos,xanchor=0.5,yanchor=0.5),briefly])
            ###
        # Handle progressing through lyrics (for recording their timing.)
        def pressN():
            global lyricfile, lyric_infile
            pos = renpy.music.get_pos() or 0.0
            line = lyric_infile.readline().strip().decode()
            lyricfile.write("%s %s\n"%(pos,line))
            s = renpy.get_screen('rhythmgame')
            lyrics = renpy.get_widget(s,id='lyrics')
            lyrics.set_text(line)
            ###
        # Dummy function (do nothing)
        def donothing():
            pass
        # Get all beats
        def get_beats(name,mode):
            global rhythmgame_leadin, rhythms
            if mode != "play": return []
            # Open rhythm file?
            if rhythms is None:
                _rhythms = []
                beat_id = 1
                with renpy.open_file("audio/"+name+".rhythm.txt") as f:
                    for line in f:
                        pos, direction = line.strip().split()
                        pos = float(pos)
                        direction = direction.decode()
                        _rhythms.append ((beat_id, pos+rhythmgame_leadin, direction))
                        beat_id += 1
                rhythms = _rhythms
            for beat_id, pos, direction in rhythms:
                yield (beat_id, pos, direction)
        # Get all lyrics and timings
        def get_lyrics(name,mode):
            global rhythmgame_leadin
            if mode != "play": return []
            try:
                with renpy.open_file("audio/"+name+".lyrics-cue.txt") as f:
                    for line in f:
                        try:
                            pos, lyric = line.strip().split(maxsplit=1)
                        except ValueError:
                            return  # No more useable lines?
                        pos = float(pos)
                        lyric = lyric.decode()
                        yield (pos+rhythmgame_leadin, lyric)
            except OSError:
                return  # No lyrics available

        # Routines for drawing beats on the screen when it's time for them to
        # be visible.
        def draw_left_beat(beat_id,final_pos):
            global rhythmgame_leadin
            renpy.show("beat",layer="rhythmgame",at_list=[reallyleft],tag="leftbeat%03d"%beat_id)
            onscreen_leftbeats[beat_id] = final_pos - rhythmgame_leadin
            ###
        def draw_right_beat(beat_id,final_pos):
            global rhythmgame_leadin
            renpy.show("beat",layer="rhythmgame",at_list=[reallyright],tag="rightbeat%03d"%beat_id)
            onscreen_rightbeats[beat_id] = final_pos - rhythmgame_leadin
            ###
        def draw_up_beat(beat_id,final_pos):
            global rhythmgame_leadin
            renpy.show("beat",layer="rhythmgame",at_list=[reallyup],tag="upbeat%03d"%beat_id)
            onscreen_upbeats[beat_id] = final_pos - rhythmgame_leadin
            ###
        def draw_W_pad(beat_id,final_pos):
            # Find somewhere to draw the pad.
            global wasd_count, rhythmgame_leadin
            i = wasd_count % len(wasd_xpos)
            xpos = wasd_xpos[i] + renpy.random.randint(-100,100)
            ypos = wasd_ypos[i] + renpy.random.randint(-100,100)
            wasd_count += 1
            location = Transform(xpos=xpos,ypos=ypos,xanchor=0.5,yanchor=0.5)
            renpy.show("wpad",layer="rhythmgame",at_list=[location],tag="wpad%03d"%beat_id)
            renpy.show("wasd_ring",layer="rhythmgame",at_list=[location,closing_in],tag="ring%03d"%beat_id)
            onscreen_Wbeats[beat_id] = (final_pos-rhythmgame_leadin,xpos,ypos)
            ###
        def draw_A_pad(beat_id,final_pos):
            # Find somewhere to draw the pad.
            global wasd_count, rhythmgame_leadin
            i = wasd_count % len(wasd_xpos)
            xpos = wasd_xpos[i] + renpy.random.randint(-100,100)
            ypos = wasd_ypos[i] + renpy.random.randint(-100,100)
            wasd_count += 1
            location = Transform(xpos=xpos,ypos=ypos,xanchor=0.5,yanchor=0.5)
            renpy.show("apad",layer="rhythmgame",at_list=[location],tag="apad%03d"%beat_id)
            renpy.show("wasd_ring",layer="rhythmgame",at_list=[location,closing_in],tag="ring%03d"%beat_id)
            onscreen_Abeats[beat_id] = (final_pos-rhythmgame_leadin,xpos,ypos)
            ###
        def draw_S_pad(beat_id,final_pos):
            # Find somewhere to draw the pad.
            global wasd_count, rhythmgame_leadin
            i = wasd_count % len(wasd_xpos)
            xpos = wasd_xpos[i] + renpy.random.randint(-100,100)
            ypos = wasd_ypos[i] + renpy.random.randint(-100,100)
            wasd_count += 1
            location = Transform(xpos=xpos,ypos=ypos,xanchor=0.5,yanchor=0.5)
            renpy.show("spad",layer="rhythmgame",at_list=[location],tag="spad%03d"%beat_id)
            renpy.show("wasd_ring",layer="rhythmgame",at_list=[location,closing_in],tag="ring%03d"%beat_id)
            onscreen_Sbeats[beat_id] = (final_pos-rhythmgame_leadin,xpos,ypos)
            ###
        def draw_D_pad(beat_id,final_pos):
            # Find somewhere to draw the pad.
            global wasd_count, rhythmgame_leadin
            i = wasd_count % len(wasd_xpos)
            xpos = wasd_xpos[i] + renpy.random.randint(-100,100)
            ypos = wasd_ypos[i] + renpy.random.randint(-100,100)
            wasd_count += 1
            location = Transform(xpos=xpos,ypos=ypos,xanchor=0.5,yanchor=0.5)
            renpy.show("dpad",layer="rhythmgame",at_list=[location],tag="dpad%03d"%beat_id)
            renpy.show("wasd_ring",layer="rhythmgame",at_list=[location,closing_in],tag="ring%03d"%beat_id)
            onscreen_Dbeats[beat_id] = (final_pos-rhythmgame_leadin,xpos,ypos)
            ###
        def draw_Q_beat(beat_id,final_pos):
            global rhythmgame_leadin
            renpy.show("chevron",layer="rhythmgame",at_list=[reallyup_q],tag="qbeat%03d"%beat_id)
            xpos = qe_beat_x0
            ypos = qe_beat_y1
            renpy.show("chevron",layer="rhythmgame",at_list=[Transform(xpos=xpos,ypos=ypos,xanchor=0.5,yanchor=0.5)],tag="qpad%03d"%beat_id)
            renpy.show("chevron_q",layer="rhythmgame",at_list=[Transform(xpos=xpos,ypos=ypos,xanchor=0.5,yanchor=0.5)],tag="qkey%03d"%beat_id)
            onscreen_Qbeats[beat_id] = final_pos - rhythmgame_leadin
            ###
        def draw_E_beat(beat_id,final_pos):
            global rhythmgame_leadin
            renpy.show("chevron",layer="rhythmgame",at_list=[reallyup_e],tag="ebeat%03d"%beat_id)
            xpos = qe_beat_x1
            ypos = qe_beat_y1
            renpy.show("chevron",layer="rhythmgame",at_list=[Transform(xpos=xpos,ypos=ypos,xanchor=0.5,yanchor=0.5)],tag="epad%03d"%beat_id)
            renpy.show("chevron_e",layer="rhythmgame",at_list=[Transform(xpos=xpos,ypos=ypos,xanchor=0.5,yanchor=0.5)],tag="ekey%03d"%beat_id)
            onscreen_Ebeats[beat_id] = final_pos - rhythmgame_leadin
            ###
        # Routines for checking if a beat is running into an already-activated
        # pad.
        def check_left_collision(beat_id):
            if leftpressed == 0: return
            final_pos = onscreen_leftbeats.pop(beat_id,None)
            if final_pos is None: return #???
            renpy.hide("leftbeat%03d"%beat_id,layer="rhythmgame")
            # Compute the position of the beat when it was hit.
            xpos = int(left_beat_x1 - (left_beat_x1-left_beat_x0)*beat_gracetime/beat_leadtime)
            renpy.hide("hit",layer="rhythmgame")
            renpy.show("hit",layer="rhythmgame",at_list=[Transform(xpos=xpos+68,ypos=822+68,xanchor=0.5,yanchor=0.5),briefly])
            ###
        def check_right_collision(beat_id):
            if rightpressed == 0: return
            final_pos = onscreen_rightbeats.pop(beat_id,None)
            if final_pos is None: return #???
            renpy.hide("rightbeat%03d"%beat_id,layer="rhythmgame")
            # Compute the position of the beat when it was hit.
            xpos = int(right_beat_x1 - (right_beat_x1-right_beat_x0)*beat_gracetime/beat_leadtime)
            renpy.hide("hit",layer="rhythmgame")
            renpy.show("hit",layer="rhythmgame",at_list=[Transform(xpos=xpos+68,ypos=822+68,xanchor=0.5,yanchor=0.5),briefly])
            ###
        def check_up_collision(beat_id):
            if uppressed == 0: return
            final_pos = onscreen_upbeats.pop(beat_id,None)
            if final_pos is None: return #???
            renpy.hide("upbeat%03d"%beat_id,layer="rhythmgame")
            # Compute the position of the beat when it was hit.
            ypos = int(up_beat_y1 - (up_beat_y1-up_beat_y0)*beat_gracetime/beat_leadtime)
            renpy.hide("hit",layer="rhythmgame")
            renpy.show("hit",layer="rhythmgame",at_list=[Transform(xpos=892+68,ypos=ypos+68,xanchor=0.5,yanchor=0.5),briefly])
            ###
        # Routines for handling beat misses
        def miss_left(beat_id):
            if onscreen_leftbeats.pop(beat_id,None) is None: return
            renpy.hide("leftbeat%03d"%beat_id,layer="rhythmgame")
            xpos = left_beat_x1
            renpy.hide("miss",layer="rhythmgame")
            renpy.show("miss",layer="rhythmgame",at_list=[Transform(alpha=0.5,xpos=xpos+68,ypos=822+68,xanchor=0.5,yanchor=0.5),briefly])
            ###
        def miss_right(beat_id):
            if onscreen_rightbeats.pop(beat_id,None) is None: return
            renpy.hide("rightbeat%03d"%beat_id,layer="rhythmgame")
            xpos = right_beat_x1
            renpy.hide("miss",layer="rhythmgame")
            renpy.show("miss",layer="rhythmgame",at_list=[Transform(alpha=0.5,xpos=xpos+68,ypos=822+68,xanchor=0.5,yanchor=0.5),briefly])
            ###
        def miss_up(beat_id):
            if onscreen_upbeats.pop(beat_id,None) is None: return
            renpy.hide("upbeat%03d"%beat_id,layer="rhythmgame")
            ypos = up_beat_y1
            renpy.hide("miss",layer="rhythmgame")
            renpy.show("miss",layer="rhythmgame",at_list=[Transform(alpha=0.5,xpos=892+68,ypos=ypos+68,xanchor=0.5,yanchor=0.5),briefly])
            ###
        def miss_W(beat_id):
            beat_info = onscreen_Wbeats.pop(beat_id,None)
            if beat_info is None: return
            _, xpos, ypos = beat_info
            renpy.hide("wpad%03d"%beat_id,layer="rhythmgame")
            renpy.hide("ring%03d"%beat_id,layer="rhythmgame")
            renpy.hide("miss_pad",layer="rhythmgame")
            renpy.show("miss",tag="miss_pad",layer="rhythmgame",at_list=[Transform(alpha=0.5,xpos=xpos,ypos=ypos,xanchor=0.5,yanchor=0.5),briefly])
            ###
        def miss_A(beat_id):
            beat_info = onscreen_Abeats.pop(beat_id,None)
            if beat_info is None: return
            _, xpos, ypos = beat_info
            renpy.hide("apad%03d"%beat_id,layer="rhythmgame")
            renpy.hide("ring%03d"%beat_id,layer="rhythmgame")
            renpy.hide("miss_pad",layer="rhythmgame")
            renpy.show("miss",tag="miss_pad",layer="rhythmgame",at_list=[Transform(alpha=0.5,xpos=xpos,ypos=ypos,xanchor=0.5,yanchor=0.5),briefly])
            ###
        def miss_S(beat_id):
            beat_info = onscreen_Sbeats.pop(beat_id,None)
            if beat_info is None: return
            _, xpos, ypos = beat_info
            renpy.hide("spad%03d"%beat_id,layer="rhythmgame")
            renpy.hide("ring%03d"%beat_id,layer="rhythmgame")
            renpy.hide("miss_pad",layer="rhythmgame")
            renpy.show("miss",tag="miss_pad",layer="rhythmgame",at_list=[Transform(alpha=0.5,xpos=xpos,ypos=ypos,xanchor=0.5,yanchor=0.5),briefly])
            ###
        def miss_D(beat_id):
            beat_info = onscreen_Dbeats.pop(beat_id,None)
            if beat_info is None: return
            _, xpos, ypos = beat_info
            renpy.hide("dpad%03d"%beat_id,layer="rhythmgame")
            renpy.hide("ring%03d"%beat_id,layer="rhythmgame")
            renpy.hide("miss_pad",layer="rhythmgame")
            renpy.show("miss",tag="miss_pad",layer="rhythmgame",at_list=[Transform(alpha=0.5,xpos=xpos,ypos=ypos,xanchor=0.5,yanchor=0.5),briefly])
            ###
        def miss_Q(beat_id):
            if onscreen_Qbeats.pop(beat_id,None) is None: return
            renpy.hide("qpad%03d"%beat_id,layer="rhythmgame")
            renpy.hide("qkey%03d"%beat_id,layer="rhythmgame")
            renpy.hide("qbeat%03d"%beat_id,layer="rhythmgame")
            xpos = qe_beat_x0
            ypos = qe_beat_y1
            renpy.hide("miss_q",layer="rhythmgame")
            renpy.show("miss",tag="miss_q",layer="rhythmgame",at_list=[Transform(alpha=0.5,xpos=xpos,ypos=ypos,xanchor=0.5,yanchor=0.5),briefly])
            ###
        def miss_E(beat_id):
            if onscreen_Ebeats.pop(beat_id,None) is None: return
            renpy.hide("epad%03d"%beat_id,layer="rhythmgame")
            renpy.hide("ekey%03d"%beat_id,layer="rhythmgame")
            renpy.hide("ebeat%03d"%beat_id,layer="rhythmgame")
            xpos = qe_beat_x1
            ypos = qe_beat_y1
            renpy.hide("miss_e",layer="rhythmgame")
            renpy.show("miss",tag="miss_e",layer="rhythmgame",at_list=[Transform(alpha=0.5,xpos=xpos,ypos=ypos,xanchor=0.5,yanchor=0.5),briefly])
            ###
        # Update lyrics at the bottom of the screen.
        def lyric (line):
            s = renpy.get_screen('rhythmgame')
            lyrics = renpy.get_widget(s,id='lyrics')
            lyrics.set_text(line)

        # End of minigame (cleanup)
        def finish(mode):
            # Turn on quick menu at bottom
            global quick_menu
            quick_menu = True
            # Rest state of button presses, so they start unpressed for the
            # next rhythmgame after this one.
            leftpressed = 0
            rightpressed = 0
            uppressed = 0
            # Stop any music that's playing
            renpy.music.stop()
            # Close rhythm and lyrics files.
            if mode == "record":
                global rhythmfile
                rhythmfile.close()
                rhythmfile = None
            if mode == "lyrics":
                global lyricfile
                lyricfile.close()
                lyricfile = None
            # No more onscreen beats.
            global onscreen_leftbeats, onscreen_rightbeats, onscreen_upbeats
            global onscreen_Wbeats, onscreen_Abeats, onscreen_Sbeats, onscreen_Dbeats
            global wasd_count
            onscreen_leftbeats = dict()
            onscreen_rightbeats = dict()
            onscreen_upbeats = dict()
            onscreen_Abeats = dict()
            onscreen_Sbeats = dict()
            onscreen_Dbeats = dict()
            onscreen_Qbeats = dict()
            onscreen_Ebeats = dict()
            wasd_count = 0
            global rhythmgame_started, rhythms
            rhythmgame_started = False
            rhythms = None
            # Clear the rhythmgame screen from display.
            ui.layer("rhythmgame")
            ui.clear()
            ui.close()

    # Bind arrow keys to the landing pads.
    key "keydown_K_LEFT" action Function(pressleft,mode)
    key "keyup_K_LEFT" action unpressleft
    key "keydown_K_RIGHT" action Function(pressright,mode)
    key "keyup_K_RIGHT" action unpressright
    key "keydown_K_UP" action Function(pressup,mode)
    key "keyup_K_UP" action unpressup
    # Bind WASD keys as well.
    key "K_w" action Function(pressW,mode)
    key "K_a" action Function(pressA,mode)
    key "K_s" action Function(pressS,mode)
    key "K_d" action Function(pressD,mode)
    # Bind Q and E keys for those chevron things
    key "K_q" action Function(pressQ,mode)
    key "K_e" action Function(pressE,mode)
    # Bind "N" key for next lyric line.
    if mode == "lyrics":
        key "K_n" action Function(pressN)
    # Disable menu during minigame (the beats won't pause!)
    key "game_menu" action donothing

    # Handle non-keyboard triggers (hovering over pads).
    # Also handles taps from touch screens, although it's a little flaky
    # for the web version (can tap to activate the pad, but holding your finger
    # down can cause the browser to do something weird like bring up a select
    # / copy / etc. prompt).
    imagemap:
        ground "invisible"
        alpha False
        # Note: I needed to add a dummy "clicked" parameter, or other things
        # like "hovered" don't work!
        hotspot (795, 845, 90, 90) clicked donothing hovered pressleft unhovered unpressleft
        hotspot (1035, 845, 90, 90) clicked donothing hovered pressright unhovered unpressright
        hotspot (915, 725, 90, 90) clicked donothing hovered pressup unhovered unpressup

    # Add a textbox for showing the lyrics.
    frame:
        background None
        xsize 1.0
        yanchor 0.5 ypos 1000
        hbox:
            xalign 0.5
            # Text will be dynamically updated during rhythmgame.
            text "" textalign 0.5 line_spacing 10 outlines [(5,"000000",0,0)] id "lyrics"

    # Call the startup routine once for this screen.
    on "show" action Function(start,name,mode)
    # Show the pads.
    timer 1.0 action Function(show_centrecircle)
    timer 1.6 action Function(show_leftcircle)
    timer 1.8 action Function(show_upcircle)
    timer 2.0 action Function(show_rightcircle)
    timer rhythmgame_leadin action Function(start_music,name,mode)
    # Queue up the beats.
    for beat_id, pos, direction in get_beats(name,mode):
        if direction == "left":
            timer pos-beat_leadtime action Function(draw_left_beat,beat_id,pos)
            timer pos-beat_gracetime action Function(check_left_collision,beat_id)
            timer pos+beat_gracetime action Function(miss_left,beat_id)
        if direction == "right":
            timer pos-beat_leadtime action Function(draw_right_beat,beat_id,pos)
            timer pos-beat_gracetime action Function(check_right_collision,beat_id)
            timer pos+beat_gracetime action Function(miss_right,beat_id)
        if direction == "up":
            timer pos-beat_leadtime action Function(draw_up_beat,beat_id,pos)
            timer pos-beat_gracetime action Function(check_up_collision,beat_id)
            timer pos+beat_gracetime action Function(miss_up,beat_id)
        if direction == "W":
            timer pos-beat_leadtime action Function(draw_W_pad,beat_id,pos)
            timer pos+beat_gracetime action Function(miss_W,beat_id)
        if direction == "A":
            timer pos-beat_leadtime action Function(draw_A_pad,beat_id,pos)
            timer pos+beat_gracetime action Function(miss_A,beat_id)
        if direction == "S":
            timer pos-beat_leadtime action Function(draw_S_pad,beat_id,pos)
            timer pos+beat_gracetime action Function(miss_S,beat_id)
        if direction == "D":
            timer pos-beat_leadtime action Function(draw_D_pad,beat_id,pos)
            timer pos+beat_gracetime action Function(miss_D,beat_id)
        if direction == "QE":
            timer pos-beat_leadtime action Function(draw_Q_beat,beat_id,pos)
            timer pos-beat_leadtime action Function(draw_E_beat,beat_id,pos)
            timer pos+beat_gracetime action Function(miss_Q,beat_id)
            timer pos+beat_gracetime action Function(miss_E,beat_id)
    # Clean up close rhythmgame after the last beats are done.
    if mode == "play":
        timer pos+2.0 action [Function(finish,mode),Return()]
    # Allow termination of rhything / lyrics recording with space bar.
    else:
        key "K_SPACE" action [Function(finish,mode),Return()]
    # Queue up the lyrics.
    for pos, line in get_lyrics(name,mode):
        timer pos action Function(lyric,line)
