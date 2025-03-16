from OpenGL.GL import *
import glm
import numpy as np
import globals
import os

def prepare_vao_axis():
    # prepare vertex data (in main memory)
    vertices = glm.array(glm.float32,
        # position        # color
         -10.0, 0.0, 0.0,  1.0, 0.0, 0.0, # x-axis start
         10.0, 0.0, 0.0,  1.0, 0.0, 0.0, # x-axis end 
         0.0, 0.0, -10.0,  0.0, 0.0, 1.0, # z-axis start
         0.0, 0.0, 10.0,  0.0, 0.0, 1.0, # z-axis end
    )

    # create and activate VAO (vertex array object)
    VAO = glGenVertexArrays(1)  # create a vertex array object ID and store it to VAO variable
    glBindVertexArray(VAO)      # activate VAO

    # create and activate VBO (vertex buffer object)
    VBO = glGenBuffers(1)   # create a buffer object ID and store it to VBO variable
    glBindBuffer(GL_ARRAY_BUFFER, VBO)  # activate VBO as a vertex buffer object

    # copy vertex data to VBO
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW) # allocate GPU memory for and copy vertex data to the currently bound vertex buffer

    # configure vertex positions
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), None)
    glEnableVertexAttribArray(0)

    # configure vertex colors
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), ctypes.c_void_p(3*glm.sizeof(glm.float32)))
    glEnableVertexAttribArray(1)

    return VAO

