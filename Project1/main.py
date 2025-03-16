from OpenGL.GL import *
from glfw.GLFW import *
import glm
import numpy as np

from vao_frame import prepare_vao_axis, prepare_vao_grid
from load_shader import load_shaders
from shader import g_vertex_shader_src, g_fragment_shader_src
import globals
from input_callback import key_callback, cursor_callback, scroll_callback

def main():
    globals.initialize()
    # initialize glfw
    if not glfwInit():
        return
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)   # OpenGL 3.3
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)  # Do not allow legacy OpenGl API calls
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE) # for macOS

    # create a window and OpenGL context
    window = glfwCreateWindow(1200, 1000, 'Project1', None, None)
    if not window:
        glfwTerminate()
        return
    glfwMakeContextCurrent(window)

    # register event callbacks
    glfwSetKeyCallback(window, key_callback);
    glfwSetCursorPosCallback(window, cursor_callback)
    glfwSetScrollCallback(window, scroll_callback)

    # load shaders
    shader_program = load_shaders(g_vertex_shader_src, g_fragment_shader_src)

    # get uniform locations
    MVP_loc = glGetUniformLocation(shader_program, 'MVP')
    
    # prepare vaos
    vao_axis = prepare_vao_axis()
    vao_grid = prepare_vao_grid()

    # loop until the user closes the window
    while not glfwWindowShouldClose(window):
        # render

        # enable depth test (we'll see details later)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        # render in "wireframe mode"
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        glUseProgram(shader_program)

        # projection matrix
        # P = glm.perspective(np.radians(globals.g_cam_zoom), 1, 0.1, 100.)
        P = glm.perspective(45, 1, 0.1, 100.)
        if not globals.g_is_perspective :
            P = glm.ortho(-.02*(globals.g_cam_zoom+45.1),.02*(globals.g_cam_zoom+45.1),-.02*(globals.g_cam_zoom+45.1),.02*(globals.g_cam_zoom+45.1), -10, 90)
        #    P = glm.ortho(-2,2,-2,2, -10, 90)

        # target position
        cameraTarget = glm.vec3(1)
        cameraTarget.x = globals.g_origin_x * np.cos(np.radians(globals.g_azimuth)) + globals.g_origin_z * np.sin(np.radians(globals.g_azimuth))
        cameraTarget.y = 0
        cameraTarget.z = - globals.g_origin_x *np.sin(np.radians(globals.g_azimuth)) + globals.g_origin_z * np.cos(np.radians(globals.g_azimuth))
        glm.normalize(cameraTarget)

        # camera position
        cameraPos = glm.vec3(1)
        cameraPos.x = 3*np.cos(np.radians(globals.g_elevation))*np.sin(np.radians(globals.g_azimuth)) + cameraTarget.x
        cameraPos.y = 3*np.sin(np.radians(globals.g_elevation))
        cameraPos.z = 3*np.cos(np.radians(globals.g_elevation))*np.cos(np.radians(globals.g_azimuth)) + cameraTarget.z
        glm.normalize(cameraPos)

        cameraDirection = glm.vec3(cameraPos - cameraTarget)
        cameraPos.x += .02* globals.g_cam_zoom * cameraDirection.x
        cameraPos.y += .02* globals.g_cam_zoom * cameraDirection.y
        cameraPos.z += .02* globals.g_cam_zoom * cameraDirection.z
        glm.normalize(cameraPos)

        V = glm.lookAt(cameraPos, cameraTarget, glm.vec3(0,1,0))

        # current frame: P*V*I (now this is the world frame)
        I = glm.mat4()
        MVP = P*V*I
        glUniformMatrix4fv(MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP))

        # draw axis
        glBindVertexArray(vao_axis)
        glDrawArrays(GL_LINES, 0, 4)

        # draw grid
        glBindVertexArray(vao_grid)
        for i in range(9):
            for j in range(9):
                MVP_grid = MVP * glm.translate(glm.vec3(2*(i-4), 0, 2*(j-4)))
                glUniformMatrix4fv(MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP_grid))
                glDrawArrays(GL_LINES, 0, 76)

        # swap front and back buffers
        glfwSwapBuffers(window)

        # poll events
        glfwPollEvents()

    # terminate glfw
    glfwTerminate()

if __name__ == "__main__":
    main()
