import os
import getpass
import shutil

# Local import
import desktop_functions



xml_file = 'wallpapers/catalina.xml'






if os.path.exists(xml_file):
	
	print('Configuring wallpaper...')
	
	# Get the current user name
	current_user = getpass.getuser()
	
	# Read the content of the catalina.xml file into an array and replace the username in each file path
	new_content = []
	with open(xml_file) as original_file:
		for original_line in original_file:
			if 'USERNAME' in original_line:
				new_content.append(original_line.replace('USERNAME', current_user))
			else:
				new_content.append(original_line)
	
	# Remove the original file
	os.remove(xml_file)

	# Create a new file using the content from the array
	with open(xml_file,'w') as new_file:
		new_file.writelines(new_content)
	
	# Move the wallpapers directory
	pictures_path = '/home/{0}/Pictures/'.format(current_user)
	catalina_wallpaper_path = '{0}{1}'.format(pictures_path, xml_file)
	shutil.move('wallpapers', pictures_path)  
	print('MacOS Catalina style wallpaper has been moved to: {0}'.format(pictures_path))
	
	
	# Try and set the desktop wallpaper
	
	desktop_env = desktop.get_desktop_environment()
	print('Desktop: %s' % desktop_env)
	
	
	if desktop_env == 'unknown':
		print('Unable to detect your desktop environment, you will need to manually set the wallpaper.')
	elif desktop_env == 'windows':
		print('It looks like you are running Microsoft Windows? This wallpaper only supports GTK based desktops.')
	elif desktop_env == 'mac':
		print('It looks like you are running MacOS? This wallpaper only supports GTK based desktops.')
	elif not desktop_functions.is_environment_gtk(desktop_env):
		print('It looks like you are running a {0} desktop environment? This wallpaper only supports GTK based desktops.'.format(desktop_env))
	else
		if os.path.exists(catalina_wallpaper_path):
			desktop_functions.set_wallpaper(catalina_wallpaper_path, desktop_env)
			print('MacOS Catalina style wallpaper installed.')
		
else:
	print('Unable to locate the catalina.xml file.')
