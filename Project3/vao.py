from OpenGL.GL import *
import glm
import numpy as np

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

def prepare_vao_box():
    # prepare vertex data (in main memory)
    # 36 vertices for 12 triangles
    vertices = glm.array(glm.float32,
        # position      normal
        -.05 ,  .05 ,  .05 ,  0, 0, 1, # v0
         .05 , -.05 ,  .05 ,  0, 0, 1, # v2
         .05 ,  .05 ,  .05 ,  0, 0, 1, # v1

        -.05 ,  .05 ,  .05 ,  0, 0, 1, # v0
        -.05 , -.05 ,  .05 ,  0, 0, 1, # v3
         .05 , -.05 ,  .05 ,  0, 0, 1, # v2

        -.05 ,  .05 , -.05 ,  0, 0,-1, # v4
         .05 ,  .05 , -.05 ,  0, 0,-1, # v5
         .05 , -.05 , -.05 ,  0, 0,-1, # v6

        -.05 ,  .05 , -.05 ,  0, 0,-1, # v4
         .05 , -.05 , -.05 ,  0, 0,-1, # v6
        -.05 , -.05 , -.05 ,  0, 0,-1, # v7

        -.05 ,  .05 ,  .05 ,  0, 1, 0, # v0
         .05 ,  .05 ,  .05 ,  0, 1, 0, # v1
         .05 ,  .05 , -.05 ,  0, 1, 0, # v5

        -.05 ,  .05 ,  .05 ,  0, 1, 0, # v0
         .05 ,  .05 , -.05 ,  0, 1, 0, # v5
        -.05 ,  .05 , -.05 ,  0, 1, 0, # v4
 
        -.05 , -.05 ,  .05 ,  0,-1, 0, # v3
         .05 , -.05 , -.05 ,  0,-1, 0, # v6
         .05 , -.05 ,  .05 ,  0,-1, 0, # v2

        -.05 , -.05 ,  .05 ,  0,-1, 0, # v3
        -.05 , -.05 , -.05 ,  0,-1, 0, # v7
         .05 , -.05 , -.05 ,  0,-1, 0, # v6

         .05 ,  .05 ,  .05 ,  1, 0, 0, # v1
         .05 , -.05 ,  .05 ,  1, 0, 0, # v2
         .05 , -.05 , -.05 ,  1, 0, 0, # v6

         .05 ,  .05 ,  .05 ,  1, 0, 0, # v1
         .05 , -.05 , -.05 ,  1, 0, 0, # v6
         .05 ,  .05 , -.05 ,  1, 0, 0, # v5

        -.05 ,  .05 ,  .05 , -1, 0, 0, # v0
        -.05 , -.05 , -.05 , -1, 0, 0, # v7
        -.05 , -.05 ,  .05 , -1, 0, 0, # v3

        -.05 ,  .05 ,  .05 , -1, 0, 0, # v0
        -.05 ,  .05 , -.05 , -1, 0, 0, # v4
        -.05 , -.05 , -.05 , -1, 0, 0, # v7
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

    # configure vertex normals
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), ctypes.c_void_p(3*glm.sizeof(glm.float32)))
    glEnableVertexAttribArray(1)

    return VAO

def prepare_vao_line(start, end):
    # 2 vertices for 1 lines
    vertices = glm.array(np.array([start, end]))

    # create and activate VAO (vertex array object)
    VAO = glGenVertexArrays(1)  # create a vertex array object ID and store it to VAO variable
    glBindVertexArray(VAO)      # activate VAO

    # create and activate VBO (vertex buffer object)
    VBO = glGenBuffers(1)   # create a buffer object ID and store it to VBO variable
    glBindBuffer(GL_ARRAY_BUFFER, VBO)  # activate VBO as a vertex buffer object

    # copy vertex data to VBO
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW) # allocate GPU memory for and copy vertex data to the currently bound vertex buffer

    # configure vertex positions
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * glm.sizeof(glm.float32), None)
    glEnableVertexAttribArray(0)

    return VAO
    