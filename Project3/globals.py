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

    global g_nodes
    global g_time_press_space 
    global g_line_mode
    global g_animate_mode
    global g_frame_time
    global g_frame_arr
    global g_frame_cnt

    global g_lock
    global g_scale

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

    g_nodes = []
    g_time_press_space = 0
    g_line_mode = True
    g_animate_mode = False
    g_frame_time = 0
    g_frame_arr = []
    g_frame_cnt = 0

    g_lock = True 
    g_scale = 1.
