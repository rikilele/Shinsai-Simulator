"""
This is a terrain tracer for any maps that have been created to be rendered in
to the Shinsai-Simulator app. The purpose of this program is to get all Z-axis 
values for given (x, y) coordinates on the map. While this program is running,
a "laser" will be tracing the height for each coordinate of the map in a panda3d
window. Ideally, the tuple (x, y) will then become a "key" to the dictionary 
that maps the respective z-values obtained.
"""

while x < maxX:
    while y < maxY:
        pass