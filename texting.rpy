# Modify say screen to control whether the background is darkened when
# characters are talking.
# We don't want this if the dialogue is being displayed as texts.
default show_textbox = True
screen say(who, what):
    style_prefix "say"

    window:
        id "window"
        if not show_textbox:
            background None
        if show_textbox == "top":
            yalign 0.0

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"

# A place to store the texting history while the screen is active.
default texting_history = None

# Fade-in effect for texting window
transform texting_fadein:
    alpha 0.0
    easein 0.5 alpha 1.0

screen texting(title=None,pov=None,save={},resume=False):
    # Trick for making viewport that autoscrolls to bottom.
    # Source: https://lemmasoft.renai.us/forums/viewtopic.php?p=521419&sid=1f0e9f9e9478f7e2d24b2a653952b3d0#p521419
    default yadj = ui.adjustment()  # Assign dummy value for now, so yadj is screen variable.
    python:  # This is the trick for keeping viewport at the bottom.
        if yadj.value == yadj.range:
            yadj.value = float('inf')
    # Frame for the text conversation
    frame:
        at texting_fadein
        background None
        xsize 0.5
        xpadding 100 ypadding 50
        vbox:
            spacing 30
            # Title of chat goes in here.
            hbox id "chattitle":
                xanchor 0.5 xpos 0.3
            # Where the texts show up.
            # Make it scrollable.
            # Assign yadjustment attribute to "yadj" variable for access.
            null
            viewport yadjustment yadj id "vp":
                mousewheel True
                yinitial 1.0
                # The vertical stack of text messages
                vbox id "chat":
                    # Make it use entire width of frame, so sender's messages are
                    # aligned all the way to the right.
                    xfill True
    python:
        def start_texting (title,pov,save,resume):
            # Disable the textbox background while using texting.
            # Otherwise get an annoying black shaded box covering part of the
            # screen for no reason.
            global show_textbox, textingmode, text_pov, texting_history
            show_textbox = False
            textingmode = True
            # If this was called with resume=True, then use whatever was in the
            # last texting session.
            if resume is True: resume = dict(texting_history)
            texting_history = save
            # If resuming, use old title and pov if not otherwise updated.
            if resume is not False:
                if title is None: title = resume.get("title",None)
                if pov is None: pov = resume.get("pov",None)
            if hasattr(pov,"name"):
                text_pov = pov.name
            else:
                text_pov = pov
            # Add chat title at the top.
            if title is not None:
                s = renpy.get_screen('texting')
                chattitle = renpy.get_widget(s,id='chattitle')
                t = Text(title, color="000000", align=(0.5,0.5))
                w = Window(t,background=Frame("centrechattitle",tile='integer'),ysize=56,xfill=False)
                chattitle.add(Frame(ImageReference("leftchattitle"),ysize=56,xsize=16))
                chattitle.add(w)
                chattitle.add(Frame(ImageReference("rightchattitle"),ysize=56,xsize=16))
            # Store texting metadata in case it's needed later.
            save['title'] = title
            save['pov'] = pov
            save['history'] = []
            # If resuming a conversation, display the past history again.
            if resume is not False:
                for who, what in resume['history']:
                    if who == text_pov:
                        sendertxt (who, what, instantaneous=True)
                    else:
                        othertxt (who, what, instantaneous=True)

        def stop_texting():
            # Remove the texting conversation.
            global show_textbox, textingmode
            show_textbox = True
            textingmode = False

    on "show" action Function(start_texting,title,pov,save,resume)
    on "hide" action Function(stop_texting)

image dotdotdot:
    "dotdotdot1"
    pause 0.15
    "dotdotdot2"
    pause 0.15
    "dotdotdot3"
    pause 0.15
    "dotdotdot4"
    pause 0.15
    repeat

# Keep track of where character icon is, so only one copy is shown in a row.
# [name,container]
default last_icon = [None,None]

