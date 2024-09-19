transform menu_up:
    yanchor 1.0
    ypos 1.0 alpha 0.0
    easein 0.3 ypos 0.8 alpha 1.0

# Internal state of buttons.
# Contains some integer value, starting at zero.
# The context depends on the type of button.
default choice_state = [0]*100
# For some buttons, need a timer to indicate when an action can be perfomed.
default choice_timer = [None]*100
# Queue up an action to perform after ending animation.
default action_queue = None

# Internal layout of choice buttons.
# Using this as a template, to cut down on the amount of copy/pasted layout
# in the choicebutton screen.
screen choicebutton_internal(choice_type, choice_text, choice_action, choice_hovered, choice_unhovered, fit_type=None, fit_text=None, button_transform=None, choice_ysize=75, fg=None, bg_tile="integer", textcolor="#777777"):
    fixed:
        fit_first True
        yalign 0.5
        # Invisible copy of button for forcing a certain layout.
        if fit_type is not None:
            ###
            # Dummy button layout for arranging the space for the button.
            # Requires fit_first to be turned on.
            hbox:
                yalign 0.5 xalign 0.5
                image "leftmenubutton%s"%(fit_type or choice_type) alpha 0.0
                frame:
                    background None
                    textbutton "%s"%(fit_text or choice_text) text_size 40 text_color "#00000000" text_hover_color "#00000000"
                image "rightmenubutton%s"%(fit_type or choice_type) alpha 0.0
        # Transformed background button
        if button_transform is not None:
            hbox:
                yalign 0.5 xalign 0.5
                at button_transform
                image "leftmenubutton%s"%choice_type
                frame:
                    background Frame(ImageReference("centremenubutton%s"%choice_type),tile="integer",ysize=choice_ysize)
                    textbutton "%s"%(fit_text or choice_text) text_size 40 text_color "#00000000" text_hover_color "#00000000"
                image "rightmenubutton%s"%choice_type
        # The main button.
        # Contains the text, and the background if no transform is applied.
        hbox:
            yalign 0.5 xalign 0.5
            if button_transform is not None:
                image "leftmenubutton%s"%choice_type alpha 0.0
            else:
                image "leftmenubutton%s"%choice_type
            frame:
                if button_transform is not None:
                    background None
                else:
                    if fg is not None:
                        foreground Frame(ImageReference(fg),tile=True,ysize=choice_ysize)
                    background Frame(ImageReference("centremenubutton%s"%choice_type),tile=bg_tile,ysize=choice_ysize)
                # Special case: use some other text to define the size.
                # Make it an invisible copy, and apply fit_first to it.
                if fit_text is not None:
                    fixed:
                        fit_first True
                        textbutton fit_text text_size 40 text_color "#00000000" text_hover_color "#00000000"
                        textbutton choice_text action choice_action text_size 40 xalign 0.5 text_color textcolor text_hover_color "#ffffff" hovered choice_hovered unhovered choice_unhovered
                else:
                    # Some questionable stuff to get vertical alignment of text consistent.
                    vbox:
                        null height (choice_ysize-75)/2
                        textbutton choice_text action choice_action text_size 40 text_color textcolor text_hover_color "#ffffff" hovered choice_hovered unhovered choice_unhovered
            if button_transform is not None:
                image "rightmenubutton%s"%choice_type alpha 0.0
            else:
                image "rightmenubutton%s"%choice_type


