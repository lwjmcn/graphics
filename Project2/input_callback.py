from glfw.GLFW import *
import numpy as np
import glm
import globals
import os
from vao import prepare_vao_obj

# 키보드 입력 이벤트
def key_callback(window, key, scancode, action, mods):
    if key==GLFW_KEY_ESCAPE and action==GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE);
    else:
        if action==GLFW_PRESS or action==GLFW_REPEAT:
            if key==GLFW_KEY_V:
                # toggle orthogonal / perspective
                globals.g_is_perspective = not globals.g_is_perspective
            elif key==GLFW_KEY_H:
                # hierarchical model rendering mode
                globals.g_is_hierarchical = True
            elif key==GLFW_KEY_Z:
                # toggle wireframe / solid mode
                globals.g_is_wireframe = not globals.g_is_wireframe

# 마우스 드래그 이벤트
def cursor_callback(window, xpos, ypos):
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
    # single mesh rendering mode
    globals.g_is_hierarchical = False

    if len(paths) > 1: # 한 번에 한 파일만 처리
        print("Only one file at a time")

    face = 0
    face_with_3 = 0
    face_with_4 = 0
    face_with_5 = 0

    # 초기화
    globals.g_vertex_arr = []
    vertex_arr = []
    normal_arr = []

   # OBJ Parsing
    file = open(os.path.join(paths[0]), "r")
    while True :
        line = file.readline()
        parse = line.split()
        if not line : # end of file
            break
        if len(parse) == 0: # empty
            continue
        elif parse[0] == 'v': # vertex position
            pos = glm.vec3()
            pos.x = float(parse[1])
            pos.y = float(parse[2])
            pos.z = float(parse[3])
            vertex_arr.append(pos)
        elif parse[0] == "vn" : # vertex normal
            nor = glm.vec3()
            nor.x = float(parse[1])
            nor.y = float(parse[2])
            nor.z = float(parse[3])
            normal_arr.append(nor)
        elif parse[0] == 'f': # face. vertex position index(//vertex normal index)
            face += 1
            l = len(parse[1:])
            if l == 3 :
                face_with_3 += 1                
            elif l == 4 :
                face_with_4 += 1
            elif l == 5 :
                face_with_5 += 1
            
            tmp = []
            for i in range(l) : # convert to triangle mesh
                if i >= 3 :
                    tmp.append(parse[1])
                    tmp.append(parse[i])
                tmp.append(parse[i+1])

            for j in tmp :
                partition = j.split('/')
                
                v = vertex_arr[int(partition[0])-1]
                globals.g_vertex_arr.append(v.x)
                globals.g_vertex_arr.append(v.y)
                globals.g_vertex_arr.append(v.z)
           
                if(len(partition) > 2):
                    n = normal_arr[int(partition[2])-1]
                    globals.g_vertex_arr.append(n.x)
                    globals.g_vertex_arr.append(n.y)
                    globals.g_vertex_arr.append(n.z)
                else :
                    globals.g_vertex_arr.append(0)
                    globals.g_vertex_arr.append(0)
                    globals.g_vertex_arr.append(0)
        else : # ignore comment, vt, mtllib, usemtl, o, s, ....
            continue

    # 정보 출력
    print("Obj file name : ", os.path.basename(paths[0]))
    print("Total number of faces : ", face)
    print("Number of faces with 3 vertices : ", face_with_3)
    print("Number of faces with 4 vertices : ", face_with_4)
    print("Number of faces with more than 4 vertices : ", face_with_5)
    file.close()

    globals.g_vao_obj = prepare_vao_obj()