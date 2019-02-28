import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import base64

from config import config
import filesystem as fsys
import dataset as ds

def CreateLayout(app):
	app.layout =  html.Div([
		dcc.Location(id='url', refresh=False),
		html.Div(id='page-contents', children=ServeLayout(''))])

	# This function is called every time a folder name or a file name is clicked.
	@app.callback(dash.dependencies.Output('page-contents', 'children'),
		[dash.dependencies.Input('url', 'pathname')])
	def ProcessUrl(selectedPath):
		if selectedPath is None:
			return ServeLayout('')
		else:
			return ServeLayout(Decode(selectedPath[1:]))

def ServeLayout(selectedPath):
	# Create a folder tree
	selectedDir = os.path.dirname(selectedPath)
	tree = MakeDirTree('', selectedDir)
	treeObj = html.Ul(id='tree-root-ul', className='tree-root', children=tree)

	# List all the files in the selected folder.
	fs = fsys.FileSystem()
	filesArray = fs.ListFiles(selectedDir)
	fileListHtml = []
	for fn in filesArray:
		filePath = os.path.join(selectedDir, fn)
		if filePath == selectedPath:
			fileListHtml.append(html.Li(html.A(fn, href=Encode(filePath)), className='selected'))
		else:
			fileListHtml.append(html.Li(html.A(fn, href=Encode(filePath))))
	fileListHtml = html.Ul(id='file-list', className='file-list', children=fileListHtml)

	# is plottable checks if the selected path is a
	#    file of a type that we can handle
	if fs.IsPlottable(selectedPath):
		# print(selectedPath)
		# xlist, ylist, zlist = ds.ListDatasets()
		dset = ds.Dataset(fs.FullPath(selectedPath))
		dropdowns = html.Div(
		    [
		        html.Div([
		        dcc.Dropdown(
		            id='x-dropdown',
		            options=[{'label':name, 'value':name} for name in dset.names],
		            value = dset.xdefault,
					clearable=False,),
		            ],
				style={'width': '19%', 'margin-left': '0', 'margin-right': '0.5%', 'display': 'inline-block'}
				),
		        html.Div([
		        dcc.Dropdown(
		            id='y-dropdown',
					options=[{'label':name, 'value':name} for name in dset.names],
		            value = dset.ydefault,
					clearable=False,),
		            ],
				style={'width': '19%', 'margin-left': '0.5%', 'margin-right': '0.5%', 'display': 'inline-block'}
				),
				html.Div([
		        dcc.Dropdown(
		            id='z-dropdown',
					options=[{'label':name, 'value':name} for name in dset.names],
		            value = dset.zdefault,
					clearable=False,),
		            ],
				style={'width': '19%', 'margin-left': '0.5%', 'margin-right': '0', 'display': 'inline-block'}
				),
		    ],
		)
		plot = html.Div(
				html.P('Select data to plot...'),
			   )
		# plot = dset.plot()
	else:
		dropdowns = html.Div('')
		plot = html.Div('')

	return [html.Div(id='row-container',
			children=[html.Div(id='tree-div', children=treeObj),
			html.Div(id='file-list-div', children=[fileListHtml]),
			html.Div(id='graph-div', children=[dropdowns, plot])])]


# A recusive function that generates a tree structure
# using <ul> and <li> HTML elements.
def MakeDirTree(curDir, selectedDir):
	if selectedDir == '' or selectedDir == os.path.sep:
		selectedDir = ''
	selected = False
	isOpen = False
	if selectedDir == curDir[:-1]:
		selected = True
	if selectedDir.startswith(curDir[:-1]):
		isOpen = True
	fs = fsys.FileSystem()
	dirName = os.path.basename(curDir[:-1])

	childArr = []
	for subDir in fs.ListSubDirs(curDir):
		childArr.append(MakeDirTree(os.path.join(curDir, subDir), selectedDir))

	if curDir == '':
		dirName = os.path.basename(fs.root)

	liClassName = ''
	if selected:
		liClassName += 'selected '
	if isOpen:
		liClassName += 'open '

	if curDir == '':
		curDir = os.path.sep

	if len(childArr) > 0:
		return html.Li(className=liClassName, children=[
				html.A(dirName, href=Encode(curDir)), html.Ul(children=childArr)
			])
	else:
		return html.Li(className=liClassName, children=[
				html.A(dirName, href=Encode(curDir))
			])

# Encode the folder and file names into something that
# can safely be included in a URL.
def Encode(s):
	return base64.b64encode(bytes(s, 'utf-8')).decode('UTF-8','ignore')

def Decode(n):
	return base64.b64decode(n).decode('UTF-8','ignore')
