#!/usr/bin/env python3

import numpy as np

class Vector4:

    def __init__( self, x=0, y=0, z=0, w=1 ) -> None:
        self.v = np.zeros( ( 4, 1 ), dtype=np.float32 )
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __repr__( self ):
        return str( self.v )
    
    @property
    def x( self ):
        return self.v[0][0]
    
    @x.setter
    def x( self, val:float ):
        self.v[0][0] = val

    @property
    def y( self ):
        return self.v[1][0]
    
    @y.setter
    def y( self, val:float ):
        self.v[1][0] = val

    @property
    def z( self ):
        return self.v[2][0]
    
    @z.setter
    def z( self, val:float ):
        self.v[2][0] = val

    @property
    def w( self ):
        return self.v[3][0]
    
    @w.setter
    def w( self, val:float ):
        self.v[3][0] = val

