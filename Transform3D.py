#!/usr/bin/env python3

import numpy as np

from Matrix4 import Matrix4

class Transform3D:
	''' class from computing numpy
	'''

	@staticmethod
	def ortho( left:float, right:float, 
				  		bottom:float, top:float, 
						near:float, far:float ):
		'''	compute ortho projection given bounding box 
			and near, far clip
		'''

		# for alias
		l = left
		r = right
		b = bottom
		t = top
		n = near
		f = far

		# construct matrix4
		return Matrix4.fromArgs( 2/(r-l), 	0, 			0, 			-((r+l)/(r-l)),
						  			0,		2/(t-b),  	0,			-((t+b)/(t-b)),
									0,		0,			-2/(f-n),	-((f+n)/(f-n)),
									0,		0,			0,			1 )
		



