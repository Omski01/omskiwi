import fabric # importing the base package
from fabric import Application # prepare the application class which manages multi-config setups
from fabric.widgets.box import Box # gets the Box class
from fabric.widgets.label import Label # gets the Label class
from fabric.widgets.window import Window # grabs the Window class from Fabric
from fabric.widgets.button import Button
from fabric import Fabricator
from fabric.widgets.datetime import DateTime
import os
import subprocess
from fabric.hyprland.widgets import get_hyprland_connection
from fabric.utils import exec_shell_command_async


def create_button(label_text, on_click:None):
    button = Button(
        label=label_text,
    )
    if on_click:
        button.connect("clicked", on_click)


    return button

user = os.getlogin()
user_label = Label(label=user)
#Not needed since using DateTime instead now
#date_label = Label(label="Loading date...")

#Define profile picture path
def get_profile_picture_path() -> str | None:
    path = os.path.expanduser("~/Pictures/falcon.jpg")
    if not os.path.exists(path):
        path = os.path.expanduser("~/.face")
    return path
            

if __name__ == "__main__":

#   Box containing the profile pic of the user
#   Is it possible to make it take profile pic of current user instead of having a set absolute path to a picture?

    profile_pic = Box(
            orientation="v",
            name="profile_pic",
            style=f'''
            background-image: url("file:///{get_profile_picture_path() or ""}");
            background-size: cover;
            min-width: 128px;
            min-height: 128px;
            border-radius: 50%;
            ''',
        )
    

#   Box containing the buttons for apps

    top_buttons = Box(
        spacing=28, # adds some spacing between the children
		orientation="h", # horizontal
		children=[
			Box(
				spacing=28,
				orientation="h",
                style=f'''
                font-size:20px;
                margin-bottom: 90px;
                ''',
				children=[
                    create_button("",lambda*_: exec_shell_command_async(f"alacritty")),
					create_button("", lambda*_: exec_shell_command_async(f"librewolf")),
					create_button("", lambda*_: exec_shell_command_async(f"librewolf")),
                    create_button("", lambda*_: exec_shell_command_async(f"dolphin"))
				],
			),
            Box(v_expand=True)
		],
	)

#   Not needed since using DateTime now

#    date_fabricator = Fabricator(
#		interval=500,
#		poll_from="date",
#		on_changed=lambda f, v: date_label.set_label(f"Current date: {v.strip()}"),
#	)
	
# Import DateTime and using it instead of the fabricator is more convenient, easier, looks better and makes the code cleaner.

    time_box = Box(
		h_align="start",
		orientation="v",
		spacing=10,
		css_classes=["time-box"],
		children=[
			DateTime(name="date-time")
		],
        
	)

#   Header box containing DateTime, welcome text
#   todo: add weather to the right of the welcome text

    header_box = Box(
		orientation="h",
		spacing=20,
        children=[
			time_box,
            Box(h_expand=True), #Left spacing box
            Label(label="Welcome, Pilot"),
            Box(h_expand=True), #Right spacing box
		],
	)



    profile_box = Box(
            orientation="v",
            spacing=5,
            children=[
                profile_pic,
                user_label
            ]
    )


#   Middle of the dashboard containing user, user pic and buttons (box_2 are the buttons)
#   todo: make the buttons functional and for apps
#   Is it possible to make it so it would take the user profile pic instead of a static/absolute path to a picture?

    middle_box = Box(
		orientation="h",
        spacing=20,
		children=[
			profile_box,
			top_buttons
		],
	)
    middle_box.reorder_child(user_label, 1),


#   Main box containing other boxes

    box_1 = Box(		
		orientation="v",
		spacing=20,
        style=f'padding:20px',
        anchor="center",
		children=[
			header_box,
			middle_box
		],
	)
			

#	def apply_stylesheet(*_):
#	    return app.set_stylesheet_from_file(
 #   	    get_relative_path("styles.css")
  # 	 )
#
	#style_monitor = monitor_file(get_relative_path("styles.css"))
	#style_monitor.connect("changed", apply_stylesheet)
	#apply_stylesheet() # initial styling


    box_1.add(time_box)# append box_3 inside box_1 along with the label already in there
    box_1.add(top_buttons)
    box_1.reorder_child(time_box, 0) # Move the time box to the top left corner
	

#   Window containing all boxes, the base so to say

    window = Window(
            padding=20,
            style=f'''
            padding:20px;
            font-family:JetBrainsMono Nerd Font Propo;
            ''',
            anchor="center",
            layer="overlay",
            exclusive=False,
            child=box_1
    ) # there's no need showing this window using `show_all()`; it'll show them itself because the children are already passed
		

    app = Application("default", window) # define a new config named "default" which holds `window`
    
    window.connect("destroy", lambda*_: app.quit()) # If destroyed (with super + q) then quit completely, otherwise it leaves the process running in the background and makes it unable to launch a new one

    app.run() # run the event loop (run the config)

