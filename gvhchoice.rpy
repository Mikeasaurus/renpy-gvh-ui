transform menu_up:
    yanchor 1.0
    ypos 1.0 alpha 0.0
    easein 0.3 ypos 0.8 alpha 1.0

screen choice(items):
    window:
        background None
        yanchor 1.0 ypos 0.8
        at menu_up
        vbox:
            xalign 0.5
            spacing 30
            for n,i in enumerate(items):
                # Normal choice button
                if '->' not in i.caption:
                    hbox:
                        image "leftmenubutton"
                        frame:
                            background Frame("choice/centremenubutton.png",tile="integer",ysize=75)
                            textbutton i.caption action i.action text_size 40
                        image "rightmenubutton"
                # Button that statics out to other choice
                else:
                    hbox:
                        frame id "left_%d"%n:
                            xsize 38 ysize 75
                            background Frame(ImageReference("leftmenubutton"),ysize=75)
                            foreground Frame(ImageReference("leftmenubuttonstaticoff"),ysize=75)
                            null
                        frame id "centre_%d"%n:
                            background Frame("choice/centremenubutton.png",tile="integer",ysize=75)
                            fixed:
                                fit_first True
                                # Use first textbutton as dummy to keep the right size.
                                textbutton '{alpha=0.0}'+i.caption.split('->')[0].strip()+'{/alpha}' text_size 40
                                textbutton i.caption action i.action text_size 40 xalign 0.5
                            foreground Frame(ImageReference("centremenubuttonstaticoff"),tile=True,ysize=75)
                        frame id "right_%d"%n:
                            xsize 38 ysize 75
                            background Frame(ImageReference("rightmenubutton"),ysize=75)
                            foreground Frame(ImageReference("rightmenubuttonstaticoff"),ysize=75)
                            null
    python:
        def setup_dynamic_choices():
            from datetime import datetime, timedelta
            s = renpy.get_screen('choice')
            assert s is not None
            for n in range(10):
                left = renpy.get_widget(s,id='left_%d'%n)
                if left is None: continue
                centre = renpy.get_widget(s,id='centre_%d'%n)
                right = renpy.get_widget(s,id='right_%d'%n)
                fixed = centre.visit()[-1]
                button = fixed.visit()[-1]
                oldtext, newtext = button.child.text[0].split('->')
                def do_static (when=datetime.now()+timedelta(seconds=0.5),left=left,centre=centre,right=right,button=button,newtext=newtext,action=button.action):
                    if datetime.now() < when: return
                    # Turn on static foreground for button.
                    left_statics = left.visit()[1:-1:2]
                    centre_statics = centre.visit()[1:-1:2]
                    right_statics = right.visit()[1:-1:2]
                    for x in left_statics:
                        x.image = ImageReference("leftmenubuttonstaticfade")
                    left.update()
                    for x in centre_statics:
                        x.image = ImageReference("centremenubuttonstaticfade")
                    centre.update()
                    for x in right_statics:
                        x.image = ImageReference("rightmenubuttonstaticfade")
                    right.update()
                    # Update the text of the button.
                    button.child.text = [newtext]
                    button.child.update()
                    # Turn off this hover trigger (only one once).
                    button.hovered = None
                    # Turn on action after waiting for static.
                    def do_action (when=datetime.now()+timedelta(seconds=1)):
                        if datetime.now() >= when:
                            return action()
                    # Why is it that I need to set the 'clicked' attribute here
                    # to turn on an action, but I need to set the 'action'
                    # attribute to disable the button from outside this function?
                    button.clicked = do_action
                def do_nothing (): pass
                # Set hover trigger to turn on static and morph into final form.
                button.hovered = do_static
                button.action = do_nothing
                button.child.text = [oldtext.strip()]
    on "show" action setup_dynamic_choices


# Staticky buttons
image leftmenubuttonstatic:
    "leftmenubuttonstatic1"
    pause 0.05
    "leftmenubuttonstatic2"
    pause 0.05
    "leftmenubuttonstatic3"
    pause 0.05
    "leftmenubuttonstatic4"
    pause 0.05
    "leftmenubuttonstatic5"
    pause 0.05
    "leftmenubuttonstatic6"
    pause 0.05
    "leftmenubuttonstatic7"
    pause 0.05
    "leftmenubuttonstatic8"
    pause 0.05
    "leftmenubuttonstatic9"
    pause 0.05
    repeat
image leftmenubuttonstaticoff:
    alpha 0.0
    "leftmenubuttonstatic"
image leftmenubuttonstaticfade:
    alpha 1.0
    "leftmenubuttonstatic"
    easeout 1.0 alpha 0.0
image centremenubuttonstatic:
    "centremenubuttonstatic1"
    pause 0.05
    "centremenubuttonstatic2"
    pause 0.05
    "centremenubuttonstatic3"
    pause 0.05
    "centremenubuttonstatic4"
    pause 0.05
    "centremenubuttonstatic5"
    pause 0.05
    "centremenubuttonstatic6"
    pause 0.05
    "centremenubuttonstatic7"
    pause 0.05
    "centremenubuttonstatic8"
    pause 0.05
    "centremenubuttonstatic9"
    pause 0.05
    repeat
image centremenubuttonstaticoff:
    alpha 0.0  
    "centremenubuttonstatic"
image centremenubuttonstaticfade:
    alpha 1.0
    "centremenubuttonstatic"
    easeout 1.0 alpha 0.0
image rightmenubuttonstatic:
    "rightmenubuttonstatic1"
    pause 0.05
    "rightmenubuttonstatic2"
    pause 0.05
    "rightmenubuttonstatic3"
    pause 0.05
    "rightmenubuttonstatic4"
    pause 0.05
    "rightmenubuttonstatic5"
    pause 0.05
    "rightmenubuttonstatic6"
    pause 0.05
    "rightmenubuttonstatic7"
    pause 0.05
    "rightmenubuttonstatic8"
    pause 0.05
    "rightmenubuttonstatic9"
    pause 0.05
    repeat
image rightmenubuttonstaticoff:
    alpha 0.0
    "rightmenubuttonstatic"
image rightmenubuttonstaticfade:
    alpha 1.0
    "rightmenubuttonstatic"
    easeout 1.0 alpha 0.0