def prepare_vao_grid():
    # prepare vertex data (in main memory)
    vertices = glm.array(glm.float32,
        # position        # color
         -2.0, 0.0, 0., 0.5, 0.5, 0.5,
         2.0, 0.0, 0., 0.5, 0.5, 0.5,
         -2.0, 0.0, .2,  0.5, 0.5, 0.5, # x-axis grid
         2.0, 0.0, .2,  0.5, 0.5, 0.5,
         -2.0, 0.0, .4,  0.5, 0.5, 0.5, # x-axis grid
         2.0, 0.0, .4,  0.5, 0.5, 0.5,
         -2.0, 0.0, .6,  0.5, 0.5, 0.5, # x-axis grid
         2.0, 0.0, .6,  0.5, 0.5, 0.5,
         -2.0, 0.0, .8,  0.5, 0.5, 0.5, # x-axis grid
         2.0, 0.0, .8,  0.5, 0.5, 0.5,
         -2.0, 0.0, 1.0,  0.5, 0.5, 0.5, # x-axis grid
         2.0, 0.0, 1.0,  0.5, 0.5, 0.5,
         -2.0, 0.0, 1.2,  0.5, 0.5, 0.5, # x-axis grid
         2.0, 0.0, 1.2,  0.5, 0.5, 0.5,
         -2.0, 0.0, 1.4,  0.5, 0.5, 0.5, # x-axis grid
         2.0, 0.0, 1.4,  0.5, 0.5, 0.5,
         -2.0, 0.0, 1.6,  0.5, 0.5, 0.5, # x-axis grid
         2.0, 0.0, 1.6,  0.5, 0.5, 0.5,
         -2.0, 0.0, 1.8,  0.5, 0.5, 0.5, # x-axis grid
         2.0, 0.0, 1.8,  0.5, 0.5, 0.5,
         -2.0, 0.0, -.2,  0.5, 0.5, 0.5, # x-axis grid
         2.0, 0.0, -.2,  0.5, 0.5, 0.5,
         -2.0, 0.0, -.4,  0.5, 0.5, 0.5, # x-axis grid
         2.0, 0.0, -.4,  0.5, 0.5, 0.5,
         -2.0, 0.0, -.6,  0.5, 0.5, 0.5, # x-axis grid
         2.0, 0.0, -.6,  0.5, 0.5, 0.5,
         -2.0, 0.0, -.8,  0.5, 0.5, 0.5, # x-axis grid
         2.0, 0.0, -.8,  0.5, 0.5, 0.5,
         -2.0, 0.0, -1.0,  0.5, 0.5, 0.5, # x-axis grid
         2.0, 0.0, -1.0,  0.5, 0.5, 0.5,
         -2.0, 0.0, -1.2,  0.5, 0.5, 0.5, # x-axis grid
         2.0, 0.0, -1.2,  0.5, 0.5, 0.5,
         -2.0, 0.0, -1.4,  0.5, 0.5, 0.5, # x-axis grid
         2.0, 0.0, -1.4,  0.5, 0.5, 0.5,
         -2.0, 0.0, -1.6,  0.5, 0.5, 0.5, # x-axis grid
         2.0, 0.0, -1.6,  0.5, 0.5, 0.5,
         -2.0, 0.0, -1.8,  0.5, 0.5, 0.5, # x-axis grid
         2.0, 0.0, -1.8,  0.5, 0.5, 0.5,

         0.0, 0.0, -2.0,  0.5, 0.5, 0.5, # z-axis start
         0.0, 0.0, 2.0,  0.5, 0.5, 0.5, # z-axis end
         .2, 0.0, -2.0,  0.5, 0.5, 0.5, # z-axis grid
         .2, 0.0, 2.0,  0.5, 0.5, 0.5,
         .4, 0.0, -2.0,  0.5, 0.5, 0.5, # z-axis grid
         .4, 0.0, 2.0,  0.5, 0.5, 0.5,
         .6, 0.0, -2.0,  0.5, 0.5, 0.5, # z-axis grid
         .6, 0.0, 2.0,  0.5, 0.5, 0.5,
         .8, 0.0, -2.0,  0.5, 0.5, 0.5, # z-axis grid
         .8, 0.0, 2.0,  0.5, 0.5, 0.5,
         1.0, 0.0, -2.0,  0.5, 0.5, 0.5, # z-axis grid
         1.0, 0.0, 2.0,  0.5, 0.5, 0.5,
         1.2, 0.0, -2.0,  0.5, 0.5, 0.5, # z-axis grid
         1.2, 0.0, 2.0,  0.5, 0.5, 0.5,
         1.4, 0.0, -2.0,  0.5, 0.5, 0.5, # z-axis grid
         1.4, 0.0, 2.0,  0.5, 0.5, 0.5,
         1.6, 0.0, -2.0,  0.5, 0.5, 0.5, # z-axis grid
         1.6, 0.0, 2.0,  0.5, 0.5, 0.5,
         1.8, 0.0, -2.0,  0.5, 0.5, 0.5, # z-axis grid
         1.8, 0.0, 2.0,  0.5, 0.5, 0.5,
         -.2, 0.0, -2.0,  0.5, 0.5, 0.5, # z-axis grid
         -.2, 0.0, 2.0,  0.5, 0.5, 0.5,
         -.4, 0.0, -2.0,  0.5, 0.5, 0.5, # z-axis grid
         -.4, 0.0, 2.0,  0.5, 0.5, 0.5,
         -.6, 0.0, -2.0,  0.5, 0.5, 0.5, # z-axis grid
         -.6, 0.0, 2.0,  0.5, 0.5, 0.5,
         -.8, 0.0, -2.0,  0.5, 0.5, 0.5, # z-axis grid
         -.8, 0.0, 2.0,  0.5, 0.5, 0.5,
         -1.0, 0.0, -2.0,  0.5, 0.5, 0.5, # z-axis grid
         -1.0, 0.0, 2.0,  0.5, 0.5, 0.5,
         -1.2, 0.0, -2.0,  0.5, 0.5, 0.5, # z-axis grid
         -1.2, 0.0, 2.0,  0.5, 0.5, 0.5,
         -1.4, 0.0, -2.0,  0.5, 0.5, 0.5, # z-axis grid
         -1.4, 0.0, 2.0,  0.5, 0.5, 0.5,
         -1.6, 0.0, -2.0,  0.5, 0.5, 0.5, # z-axis grid
         -1.6, 0.0, 2.0,  0.5, 0.5, 0.5,
         -1.8, 0.0, -2.0,  0.5, 0.5, 0.5, # z-axis grid
         -1.8, 0.0, 2.0,  0.5, 0.5, 0.5,
    )

    # create and activate VAO (vertex array object)
    VAO = glGenVertexArrays(1)  # create a vertex array object ID and store it to VAO variable
    glBindVertexArray(VAO)      # activate VAO

    # create and activate VBO (vertex buffer object)
    VBO = glGenBuffers(1)   # create a buffer object ID and store it to VBO variable
    glBindBuffer(GL_ARRAY_BUFFER, VBO)  # activate VBO as a vertex buffer object

    # copy vertex data to VBO
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW) # allocate GPU memory for and copy vertex data to the currently bound vertex buffer

    # configure vertex positions
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), None)
    glEnableVertexAttribArray(0)

    # configure vertex colors
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), ctypes.c_void_p(3*glm.sizeof(glm.float32)))
    glEnableVertexAttribArray(1)

    return VAO

