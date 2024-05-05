#!/usr/bin/env python3

from OpenGL import GL
from OpenGL.GL import shaders

class ShaderProgram:

	VertexShader = \
"""
#version 330 core
layout (location=0) in vec4 position;
layout (location=1) in vec4 inColor;
layout (location=2) in vec2 inTexCoord;

// uniform transform
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec4 outColorF;
out vec2 texCoord;
void main()
{

	// compute mvp
	mat4 mvp = projection * view * model;

	gl_Position = mvp * position;
	outColorF = inColor;
	texCoord = inTexCoord;
}
"""

	FragmentShader = \
"""
#version 330 core
in vec4 outColorF;
in vec2 texCoord;

out vec4 outColor;

// texture uniform attribute
uniform sampler2D texture1;

void main()
{
	outColor = texture( texture1, texCoord );
}
"""

	def __init__( self ) -> None:
		self.shaderProgram = None

	def compile( self ):
		''' compile shader program
		'''

		# compile shader and link to shader program
		vertexShader = shaders.compileShader( self.VertexShader, 
									   			GL.GL_VERTEX_SHADER )
		fragmentShader = shaders.compileShader( self.FragmentShader, 
										 		GL.GL_FRAGMENT_SHADER )
		shaderProgram = shaders.compileProgram( vertexShader, 
										 		fragmentShader, 
												validate=False )

		# add shader program to be member of this class
		self.shaderProgram = shaderProgram

		# free vertex shader and fragment shader
		# GL.glDeleteShader( vertexShader )
		# GL.glDeleteShader( fragmentShader )

	def use( self ):
		'''	call use shader program (when in render function)
		'''
		GL.glUseProgram( self.shaderProgram )

	def setMat4( self, attrName:str, matrix4 ):
		'''	set uniform attribute, matrix 4 to shader program
		'''

		GL.glUniformMatrix4fv(  GL.glGetUniformLocation( self.shaderProgram, attrName ), 
									1, 
									GL.GL_FALSE, 
									matrix4.T )
		