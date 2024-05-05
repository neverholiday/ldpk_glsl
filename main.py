#!/usr/bin/env python3

####################################################################
#
#	Standard Import
#

import sys
import ctypes
import numpy as np

import sdl2
from sdl2 import video

from OpenGL import GL
from PIL import Image

####################################################################
#
#	Local Import
#

# shader program
from ShaderProgram import ShaderProgram

# matrix
from Matrix4 import Matrix4
from Transform3D import Transform3D

####################################################################
#
#	Main Import
#

def run():
	if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
		print(sdl2.SDL_GetError())
		return -1

	windowWidth = 800
	windowHeight = 600
	window = sdl2.SDL_CreateWindow( b"OpenGL demo",
								   sdl2.SDL_WINDOWPOS_CENTERED,
								   sdl2.SDL_WINDOWPOS_CENTERED, 
								   windowWidth, windowHeight,
								   sdl2.SDL_WINDOW_OPENGL )
	if not window:
		print(sdl2.SDL_GetError())
		return -1

	# Force OpenGL 3.3 'core' context.
	# Must set *before* creating GL context!
	video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MAJOR_VERSION, 3)
	video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MINOR_VERSION, 3)
	video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_PROFILE_MASK,
		video.SDL_GL_CONTEXT_PROFILE_CORE)
	context = sdl2.SDL_GL_CreateContext(window)

	# construct shader program and compile
	shaderProgram = ShaderProgram()
	shaderProgram.compile()

	#
	#	Read image
	#
	imagePath = './image/graded_edit_final_05535.png'
	image = Image.open( imagePath ).convert( 'RGB' ).transpose( Image.FLIP_TOP_BOTTOM )
	imageArray = np.array( image )
	imageWidth = imageArray.shape[1]
	imageHeight = imageArray.shape[0]
	imageAspectRatio = imageWidth/imageHeight
	numChannels = imageArray.shape[2]

	print( 'Image Info:' )
	print( f'	image path = {imagePath}' )
	print( f'	image width = {imageWidth}' )
	print( f'	image height = {imageHeight}' )
	print( f'	image aspect ratio = {imageAspectRatio}' )
	print( f'	image num channels = {numChannels}' )
	print( f'	image data type = {imageArray.dtype}' )

	#
	#	Setup textures
	#
 
	# generate texture id
	texture = None
	texture = GL.glGenTextures(1)

	# bind texture
	GL.glBindTexture( GL.GL_TEXTURE_2D, texture )

	# set texture param
	GL.glTexParameteri( GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT )
	GL.glTexParameteri( GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT )
	GL.glTexParameteri( GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR )
	GL.glTexParameteri( GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR )

	# set to tex image
	GL.glTexImage2D( GL.GL_TEXTURE_2D, 
				 		0, 
						GL.GL_RGB,
						imageWidth,
						imageHeight,
						0,
						GL.GL_RGB,
						GL.GL_UNSIGNED_BYTE,
						imageArray )


	#
	#	Setup scene
	#
 
	print( 'scene info:' )
	print( f'	window dimension = ( {windowWidth}, {windowHeight} )' )
	print( f'	image dimension = ( {imageWidth}, {imageHeight} )' )
	
	windowAspectRatio = windowWidth/windowHeight
	print( f'	window aspect ratio = {windowAspectRatio}' )

	# compute 1-1
	zoomFactor_x = windowWidth / imageWidth
	zoomFactor_y = windowHeight / imageHeight

	print( f'	zoomFactor x (1 to 1) = {zoomFactor_x}' )
	print( f'	zoomFactor y (1 to 1) = {zoomFactor_y}' )

	# find out min of zoom factor
	zoomFactor = min( zoomFactor_x, zoomFactor_y )
	print( f'	min zoomFactor = {zoomFactor}' )
	
	# compute for scale matrix
	scaleFactor = windowAspectRatio/imageAspectRatio
	print( f'	scaleFactor ( windowAspectRatio/imageAspectRatio ) = {scaleFactor}' )

	# scale matrix
	scaleMatrix = Transform3D.scale( 1, scaleFactor, 1 )

	# ortho matrix
	ortho = Transform3D.ortho( 	0, imageWidth, 
								0, imageHeight,
								-1, 1 )
	
	# scale in image space
	scaleImageFactor = 0.9
	scaleImage = Transform3D.scale( scaleImageFactor, scaleImageFactor, 1 )

	# compute transform for project image
	projectionTransform = scaleImage * scaleMatrix * ortho
	
	#
	#	Setup vertex
	#

	# initial vertex buffer and element buffer object
	VAO = None
	VBO = None
	EBO = None

	# rect position
	l = 0
	r = imageWidth
	b = 0
	t = imageHeight

	print( 'vertex info' )
	print( f'	left = {l}' )
	print( f'	right = {r}' )
	print( f'	bottom = {b}' )
	print( f'	top = {t}' )

	vertexData = np.array([
	# Vertex Positions			# color			# uv
		l, b, 0.0, 1.0, 		1.0, 0.0, 0.0, 1.0, 0.0, 0.0,
		l, t, 0.0, 1.0, 		0.0, 1.0, 0.0, 1.0, 0.0, 1.0,
		r, t, 0.0, 1.0, 		0.0, 0.0, 1.0, 1.0, 1.0, 1.0,
		r, b, 0.0, 1.0, 		1.0, 0.0, 1.0, 1.0, 1.0, 0.0,

	], dtype=np.float32)
	indicesData = np.array( [ 0, 1, 2, 2, 3, 0 ], dtype=np.uint32 )

	# Core OpenGL requires that at least one OpenGL vertex array be bound
	VAO = GL.glGenVertexArrays(1)
	GL.glBindVertexArray(VAO)
	
	# Need VBO for triangle vertices and colours
	VBO = GL.glGenBuffers(1)
	GL.glBindBuffer( GL.GL_ARRAY_BUFFER, VBO )
	GL.glBufferData( GL.GL_ARRAY_BUFFER, 
				 		vertexData.nbytes, 
						vertexData,
						GL.GL_STATIC_DRAW )
	
	EBO = GL.glGenBuffers(1)
	GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, EBO)
	GL.glBufferData( GL.GL_ELEMENT_ARRAY_BUFFER, 
				 		indicesData.nbytes, 
						indicesData,
						GL.GL_STATIC_DRAW )
	
	# enable array and set up data
	GL.glEnableVertexAttribArray(0)
	GL.glEnableVertexAttribArray(1)
	GL.glEnableVertexAttribArray(2)

	# number of vertex
	numVertex = 4
	numColor = 4
	numTexCoord = 2
	glFloatSize = ctypes.sizeof( ctypes.c_float )

	# set vertex attribute
	GL.glVertexAttribPointer( 0, 
						  		numVertex, 
								GL.GL_FLOAT, 
								GL.GL_FALSE, 
								( numVertex + numColor + numTexCoord ) * glFloatSize,
								None )
	
	# set color attribute
	# NOTE: the last parameter is a pointer
	GL.glVertexAttribPointer( 1, 
						  		numColor, 
								GL.GL_FLOAT, 
								GL.GL_FALSE, 
								( numVertex + numColor + numTexCoord ) * glFloatSize,
								ctypes.c_void_p( numVertex * glFloatSize ) )
	
	# set uv texcoord attribute
	# NOTE: the last parameter is a pointer
	GL.glVertexAttribPointer( 2, 
						  		numTexCoord, 
								GL.GL_FLOAT, 
								GL.GL_FALSE, 
								( numVertex + numColor + numTexCoord ) * glFloatSize,
								ctypes.c_void_p( ( numVertex + numColor ) * glFloatSize ) )

	GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
	GL.glBindVertexArray(0)

	# define event
	event = sdl2.SDL_Event()
	running = True

	while running:

		# wait event 
		sdl2.SDL_WaitEvent( ctypes.byref( event ) )
		
		if event.type == sdl2.SDL_QUIT:
			running = False

		# setup viewport
		GL.glViewport( 0, 0, windowWidth, windowHeight )

		# render
		GL.glClearColor(0, 0, 0, 1)
		GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

		#
		# render part
		#

		# active shader program
		shaderProgram.use()
		GL.glBindTexture( GL.GL_TEXTURE_2D, texture )
		GL.glBindVertexArray(VAO)

		# set mvp for this object
		# get model, view and project location
		model_m4 = Matrix4()
		view_m4 = Matrix4()
		projection_m4 = projectionTransform

		shaderProgram.setMat4( "model", model_m4 )
		shaderProgram.setMat4( "view", view_m4 )
		shaderProgram.setMat4( "projection", projection_m4 )
		
		# draw triangle
		GL.glDrawElements( GL.GL_TRIANGLES, len(indicesData), GL.GL_UNSIGNED_INT, None )

		# unbind
		GL.glBindVertexArray(0)
		GL.glUseProgram(0)

		sdl2.SDL_GL_SwapWindow(window)
		sdl2.SDL_Delay(10)

	sdl2.SDL_GL_DeleteContext(context)
	sdl2.SDL_DestroyWindow(window)
	sdl2.SDL_Quit()
	return 0

if __name__ == "__main__":
	sys.exit(run())