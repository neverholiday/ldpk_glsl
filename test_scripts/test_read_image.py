#!/usr/bin/env python3

from PIL import Image
import numpy as np

imagePath = './image/graded_edit_final_05535.png'
image = Image.open( imagePath ).convert( 'RGB' )
imageData = np.array( image )
image.show()
