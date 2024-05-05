#!/usr/bin/env python3

import numpy as np

from Vector4 import Vector4

class Matrix4:
	''' Matrix4 class
	'''

	def __init__( self ) -> None:
		self.m = np.identity( 4, dtype=np.float32 )

	def __repr__( self ):
		return str( self.m )

	@property
	def x1( self ):
		return self.m[0][0]
	
	@x1.setter
	def x1( self, val:float ):
		self.m[0][0] = val

	@property
	def y1( self ):
		return self.m[1][0]
	
	@y1.setter
	def y1( self, val:float ):
		self.m[1][0] = val

	@property
	def z1( self ):
		return self.m[2][0]
	
	@z1.setter
	def z1( self, val:float ):
		self.m[2][0] = val

	@property
	def w1( self ):
		return self.m[3][0]
	
	@w1.setter
	def w1( self, val:float ):
		self.m[3][0] = val

	@property
	def x2( self ):
		return self.m[0][1]
	
	@x2.setter
	def x2( self, val:float ):
		self.m[0][1] = val

	@property
	def y2( self ):
		return self.m[1][1]
	
	@y2.setter
	def y2( self, val:float ):
		self.m[1][1] = val

	@property
	def z2( self ):
		return self.m[2][1]
	
	@z2.setter
	def z2( self, val:float ):
		self.m[2][1] = val

	@property
	def w2( self ):
		return self.m[3][1]
	
	@w2.setter
	def w2( self, val:float ):
		self.m[3][1] = val

	@property
	def x3( self ):
		return self.m[0][2]
	
	@x3.setter
	def x3( self, val:float ):
		self.m[0][2] = val

	@property
	def y3( self ):
		return self.m[1][2]
	
	@y3.setter
	def y3( self, val:float ):
		self.m[1][2] = val

	@property
	def z3( self ):
		return self.m[2][2]
	
	@z3.setter
	def z3( self, val:float ):
		self.m[2][2] = val

	@property
	def w3( self ):
		return self.m[3][2]
	
	@w3.setter
	def w3( self, val:float ):
		self.m[3][2] = val

	@property
	def x4( self ):
		return self.m[0][3]
	
	@x4.setter
	def x4( self, val:float ):
		self.m[0][3] = val

	@property
	def y4( self ):
		return self.m[1][3]
	
	@y4.setter
	def y4( self, val:float ):
		self.m[1][3] = val

	@property
	def z4( self ):
		return self.m[2][3]
	
	@z4.setter
	def z4( self, val:float ):
		self.m[2][3] = val

	@property
	def w4( self ):
		return self.m[3][3]
	
	@w4.setter
	def w4( self, val:float ):
		self.m[3][3] = val


	#
	#	operator
	#
 
	def __add__( self, other ):
		return self.m + other.m

	def __sub__( self, other ):
		return self.m - other.m
	
	def __mul__( self, other ):
		if isinstance( other, Vector4 ):
			return self.m @ other.v
		return self.m @ other.m
		
		
	
	