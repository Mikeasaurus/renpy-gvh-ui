transform menu_up:
    yanchor 1.0
    ypos 1.0 alpha 0.0
    easein 0.3 ypos 0.8 alpha 1.0

# Choice buttons are set up in a separate screen, to make it easier to place them
# in different layouts without copying / pasting a bunch of code.
# Inputs:
# n - index of choice (for labelling)
# i - choice item
# dx, dy - direction to point the central circle thing to indicate selection.
# x_align - alignment along x direction
screen choicebutton(n,i,dx=0.0,dy=0.0,x_align=0.5):
    python:
        # These functions are called when a button gets hovered / unhovered.
        # Sets up the transformation of the central pointer, to slide towards
        # the hovered choice.
        def hovered_action (n,dx,dy):
            global choicepointer_dx1, choicepointer_dy1
            global choicepointer_dx2, choicepointer_dy2
            global selected_choice
            choicepointer_dx1 = choicepointer_dx2
            choicepointer_dy1 = choicepointer_dy2
            choicepointer_dx2 = dx
            choicepointer_dy2 = dy
            selected_choice = n
            renpy.restart_interaction()
        def unhovered_action ():
            global choicepointer_dx1, choicepointer_dy1
            global choicepointer_dx2, choicepointer_dy2
            global selected_choice
            choicepointer_dx1 = choicepointer_dx2
            choicepointer_dy1 = choicepointer_dy2
            choicepointer_dx2 = 0.0
            choicepointer_dy2 = 0.0
            selected_choice = None
            renpy.restart_interaction()
    # Button that statics out to other choice
    if '->' in i.caption:
        hbox:
            yalign 0.5 xalign x_align
            frame id "left_%d"%n:
                xsize 38 ysize 75
                if selected_choice == n:
                    background Frame(ImageReference("leftmenubuttonselected"),ysize=75)
                else:
                    background Frame(ImageReference("leftmenubutton"),ysize=75)
                foreground Frame(ImageReference("leftmenubuttonstaticoff"),ysize=75)
                null
            frame id "centre_%d"%n:
                if selected_choice == n:
                    background Frame(ImageReference("centremenubuttonselected"),tile="integer",ysize=75)
                else:
                    background Frame(ImageReference("centremenubutton"),tile="integer",ysize=75)
                fixed:
                    fit_first True
                    # Use first textbutton as dummy to keep the right size.
                    # Also store the usual hovered / unhovered actions here.
                    textbutton '{alpha=0.0}'+i.caption.split('->')[0].strip()+'{/alpha}' text_size 40 hovered Function(hovered_action,n,dx,dy) unhovered unhovered_action
                    # Can't put the 'hovered' and 'unhovered' attributes in here, otherwise it
                    # won't let them change later (will keep calling the same function even though
                    # it was changed in the object)
                    # However, if those attributes are left out here, then they can be dynamically
                    # added later, and even changing them again later works fine???
                    # WTF, Ren'Py.
                    textbutton i.caption action i.action text_size 40 xalign 0.5 text_color "#777777" text_hover_color "#ffffff"
                foreground Frame(ImageReference("centremenubuttonstaticoff"),tile=True,ysize=75)
            frame id "right_%d"%n:
                xsize 38 ysize 75
                if selected_choice == n:
                    background Frame(ImageReference("rightmenubuttonselected"),ysize=75)
                else:
                    background Frame(ImageReference("rightmenubutton"),ysize=75)
                foreground Frame(ImageReference("rightmenubuttonstaticoff"),ysize=75)
                null
    # Wobbly button
    elif i.caption.startswith('~') and i.caption.endswith('~'):
        hbox:
            yalign 0.5 xalign x_align
            if selected_choice == n:
                image "leftmenubuttonwobbly selected"
            else:
                image "leftmenubuttonwobbly"
            frame:
                if selected_choice == n:
                    background Frame(ImageReference("centremenubuttonwobbly selected"),tile="integer",ysize=79)
                else:
                    background Frame(ImageReference("centremenubuttonwobbly"),tile="integer",ysize=79)
                textbutton i.caption.strip('~').strip() action i.action text_size 40 text_color "#777777" text_hover_color "#ffffff" hovered Function(hovered_action,n,dx,dy) unhovered unhovered_action
            if selected_choice == n:
                image "rightmenubuttonwobbly selected"
            else:
                image "rightmenubuttonwobbly"
    # Parallelogram button
    elif i.caption.startswith('/') and i.caption.endswith('/'):
        fixed:
            yalign 0.5 xalign x_align
            # Put wobbly parallelogram behind the text.
            if selected_choice == n:
                hbox:
                    yalign 0.5 #xalign 0.5
                    at oscillation
                    image "leftmenubuttonpgramselected"
                    frame:
                        background Frame(ImageReference("centremenubuttonselected"),tile="integer",ysize=75)
                        textbutton i.caption.strip('/').strip() text_size 40 text_color "#00000000"
                    image "rightmenubuttonpgramselected"
            hbox:
                yalign 0.5
                if selected_choice == n:
                    image "leftmenubuttonpgram" alpha 0.0
                else:
                    image "leftmenubuttonpgram"
                frame:
                    if selected_choice == n:
                        background None
                        #background Frame(ImageReference("centremenubuttonselected"),tile="integer",ysize=75)
                    else:
                        background Frame(ImageReference("centremenubutton"),tile="integer",ysize=75)
                    textbutton i.caption.strip('/').strip() action i.action text_size 40 text_color "#777777" text_hover_color "#ffffff" hovered Function(hovered_action,n,dx,dy) unhovered unhovered_action
                if selected_choice == n:
                    image "rightmenubuttonpgram" alpha 0.0
                else:
                    image "rightmenubuttonpgram"

    # Normal choice button
    else:
        hbox:
            yalign 0.5 xalign x_align
            if selected_choice == n:
                image "leftmenubuttonselected"
            else:
                image "leftmenubutton"
            frame:
                if selected_choice == n:
                    background Frame(ImageReference("centremenubuttonselected"),tile="integer",ysize=75)
                else:
                    background Frame(ImageReference("centremenubutton"),tile="integer",ysize=75)
                textbutton i.caption action i.action text_size 40 text_color "#777777" text_hover_color "#ffffff" hovered Function(hovered_action,n,dx,dy) unhovered unhovered_action
            if selected_choice == n:
                image "rightmenubuttonselected"
            else:
                image "rightmenubutton"
