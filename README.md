Welcome to the enchant client.  Currently this package contains both the 

  * python client API
  * command-line interface

Each is discussed in some detail below.

# Installing

To install, simply run

	python setup.py install

You might need to use `sudo` depending on permissions.

# Configuring default server info

While the client system allows you to manually specify all configuration info, a configuration
file can be the more convenient way to do this.  By default, the client software looks for your
configuration information in the file `~/.config/enchant.json`.  The file should contain a JSON
dictionary looking something like this:

	{
		'host':'the-enchant-server-IP-address',
		'port':12345,
		'username':'your-username',
		'password':'your-password'
	}

Note that, yes, the password is stored in the configuration file in clear text.
Is this a good idea?  Probably not.  Is this easier for me to implement?  Yes.

# Command line interface

The command line interface is available through the `enchant` command.  To see options, run

	enchant -h

To upload content, you'll use a command something like:

	enchant txt my-notebook "Great Title" "This is some very important content"


# Python client API

All functionality is available through the `enchant` package.  Core
functionality is availabe through several methods:

  * `enchant.send_text(notebook,title,content[,timestamp,config_info])` - send text to the server
  * `enchant.send_html(notebook,title,content[,timestamp,config_info])` - send arbitrary html to the server
  * `enchant.send_image_file(notebook,title,image_filename[,timestamp,config_info])` - send an image

Enjoy!
