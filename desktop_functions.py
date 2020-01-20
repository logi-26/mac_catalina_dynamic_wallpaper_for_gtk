import os
import sys
import subprocess
from textwrap import dedent


###########################################################################
def is_running(process):
    try:
        s = subprocess.Popen(['ps', 'axw'], stdout=subprocess.PIPE)
    except: 
        pass
    process_list, err = s.communicate()
    return process in str(process_list)
###########################################################################


###########################################################################
def is_environment_gtk(desktop_env):
    gtk_desktops = ['budgie', 'cinnamon', 'gnome', 'gnome2', 'lxde', 'mate', 'unity', 'pantheon', 'sugar', 'xfce', 'xfce4']
    return desktop_env in gtk_desktops
###########################################################################


###########################################################################
def get_desktop_environment():
    
    # Windows and Mac
    if sys.platform in ['win32', 'cygwin']:
        return 'windows'
    elif sys.platform == 'darwin':
        return 'mac'

	# Linux
    else:
		# Get the desktop session
        desktop_session = os.environ.get('XDG_CURRENT_DESKTOP') or os.environ.get('DESKTOP_SESSION')

		# Try to determine desktop version using the desktop session
        if desktop_session is not None:
            desktop_session = desktop_session.lower()
            
            # Fix for X-Cinnamon etc
            if desktop_session.startswith('x-'):
                desktop_session = desktop_session.replace('x-', '')

            if desktop_session in ['gnome', 'unity', 'cinnamon', 'mate', 'xfce4', 'lxde', 'fluxbox', 'blackbox', 'openbox', 'icewm', 'jwm', 'afterstep', 'trinity', 'kde', 'pantheon', 'i3', 'lxqt', 'awesome']:
                return desktop_session
            elif 'xfce' in desktop_session or desktop_session.startswith('xubuntu'):
                return 'xfce4'
            elif desktop_session.startswith('ubuntu') or desktop_session.startswith('unity'):
                return 'unity'
            elif desktop_session.startswith('lubuntu'):
                return 'lxde'
            elif desktop_session.startswith('kubuntu'):
                return 'kde'
            elif desktop_session.startswith('razor'):
                return 'razor-qt'
            elif desktop_session.startswith('wmaker'):
                return 'windowmaker'

		# Try to determine desktop version using the os environment
        if os.environ.get('KDE_FULL_SESSION') == 'true':
            return 'kde'
        elif os.environ.get('GNOME_DESKTOP_SESSION_ID'):
            if not 'deprecated' in os.environ.get('GNOME_DESKTOP_SESSION_ID'):
                return 'gnome2'
        elif is_running('xfce-mcs-manage'):
            return 'xfce4'
        elif is_running('ksmserver'):
            return 'kde'

    return 'unknown'
###########################################################################


###########################################################################
def set_wallpaper(image, desktop_env):

	# gnome, unity, cinnamon, pantheon
    if desktop_env in ['gnome', 'unity', 'cinnamon', 'pantheon']:
        uri = 'file://%s' % image
        try:
            from gi.repository import Gio
            SCHEMA = 'org.gnome.desktop.background'
            KEY = 'picture-uri'
            gsettings = Gio.Settings.new(SCHEMA)
            gsettings.set_string(KEY, uri)
        except:
            args = ['gsettings', 'set', 'org.gnome.desktop.background', 'picture-uri', uri]
            subprocess.Popen(args)
	
	# mate
    elif desktop_env == 'mate':
        try:  # MATE >= 1.6
            args = ['gsettings', 'set', 'org.mate.background', 'picture-filename', '%s' % image]
            subprocess.Popen(args)
        except:  # MATE < 1.6
            args = ['mateconftool-2', '-t', 'string', '--set', '/desktop/mate/background/picture_filename', %s' % image]
            subprocess.Popen(args)
	
	# gnome2
    elif desktop_env == 'gnome2':
        args = ['gconftool-2', '-t', 'string', '--set', '/desktop/gnome/background/picture_filename', '%s' % image]
        subprocess.Popen(args)
	
	# Xfce4
    elif desktop_env == 'xfce4':
        list_of_properties_cmd = subprocess.Popen(['bash -c "xfconf-query -R -l -c xfce4-desktop -p /backdrop"'], shell=True, stdout=subprocess.PIPE)
        list_of_properties, list_of_properties_err = list_of_properties_cmd.communicate()
        list_of_properties = list_of_properties.decode('utf-8')
        for i in list_of_properties.split('\n'):
            if i.endswith('last-image'):
                subprocess.Popen(
                    ['xfconf-query -c xfce4-desktop -p %s -s "%s"' % (i, image)],
                    shell=True)
                subprocess.Popen(['xfdesktop --reload'], shell=True)
               
	# fluxbox, jwm, openbox, afterstep
    elif desktop_env in ['fluxbox', 'jwm', 'openbox', 'afterstep', 'i3']:
        try:
            args = ['feh', '--bg-scale', image]
            subprocess.Popen(args)
        except:
            sys.stderr.write('Error: Failed to set wallpaper with feh!')
            sys.stderr.write('Please make sre that You have feh installed.')
	
	# icewm
    elif desktop_env == 'icewm':
        args = ['icewmbg', image]
        subprocess.Popen(args)
	
	# blackbox
    elif desktop_env == 'blackbox':
        args = ['bsetbg', '-full', image]
        subprocess.Popen(args)
	
	# lxde
    elif desktop_env == 'lxde':
        args = 'pcmanfm --set-wallpaper %s --wallpaper-mode=scaled' % image
        subprocess.Popen(args, shell=True)
	
	# lxqt
    elif desktop_env == 'lxqt':
        args = 'pcmanfm-qt --set-wallpaper %s --wallpaper-mode=scaled' % image
        subprocess.Popen(args, shell=True)
	
	# windowmaker
    elif desktop_env == 'windowmaker':
        args = 'wmsetbg -s -u %s' % image
        subprocess.Popen(args, shell=True)
	
	# enlightenment
    elif desktop_env == 'enlightenment':
        args = 'enlightenment_remote -desktop-bg-add 0 0 0 0 %s' % image
        subprocess.Popen(args, shell=True)
	
	# awesome
    elif desktop_env == 'awesome':
        with subprocess.Popen("awesome-client", stdin=subprocess.PIPE) as awesome_client:
            command = 'local gears = require("gears"); for s = 1, screen.count() do gears.wallpaper.maximized("%s", s, true); end;' % image
            awesome_client.communicate(input=bytes(command, 'UTF-8'))
	
	# failed
    else:
        sys.stderr.write('Error: Failed to set wallpaper. (Desktop not supported)')
        return False

    return True
###########################################################################