# Setting up the choice pointer.
default choicepointer_dx1 = 0.0
default choicepointer_dy1 = 0.0
default choicepointer_dx2 = 0.0
default choicepointer_dy2 = 0.0
default selected_choice = None
# The tranform for sliding the choice pointer to the selected choice.
transform slide(dx1,dy1,dx2,dy2):
    xpos 0.5 ypos 0.5
    xanchor 0.5-dx1/3 yanchor 0.5-dy1/3
    ease 0.1 xanchor 0.5-dx2/3 yanchor 0.5-dy2/3

# The main screen layout for choices.
screen choice(items):
    window:
        background None
        yanchor 1.0 ypos 0.8
        at menu_up
        if len(items) <= 6:
            image "menupointer" at slide(choicepointer_dx1,choicepointer_dy1,choicepointer_dx2,choicepointer_dy2)
        if len(items) == 1:
            vbox:
                xalign 0.5 yanchor 0.0 ypos 0.5
                null height 45+30
                use choicebutton(0,items[0],0.0,1.0)
        elif len(items) == 2:
            hbox:
                xanchor 1.0 xpos 0.5 yalign 0.5
                use choicebutton(0,items[0],-1.0,0.0)
                null width 45+30
            hbox:
                xanchor 0.0 xpos 0.5 yalign 0.5
                null width 45+30
                use choicebutton(1,items[1],1.0,0.0)
        elif len(items) == 3:
            hbox:
                xanchor 1.0 xpos 0.5 yalign 0.5
                use choicebutton(0,items[0],-1.0,0.0)
                null width 45+30
            hbox:
                xanchor 0.0 xpos 0.5 yalign 0.5
                null width 45+30
                use choicebutton(1,items[1],1.0,0.0)
            vbox:
                xalign 0.5 yanchor 0.0 ypos 0.5
                null height 45+30
                use choicebutton(2,items[2],0.0,1.0)
        elif len(items) == 4:
            vbox:
                xalign 0.5 yanchor 1.0 ypos 0.5
                use choicebutton(0,items[0],0.0,-1.0)
                null height 45+30
            hbox:
                xanchor 1.0 xpos 0.5 yalign 0.5
                use choicebutton(1,items[1],-1.0,0.0)
                null width 45+30
            hbox:
                xanchor 0.0 xpos 0.5 yalign 0.5
                null width 45+30
                use choicebutton(2,items[2],1.0,0.0)
            vbox:
                xalign 0.5 yanchor 0.0 ypos 0.5
                null height 45+30
                use choicebutton(3,items[3],0.0,1.0)
        elif len(items) == 5:
            vbox:
                xalign 0.5 yanchor 1.0 ypos 0.5
                hbox:
                    xanchor 1.0 xpos 0.5 yalign 0.5
                    use choicebutton(0,items[0],-0.5,-1.2)
                    null width 15
                null height 45+30
            vbox:
                xalign 0.5 yanchor 1.0 ypos 0.5
                hbox:
                    xanchor 0.0 xpos 0.5 yalign 0.5
                    null width 15
                    use choicebutton(1,items[1],0.5,-1.2)
                null height 45+30
            hbox:
                xanchor 1.0 xpos 0.5 yalign 0.5
                use choicebutton(2,items[2],-1.0,0.0)
                null width 45+30
            hbox:
                xanchor 0.0 xpos 0.5 yalign 0.5
                null width 45+30
                use choicebutton(3,items[3],1.0,0.0)
            vbox:
                xalign 0.5 yanchor 0.0 ypos 0.5
                null height 45+30
                use choicebutton(4,items[4],0.0,1.0)
        elif len(items) == 6:
            vbox:
                xalign 0.5 yanchor 1.0 ypos 0.5
                hbox:
                    xanchor 1.0 xpos 0.5 yalign 0.5
                    use choicebutton(0,items[0],-0.5,-1.2)
                    null width 15
                null height 45+30
            vbox:
                xalign 0.5 yanchor 1.0 ypos 0.5
                hbox:
                    xanchor 0.0 xpos 0.5 yalign 0.5
                    null width 15
                    use choicebutton(1,items[1],0.5,-1.2)
                null height 45+30
            hbox:
                xanchor 1.0 xpos 0.5 yalign 0.5
                use choicebutton(2,items[2],-1.0,0.0)
                null width 45+30
            hbox:
                xanchor 0.0 xpos 0.5 yalign 0.5
                null width 45+30
                use choicebutton(3,items[3],1.0,0.0)
            vbox:
                xalign 0.5 yanchor 0.0 ypos 0.5
                null height 45+30
                hbox:
                    xanchor 1.0 xpos 0.5 yalign 0.5
                    use choicebutton(4,items[4],-0.5,1.2)
                    null width 15
            vbox:
                xalign 0.5 yanchor 0.0 ypos 0.5
                null height 45+30
                hbox:
                    xanchor 0.0 xpos 0.5 yalign 0.5
                    null width 15
                    use choicebutton(5,items[5],0.5,1.2)

        # If all else fails, just list the choices
        else:
            vbox:
                xalign 0.5 yalign 0.8
                spacing 30
                for n,i in enumerate(items):
                    use choicebutton(n,i)
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
                # First button holds hovered / unhovered actions.
                # Copy them to second (main) button because that one takes
                # precedent for mouse actions.
                dummy_button = fixed.visit()[0]
                button = fixed.visit()[-1]
                oldtext, newtext = button.child.text[0].split('->')
                def do_static (when=datetime.now()+timedelta(seconds=0.5),left=left,centre=centre,right=right,dummy_button=dummy_button,button=button,newtext=newtext,action=button.action):
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
                    # Use normal hover action after waiting for static.
                    def do_hovered (when=datetime.now()+timedelta(seconds=1)):
                        if datetime.now() >= when:
                            return dummy_button.hovered()
                    button.hovered = do_hovered
                    # Turn on action after waiting for static.
                    def do_action (when=datetime.now()+timedelta(seconds=1)):
                        if datetime.now() >= when:
                            return action()
                    # Why is it that I need to set the 'clicked' attribute here
                    # to turn on an action, but I need to set the 'action'
                    # attribute to disable the button from outside this function?
                    button.clicked = do_action
                    button.action = do_action
                def do_nothing (): pass
                # Set hover trigger to turn on static and morph into final form.
                button.hovered = do_static
                button.unhovered = dummy_button.unhovered
                button.action = do_nothing
                button.child.text = [oldtext.strip()]
        # Reset any state after the screen is done, so it behaves properly
        # for the next time it's shown.
        def finish():
            global selected_choice
            selected_choice = None
    on "show" action [SetVariable("selected_choice",None), setup_dynamic_choices]
    on "hide" action finish


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
image leftmenubuttonwobbly:
    animation
    "leftmenubuttonwobbly0"
    pause 0.1
    "leftmenubuttonwobbly1"
    pause 0.1
    "leftmenubuttonwobbly2"
    pause 0.1
    "leftmenubuttonwobbly3"
    pause 0.1
    "leftmenubuttonwobbly4"
    pause 0.1
    "leftmenubuttonwobbly5"
    pause 0.1
    "leftmenubuttonwobbly6"
    pause 0.1
    "leftmenubuttonwobbly7"
    pause 0.1
    "leftmenubuttonwobbly8"
    pause 0.1
    "leftmenubuttonwobbly9"
    pause 0.1
    repeat
