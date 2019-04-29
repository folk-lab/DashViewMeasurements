config = {

	### Directory setup: ###
	#		FileServerProtocol defines where the data files are being hosted
	#		only 'local' and maybe 'samba' are supported
	'FileServerProtocol':	'local',

	#		LocalRootDirectory is the full system path to
	#		the root of the data folder file tree
	#'LocalRootDirectory':   '/Users/nik/Dropbox/data_2018',
	'LocalRootDirectory':	'Z:\Measurement_Data',
	#		LoggingDirectory is the full system path to a directory
	#		where log files will be stored for this application
	#		defaults to ./logs
	# 'LoggingDirectory':     ''

	# 	Samba data share variables below...
	# 'SambaServername':		'phys-jumbo.physik.unibas.ch',
	# 'SambaServiceName':		'zum$',
	# 'SambaServerIP':		'10.34.8.3',
	# 'SambaUsername':		'galeky83',
	# 'SambaPassword':		'####',
	# 'SambaServiceName':		'zum$',
	# 'SambaRootDirectory':	'Measurement_Data',

	### Apache deployment: ###
	#		ServerSubdirectory is the name of a subdirectory
	#		that hosts the Dash app
	#		for example: my-server.ca/dataview
	'ServerSubdirectory':   '/dataview',
}