# Choice buttons are set up in a separate screen, to make it easier to place them
# in different layouts without copying / pasting a bunch of code.
# Inputs:
# n - index of choice (for labelling)
# i - choice item
# dx, dy - direction to point the central circle thing to indicate selection.
screen choicebutton(n,i,dx=0.0,dy=0.0):
    python:
        # These functions are called when a button gets hovered / unhovered.
        # Sets up the transformation of the central pointer, to slide towards
        # the hovered choice.
        def hovered_action (n,dx,dy):
            global choicepointer_dx1, choicepointer_dy1
            global choicepointer_dx2, choicepointer_dy2
            global selected_choice
            # Don't hover something else if something was clicked and we're
            # in the end-of-screen fadeout animation.
            if action_queue is not None: return
            # Under some conditions this seems to get called twice on a button.
            # Seems to happen for instance for buttons that have a transform
            # effect applied on hover.
            # Avoid double-setting this or it snaps the pointer instantly
            # instead of sliding.
            if dx != choicepointer_dx2 or dy != choicepointer_dy2:
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
            # Don't unhover if something was already clicked.
            if action_queue is not None: return
            choicepointer_dx1 = choicepointer_dx2
            choicepointer_dy1 = choicepointer_dy2
            choicepointer_dx2 = 0.0
            choicepointer_dy2 = 0.0
            selected_choice = None
            renpy.restart_interaction()
        # Make the click response wait for an animation before returning from
        # this screen.
        def clicked (i=i):
            # Can't pause and then call the action here directly, because Ren'Py
            # "Cannot start an interaction in the middle of an interaction"...
            # so this kludge sets up the action to be called as part of the screen
            # setup.
            global action_queue
            # If an action was already clicked, then can't click again.
            if action_queue is not None: return
            action_queue = i.action
            renpy.restart_interaction()
        # Increment choice state for multi-stage buttons.
        def inc_state (n):
            global choice_state
            choice_state[n] += 1
            renpy.restart_interaction()
        # Action that does nothing.  For buttons that are disabled, but still need
        # hover actions to work.  Putting action of None seems to disable hover,
        # so this will keep hover working?
        def do_nothing ():
            return
        # Action that sets a timer to delay further action.
        # Works in conjunction with delayed_action.
        def set_delay (delay,n=n):
            def f(n=n,delay=delay):
                from datetime import datetime, timedelta
                timer = datetime.now()+timedelta(seconds=delay)
                choice_timer[n] = timer
            return f
        # Conditional action, if a time has been reached.
        def delayed_action (action_,n=n):
            def f(n=n,action_=action_):
                from datetime import datetime, timedelta
                if choice_timer[n] is not None and datetime.now() > choice_timer[n]:
                    return action_()
            return f
    default hovered_ = Function(hovered_action,n,dx,dy)
    default unhovered_ = unhovered_action
    default inc_state_ = Function(inc_state,n)
    # Button that statics out to other choice
    if '->' in i.caption:
        default caption1 = i.caption.split('->')[0].strip()
        default caption2 = i.caption.split('->')[1].strip()
        # Hide after clicking (if not selected)
        if action_queue is not None and selected_choice != n:
            pass
        # Add outline effect if it was just clicked.
        elif action_queue is not None  and selected_choice == n:
            use choicebutton_internal("outline", caption2, do_nothing, hovered_, unhovered_, button_transform=buttonexpanding, fit_type="", fit_text=caption1)
        # First, present normal-looking button with some initial choice text.
        elif choice_state[n] == 0:
            use choicebutton_internal("", caption1, do_nothing, [hovered_,inc_state_,set_delay(1.0)], unhovered_)
        # After getting hovered, show a staticky button
        elif choice_state[n] == 1:
            fixed:
                fit_first True
                # Normal button in the back.
                if selected_choice == n:
                    use choicebutton_internal("selected", caption2, delayed_action(clicked), hovered_, unhovered_, fit_text=caption1, textcolor="#ffffff")
                else:
                    use choicebutton_internal("", caption2, delayed_action(clicked), hovered_, unhovered_, fit_text=caption1)
                # Staticky button in front.
                use choicebutton_internal("staticfade", "{alpha=0.0}"+caption1+"{/alpha}", None, hovered_, unhovered_, bg_tile=True)
    # Wobbly button
    elif i.caption.startswith('~') and i.caption.endswith('~'):
        default caption = i.caption.strip('~').strip()
        # Hide after clicking (if not selected)
        if action_queue is not None and selected_choice != n:
            pass
        # Add outline effect if it was just clicked.
        elif action_queue is not None  and selected_choice == n:
            use choicebutton_internal("wobblyoutline", caption, do_nothing, hovered_, unhovered_, button_transform=buttonexpanding, choice_ysize=79, fit_type="wobbly")
        elif selected_choice == n:
            use choicebutton_internal("wobblyselected", caption, clicked, hovered_, unhovered_, choice_ysize=79)
        else:
            use choicebutton_internal("wobbly", caption, clicked, hovered_, unhovered_, choice_ysize=79)
    # Parallelogram button
    elif i.caption.startswith('/') and i.caption.endswith('/'):
        default caption = i.caption.strip('/').strip()
        # Hide after clicking (if not selected)
        if action_queue is not None and selected_choice != n:
            pass
        # Add outline effect if it was just clicked.
        elif action_queue is not None  and selected_choice == n:
            use choicebutton_internal("pgramoutline", caption, do_nothing, hovered_, unhovered_, button_transform=buttonexpanding, fit_type="pgram")
        elif selected_choice == n:
            use choicebutton_internal("pgramselected", caption, clicked, hovered_, unhovered_, button_transform=oscillation, fit_type="pgram")
        else:
            use choicebutton_internal("pgram", caption, clicked, hovered_, unhovered_)
    # Pulsing button
    elif i.caption.startswith('((') and i.caption.endswith('))'):
        default caption = i.caption.lstrip('(').rstrip(')').strip()
        # Hide after clicking (if not selected)
        if action_queue is not None and selected_choice != n:
            pass
        # Add outline effect if it was just clicked.
        elif action_queue is not None  and selected_choice == n:
            use choicebutton_internal("outline", caption, do_nothing, hovered_, unhovered_, button_transform=buttonexpanding, fit_type="")
        elif selected_choice == n:
            use choicebutton_internal("selected", caption, clicked, hovered_, unhovered_, button_transform=thumping, fit_type="")
        else:
            use choicebutton_internal("", caption, clicked, hovered_, unhovered_)
    # Sparkly button
    elif i.caption.startswith('*') and i.caption.endswith('*'):
        default caption = i.caption.strip('*').strip()
        # Hide after clicking (if not selected)
        if action_queue is not None and selected_choice != n:
            pass
        # Add outline effect if it was just clicked.
        elif action_queue is not None  and selected_choice == n:
            use choicebutton_internal("outline", caption, do_nothing, hovered_, unhovered_, button_transform=buttonexpanding, fit_type="")
        elif selected_choice == n:
            use choicebutton_internal("selected", caption, clicked, hovered_, unhovered_, fg="centremenubuttonsparkly animated")
        else:
            use choicebutton_internal("", caption, clicked, hovered_, unhovered_, fg="centremenubuttonsparkly animated")
    # Spikey button
    elif i.caption.startswith('^') and i.caption.endswith('^'):
        default caption = i.caption.strip('^').strip()
        # Hide after clicking (if not selected)
        if action_queue is not None and selected_choice != n:
            pass
        # Add outline effect if it was just clicked.
        elif action_queue is not None  and selected_choice == n:
            use choicebutton_internal("spikeyoutline", caption, do_nothing, hovered_, unhovered_, button_transform=buttonexpanding, choice_ysize=115, fit_type="selected")
        elif selected_choice == n:
            use choicebutton_internal("spikeyselected", caption, clicked, hovered_, unhovered_, choice_ysize=115, fit_type="selected")
        else:
            use choicebutton_internal("spikeyunselected", caption, clicked, hovered_, unhovered_, choice_ysize=115, fit_type="selected")
    # Normal button
    else:
        # Hide after clicking (if not selected)
        if action_queue is not None and selected_choice != n:
            pass
        # Add outline effect if it was just clicked.
        elif action_queue is not None  and selected_choice == n:
            use choicebutton_internal("outline", i.caption, do_nothing, hovered_, unhovered_, button_transform=buttonexpanding, fit_type="")
        elif selected_choice == n:
            use choicebutton_internal("selected", i.caption, clicked, hovered_, unhovered_)
        else:
            use choicebutton_internal("", i.caption, clicked, hovered_, unhovered_)
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
            # Regular pointer during selection prompt
            if action_queue is None:
                image "menupointer" at slide(choicepointer_dx1,choicepointer_dy1,choicepointer_dx2,choicepointer_dy2)
            # After clicking, make it an expanding outline.
            else:
                image "menupointeroutline expanding" at slide(choicepointer_dx2,choicepointer_dy2,choicepointer_dx2,choicepointer_dy2)
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
        # Set up choice button state.
        def start():
            global selected_choice, choice_state, choice_timer, action_queue
            selected_choice = None
            choice_state = [0]*100
            choice_timer = [None]*100
            action_queue = None
    if action_queue is not None:
        timer 0.2 action action_queue
    on "show" action start
    