image centremenubuttonwobbly:
    animation
    "centremenubuttonwobbly0"
    pause 0.1
    "centremenubuttonwobbly1"
    pause 0.1
    "centremenubuttonwobbly2"
    pause 0.1
    "centremenubuttonwobbly3"
    pause 0.1
    "centremenubuttonwobbly4"
    pause 0.1
    "centremenubuttonwobbly5"
    pause 0.1
    "centremenubuttonwobbly6"
    pause 0.1
    "centremenubuttonwobbly7"
    pause 0.1
    "centremenubuttonwobbly8"
    pause 0.1
    "centremenubuttonwobbly9"
    pause 0.1
    repeat
image rightmenubuttonwobbly:
    animation
    "rightmenubuttonwobbly0"
    pause 0.1
    "rightmenubuttonwobbly1"
    pause 0.1
    "rightmenubuttonwobbly2"
    pause 0.1
    "rightmenubuttonwobbly3"
    pause 0.1
    "rightmenubuttonwobbly4"
    pause 0.1
    "rightmenubuttonwobbly5"
    pause 0.1
    "rightmenubuttonwobbly6"
    pause 0.1
    "rightmenubuttonwobbly7"
    pause 0.1
    "rightmenubuttonwobbly8"
    pause 0.1
    "rightmenubuttonwobbly9"
    pause 0.1
    repeat