def prepare_vao_obj():
    # prepare vertex data (in main memory)
    vertices = (ctypes.c_float * len(globals.g_vertex_arr))(*globals.g_vertex_arr) 

    # create and activate VAO (vertex array object)
    VAO = glGenVertexArrays(1)  # create a vertex array object ID and store it to VAO variable
    glBindVertexArray(VAO)      # activate VAO

    # create and activate VBO (vertex buffer object)
    VBO = glGenBuffers(1)   # create a buffer object ID and store it to VBO variable
    glBindBuffer(GL_ARRAY_BUFFER, VBO)  # activate VBO as a vertex buffer object

    # create and activate EBO (element buffer object)
    EBO = glGenBuffers(1)   # create a buffer object ID and store it to EBO variable
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)  # activate EBO as an element buffer object

    # copy vertex data to VBO
    glBufferData(GL_ARRAY_BUFFER, len(vertices)*glm.sizeof(glm.float32), vertices, GL_STATIC_DRAW)

    # configure vertex positions
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), None)
    glEnableVertexAttribArray(0)

     # configure vertex normals
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), ctypes.c_void_p(3*glm.sizeof(glm.float32)))
    glEnableVertexAttribArray(1)

    return VAO

def prepare_vao_objfile(path): 
    final_arr = []
    vertex_arr = []
    normal_arr = []

   # OBJ Parsing
    file = open(os.path.join(path), "r")
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
            l = len(parse[1:])            
            tmp = []
            for i in range(l) : # convert to triangle mesh
                if i >= 3 :
                    tmp.append(parse[1])
                    tmp.append(parse[i])
                tmp.append(parse[i+1])
            for j in tmp :
                partition = j.split('/')
                
                v = vertex_arr[int(partition[0])-1]
                final_arr.append(v.x)
                final_arr.append(v.y)
                final_arr.append(v.z)
           
                if(len(partition) > 2):
                    n = normal_arr[int(partition[2])-1]
                    final_arr.append(n.x)
                    final_arr.append(n.y)
                    final_arr.append(n.z)
                else :
                    final_arr.append(0)
                    final_arr.append(0)
                    final_arr.append(0)
        else : # ignore comment, vt, mtllib, usemtl, o, s, ....
            continue

    # prepare vertex data (in main memory)
    vertices = (ctypes.c_float * len(final_arr))(*final_arr) 


    # create and activate VAO (vertex array object)
    VAO = glGenVertexArrays(1)  # create a vertex array object ID and store it to VAO variable
    glBindVertexArray(VAO)      # activate VAO

    # create and activate VBO (vertex buffer object)
    VBO = glGenBuffers(1)   # create a buffer object ID and store it to VBO variable
    glBindBuffer(GL_ARRAY_BUFFER, VBO)  # activate VBO as a vertex buffer object
  
    # copy vertex data to VBO
    glBufferData(GL_ARRAY_BUFFER, len(vertices)*glm.sizeof(glm.float32), vertices, GL_STATIC_DRAW)

    # configure vertex positions
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), None)
    glEnableVertexAttribArray(0)

     # configure vertex normals
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), ctypes.c_void_p(3*glm.sizeof(glm.float32)))
    glEnableVertexAttribArray(1)

    return VAO, len(final_arr)//2
