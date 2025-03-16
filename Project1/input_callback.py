from glfw.GLFW import *
import numpy as np
import globals

# https://www.glfw.org/docs/3.3/group__input.html
# 키보드 입력 이벤트
def key_callback(window, key, scancode, action, mods):
    global azimuth, elevation, firstLeftClick, lastX, lastY, firstRightClick
    if key==GLFW_KEY_ESCAPE and action==GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE);
    else:
        if action==GLFW_PRESS or action==GLFW_REPEAT:
            # pressing v
            if key==GLFW_KEY_V:
                globals.g_is_perspective = not globals.g_is_perspective

# 마우스 드래그 이벤트
def cursor_callback(window, xpos, ypos):
    global azimuth, elevation, firstLeftClick, lastX, lastY, firstRightClick
    # 왼쪽 버튼
    if glfwGetMouseButton(window, GLFW_MOUSE_BUTTON_LEFT) == GLFW_RELEASE:
        globals.g_firstLeftClick = True
    else :
        if glfwGetMouseButton(window, GLFW_MOUSE_BUTTON_LEFT) == GLFW_PRESS:
            if globals.g_firstLeftClick:
                globals.g_lastX = xpos
                globals.g_lastY = ypos
                globals.g_firstLeftClick = False
        xOffset = xpos - globals.g_lastX
        yOffset = globals.g_lastY - ypos
        globals.g_lastX = xpos
        globals.g_lastY = ypos

        #sensitivity
        xOffset /= 10
        yOffset /= 20

        globals.g_azimuth -= xOffset
        globals.g_elevation -= yOffset

        # 뒤집어 지지 않게
        if globals.g_elevation > 89. :
            globals.g_elevation = 89.
        if globals.g_elevation < -89. :
            globals.g_elevation = -89.
        
    # 오른쪽 버튼 
    if glfwGetMouseButton(window, GLFW_MOUSE_BUTTON_RIGHT) == GLFW_RELEASE:
        globals.g_firstRightClick = True
    else :
        if glfwGetMouseButton(window, GLFW_MOUSE_BUTTON_RIGHT) == GLFW_PRESS:
            if globals.g_firstRightClick:
                globals.g_lastX = xpos
                globals.g_lastY = ypos
                globals.g_firstRightClick = False
        xOffset = xpos - globals.g_lastX
        yOffset = globals.g_lastY - ypos
        globals.g_lastX = xpos
        globals.g_lastY = ypos

        # sensitivity
        xOffset /= 300
        yOffset /= 300

        globals.g_origin_x -= xOffset
        if(globals.g_elevation < 0) : # 뒤집어졌을 때 거꾸로 인식
            globals.g_origin_z -= yOffset    
        else :
            globals.g_origin_z += yOffset    

# 스크롤 움직임 이벤트
def scroll_callback(window, xoffset, yoffset):
    globals.g_cam_zoom -= yoffset
    if globals.g_cam_zoom < -45 : # 거꾸로 넘어가지 않게
        globals.g_cam_zoom = -45
    if globals.g_cam_zoom > 400. : # 그리드가 보이지 않을 정도로 확대되지 않게
        globals.g_cam_zoom = 400.