python early:
    def sendertxt (Name, msg, instantaneous=False, **kwargs):
        s = renpy.get_screen('texting')
        chat = renpy.get_widget(s,id='chat')
        # Brief pause before message appears
        if not instantaneous:
            renpy.pause(2.0+0.1*len(msg))
        # The message
        t = Text(msg, color="ffffff", align=(0.5,0.5))
        # Put it on a background
        w = Window(t,background=Frame("centreblackbubble",tile='integer'),ysize=90,xfill=False)
        # Add round sides
        h = HBox(xanchor=1.0,xpos=1.0)
        h.add(Frame(ImageReference("leftblackbubble"),ysize=90,xsize=45))
        h.add(w)
        h.add(Frame(ImageReference("rightblackbubble"),ysize=90,xsize=45))
        if last_icon[0] is not None:
            chat.add(Null(height=20))
        # If the sender is talking, then invalid the "last icon" tracker.
        last_icon[0] = None
        # Add message to the chat
        chat.add(h)
        # Add a bit of vertical spacing of texts.
        chat.add(Null(height=10))
        # Record this message in the history.
        texting_history['history'].append((Name,msg))
    def othertxt (Name, msg, instantaneous=False, **kwargs):
        # Lower-case version of name for image files.
        name = Name.lower()
        s = renpy.get_screen('texting')
        chat = renpy.get_widget(s,id='chat')
        if not instantaneous:
            # Brief pause before dots appear
            renpy.pause(1.0)
        # Show dots
        dots = ImageReference('dotdotdot')
        h = HBox(xanchor=0.0,xpos=0.0)
        h.add(Null(width=100))
        # Extra space and nametag if this is not the same person talking as before
        if last_icon[0] != Name:
            chat.add(Null(height=20))
            nameplate = HBox(xanchor=0.0,xpos=0.0)
            nameplate.add(Null(width=120,height=50))
            nameplate.add(Text(Name, color="ffffff",outlines=[(3,"000000",0,0)]))
            chat.add(nameplate)
        if not instantaneous:
            h.add(dots)
            chat.add(h)
            # Brief pause before message appears
            renpy.pause(2.0+0.05*len(msg))
            chat.remove(h)
        # The message
        t = Text(msg, color="000000", align=(0.5,0.5))
        # Put it on a background
        w = Window(t,background=Frame("centrewhitebubble",tile='integer'),ysize=90,xfill=False)
        # Add round sides
        h = HBox(xanchor=0.0,xpos=0.0)
        # Add image icon if available, otherwise use initials
        if renpy.has_image(name+"icon"):
            icon = ImageReference(name+"icon")
        else:
            initials = "{b}"+Name[:2].upper()+"{/b}"
            t = Text(initials, color="000000", size=45, align=(0.5,0.5))
            icon = Window(child=t,background=Frame("iconcircle",tile="integer"),ysize=90,xsize=90)
        h.add(Frame(icon,ysize=90,xsize=90))
        h.add(Null(width=10))
        h.add(Frame(ImageReference("leftwhitebubble"),ysize=90,xsize=45))
        h.add(w)
        h.add(Frame(ImageReference("rightwhitebubble"),ysize=90,xsize=45))
        # Only make one copy of icon visible in a row.
        if last_icon[0] == Name:
            last_icon[1].children[0] = Frame(ImageReference("blankicon"),ysize=90,xsize=90)
            last_icon[1].update()
        # Add message to the chat
        chat.add(h)
        # Add a bit of vertical spacing of texts.
        chat.add(Null(height=10))
        last_icon[0] = Name
        last_icon[1] = h
        # Record this message in the history.
        texting_history['history'].append((Name,msg))


# Modify character class to switch to texting mode when it's activated.
default textingmode = False
default text_pov = None
python early:
    orig_character_call = ADVCharacter.__call__
    def new_call (self, what, **kwargs):
        if not textingmode:
            return orig_character_call(self, what, **kwargs)
        elif self.name == text_pov:
            # Start typing animation
            images = renpy.game.context().images
            attrs = images.get_attributes(None, text_pov.lower())
            # Note: if "texting" attribute is not defined for the sprite,
            # and config.developer is True, then a small message about an
            # unknown attribute will show on the screen.
            # I assume this won't show up in the published version, since
            # then config.developer is set to False?
            renpy.exports.show((text_pov.lower(),)+attrs+("texting",))
            # Render the message
            sendertxt (self.name, what, **kwargs)
            # Stop typing animation
            renpy.exports.show((text_pov.lower(),)+attrs+("-texting",))
        else:
            othertxt (self.name, what, **kwargs)
    ADVCharacter.__call__ = new_call