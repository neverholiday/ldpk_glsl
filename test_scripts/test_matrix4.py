#!/usr/bin/env python3

from Matrix4 import Matrix4
from Vector4 import Vector4

x = Matrix4()
y = Matrix4()
v = Vector4( x=1, y=0.5 )

x.x4 = 2
x.y4 = 1
print( x )

y.x4 = 1
y.y4 = 2
print( y )

print( x * y )

print( v )
print( x * v )
