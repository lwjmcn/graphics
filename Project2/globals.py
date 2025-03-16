import glm
import numpy as np

def initialize():
    global g_origin_x
    global g_origin_z

    global g_firstLeftClick
    global g_lastX
    global g_lastY

    global g_azimuth 
    global g_elevation

    global g_firstRightClick

    global g_cam_zoom

    global g_is_perspective

    global g_vertex_arr
    global g_vao_obj

    global g_is_hierarchical
    global g_is_wireframe

    # initialize target point to the origin
    g_origin_x = 0.
    g_origin_z = 0.

    g_firstLeftClick = True
    g_lastX = 0.
    g_lastY = 0.

    g_azimuth = 0.
    g_elevation = 0.

    g_firstRightClick = True

    g_cam_zoom = 0

    g_is_perspective = True

    g_vertex_arr = []
    g_vao_obj = []
    
    g_is_hierarchical = False
    g_is_wireframe = True