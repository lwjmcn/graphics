from glfw.GLFW import *
import numpy as np
import globals
import os
import glm
from node import Node


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
            if key==GLFW_KEY_1:
                globals.g_line_mode = True # line rendering mode
            if key==GLFW_KEY_2:
                globals.g_line_mode = False # box rendering mode
            if key==GLFW_KEY_SPACE:
                globals.g_time_press_space = glfwGetTime()
                globals.g_animate_mode = not globals.g_animate_mode

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


# 파일 드래그앤드롭 이벤트
def drop_callback(window, paths):
    globals.g_lock = True # 처리중에 lock 걸기

    if len(paths) > 1: # 한 번에 한 파일만 처리
        print("Only one file at a time")

    # 초기화
    globals.g_nodes = [] # node들 저장
    globals.g_time_press_space = 0 # animating 모드로 들어간 순간의 시각
    globals.g_line_mode = True # line 모드 (또는 box 모드)
    globals.g_animate_mode = False # animating 모드 (또는 rest pose 모드)
    globals.g_frame_time = 0 # frame time (1/FPS)
    globals.g_frame_arr = [] # frame channel 값들
    globals.g_frame_cnt = 0 # frame 개수
    globals.g_scale = 1. # 모델 크기 조절

    frame_num = 0
    frame_time = 0
    joint_num = 0
    joint_names = []
    joint_offset_arr = [] # OFFSET 정보 저장
    total_channel_num = 0 # channel 개수
    joint_channel_arr = [] # XROTATION, YROTATION, ...
    frame_channel_arr = [] # channel 
    vertex_index_arr = [] # line을 그리기 위한 vertex 정보 저장
    nodeStack = [] # stack으로 유지하여 중괄호에 따라 append/pop하면서 저장함
    i = 0

   # BVH Parsing
    file = open(os.path.join(paths[0]), "r")
    while True :
        line = file.readline()
        parse = line.split()
        if not line : # end of file
            break
        elif parse[0] == "HIERARCHY" or parse[0] == "MOTION" or parse[0] == "{":
            continue

        #HIERARCHY
        elif parse[0] == "ROOT" :
            joint_names.append(parse[1])
            joint_num += 1

            node = Node(parse[1], None)
            globals.g_nodes.append(node)
            nodeStack.append(node)
        elif parse[0] == "JOINT" :
            joint_names.append(parse[1])
            joint_num += 1

            parent = nodeStack[-1]

            node = Node(parse[1], parent)
            globals.g_nodes.append(node)
            nodeStack.append(node)
        elif parse[0] == "CHANNELS":
            channel_num = int(parse[1])
            total_channel_num += channel_num
            for item in parse[2:]:  
                nodeStack[-1].columnIndex.append(i)
                nodeStack[-1].channels.append(item)
                i += 1
        elif parse[0] == "OFFSET":
            offset = glm.vec3()
            offset.x = float(parse[1])
            offset.y = float(parse[2])
            offset.z = float(parse[3])
            globals.g_scale = max(globals.g_scale, 3*float(parse[1]))
            nodeStack[-1].offset = offset
        elif parse[0] == "End":
            parent = nodeStack[-1]
            node = Node(parse[1], parent)
            globals.g_nodes.append(node)
            nodeStack.append(node)
        elif parse[0] == "}":
            nodeStack.pop()
        
        # MOTION
        elif parse[0] == "Frames:":
            frame_num = int(parse[1])
        elif parse[0] == "Frame": # Frame Time:
            frame_time = float(parse[2])
        else :
            # frame channel value
            channel_val_arr = [] 
            for item in parse:
                channel_val_arr.append(float(item))
            globals.g_frame_arr.append(channel_val_arr)
    
    # 정보 출력
    print("Bvh file name : ", os.path.basename(paths[0]))
    print("Number of frames : ", frame_num)
    print("FPS(1/FrameTime) : ", 1.0/frame_time)
    print("Number of joints (including root) : ", joint_num)
    print("List of all joint names : ", end="")
    for joint in joint_names:
        print(joint, end=" ")
    print()
    file.close()

    # for node in globals.g_nodes:
    #     print(node.name, end=" ")
    #     print(node.offset, end=" ")
    #     print(node.link_transform_from_parent, end=" ")
    # print()

    globals.g_frame_time = frame_time
    globals.g_frame_cnt = frame_num

    globals.g_lock = False # 처리중에 lock 걸기