# Pointer after clicking an option
image menupointeroutline expanding:
    "menupointeroutline"
    zoom 1.0 alpha 1.0
    linear 0.1 zoom 1.5 alpha 0.0
# Choice button after being clicked
transform buttonexpanding:
    zoom 1.0 alpha 1.0
    linear 0.1 zoom 1.5 alpha 0.0


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
image leftmenubuttonwobblyselected:
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
image centremenubuttonwobblyselected:
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
image rightmenubuttonwobblyselected:
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
    easein 0.5 rotate -10.0
    easeout 0.5 rotate 0.0
    easein 0.5 rotate 10.0
    easeout 0.5 rotate 0.0
    repeat
transform thumping:
    xalign 0.5
    easeout 0.1 zoom 1.4
    easein 0.1 zoom 1.0
    pause 0.2
    repeat
image centremenubuttonsparkly animated:
    animation
    "centremenubuttonsparkly"
    xalign 0.5 yalign 0.5
    crop (0,0,300,75)
    linear 10.0 crop (0,299,300,75)
    repeat
# Parallelogram button uses same middle section as normal button.
image centremenubuttonpgram:
    "centremenubutton"
image centremenubuttonpgramselected:
    "centremenubuttonselected"
image centremenubuttonpgramoutline:
    "centremenubuttonoutline"