image leftmenubuttonwobbly selected:
    animation
    "leftmenubuttonwobblyselected0"
    pause 0.1
    "leftmenubuttonwobblyselected1"
    pause 0.1
    "leftmenubuttonwobblyselected2"
    pause 0.1
    "leftmenubuttonwobblyselected3"
    pause 0.1
    "leftmenubuttonwobblyselected4"
    pause 0.1
    "leftmenubuttonwobblyselected5"
    pause 0.1
    "leftmenubuttonwobblyselected6"
    pause 0.1
    "leftmenubuttonwobblyselected7"
    pause 0.1
    "leftmenubuttonwobblyselected8"
    pause 0.1
    "leftmenubuttonwobblyselected9"
    pause 0.1
    repeat
image centremenubuttonwobbly selected:
    animation
    "centremenubuttonwobblyselected0"
    pause 0.1
    "centremenubuttonwobblyselected1"
    pause 0.1
    "centremenubuttonwobblyselected2"
    pause 0.1
    "centremenubuttonwobblyselected3"
    pause 0.1
    "centremenubuttonwobblyselected4"
    pause 0.1
    "centremenubuttonwobblyselected5"
    pause 0.1
    "centremenubuttonwobblyselected6"
    pause 0.1
    "centremenubuttonwobblyselected7"
    pause 0.1
    "centremenubuttonwobblyselected8"
    pause 0.1
    "centremenubuttonwobblyselected9"
    pause 0.1
    repeat
image rightmenubuttonwobbly selected:
    animation
    "rightmenubuttonwobblyselected0"
    pause 0.1
    "rightmenubuttonwobblyselected1"
    pause 0.1
    "rightmenubuttonwobblyselected2"
    pause 0.1
    "rightmenubuttonwobblyselected3"
    pause 0.1
    "rightmenubuttonwobblyselected4"
    pause 0.1
    "rightmenubuttonwobblyselected5"
    pause 0.1
    "rightmenubuttonwobblyselected6"
    pause 0.1
    "rightmenubuttonwobblyselected7"
    pause 0.1
    "rightmenubuttonwobblyselected8"
    pause 0.1
    "rightmenubuttonwobblyselected9"
    pause 0.1
    repeat
transform oscillation:
    rotate 0.0
    easein 1.0 rotate -10.0
    easeout 1.0 rotate 0.0
    easein 1.0 rotate 10.0
    easeout 1.0 rotate 0.0
    repeat