image leftmenubuttonspikeyselected:
    "leftmenubuttonspikeyselected1"
    pause 0.02
    "leftmenubuttonspikeyselected2"
    pause 0.02
    "leftmenubuttonspikeyselected3"
    pause 0.02
    "leftmenubuttonspikeyselected4"
    pause 0.02
    "leftmenubuttonspikeyselected5"
    pause 0.02
    "leftmenubuttonspikeyselected6"
    pause 0.02
    "leftmenubuttonspikeyselected7"
    pause 0.02
    "leftmenubuttonspikeyselected8"
    pause 0.02
    "leftmenubuttonspikeyselected9"
    pause 0.02
image centremenubuttonspikeyselected:
    "centremenubuttonspikeyselected1"
    pause 0.02
    "centremenubuttonspikeyselected2"
    pause 0.02
    "centremenubuttonspikeyselected3"
    pause 0.02
    "centremenubuttonspikeyselected4"
    pause 0.02
    "centremenubuttonspikeyselected5"
    pause 0.02
    "centremenubuttonspikeyselected6"
    pause 0.02
    "centremenubuttonspikeyselected7"
    pause 0.02
    "centremenubuttonspikeyselected8"
    pause 0.02
    "centremenubuttonspikeyselected9"
    pause 0.02
image rightmenubuttonspikeyselected:
    "rightmenubuttonspikeyselected1"
    pause 0.02
    "rightmenubuttonspikeyselected2"
    pause 0.02
    "rightmenubuttonspikeyselected3"
    pause 0.02
    "rightmenubuttonspikeyselected4"
    pause 0.02
    "rightmenubuttonspikeyselected5"
    pause 0.02
    "rightmenubuttonspikeyselected6"
    pause 0.02
    "rightmenubuttonspikeyselected7"
    pause 0.02
    "rightmenubuttonspikeyselected8"
    pause 0.02
    "rightmenubuttonspikeyselected9"
    pause 0.02
image leftmenubuttonspikeyunselected:
    "leftmenubuttonspikey7"
    pause 0.05
    "leftmenubuttonspikey6"
    pause 0.02
    "leftmenubuttonspikey5"
    pause 0.02
    "leftmenubuttonspikey4"
    pause 0.02
    "leftmenubuttonspikey3"
    pause 0.02
    "leftmenubuttonspikey2"
    pause 0.02
    "leftmenubuttonspikey1"
    pause 0.02
image centremenubuttonspikeyunselected:
    "centremenubuttonspikey7"
    pause 0.05
    "centremenubuttonspikey6"
    pause 0.02
    "centremenubuttonspikey5"
    pause 0.02
    "centremenubuttonspikey4"
    pause 0.02
    "centremenubuttonspikey3"
    pause 0.02
    "centremenubuttonspikey2"
    pause 0.02
    "centremenubuttonspikey1"
    pause 0.02
image rightmenubuttonspikeyunselected:
    "rightmenubuttonspikey7"
    pause 0.05
    "rightmenubuttonspikey6"
    pause 0.02
    "rightmenubuttonspikey5"
    pause 0.02
    "rightmenubuttonspikey4"
    pause 0.02
    "rightmenubuttonspikey3"
    pause 0.02
    "rightmenubuttonspikey2"
    pause 0.02
    "rightmenubuttonspikey1"
    pause 0.02
