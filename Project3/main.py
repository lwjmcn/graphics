from OpenGL.GL import *
from glfw.GLFW import *
import glm
import numpy as np

from vao import prepare_vao_axis, prepare_vao_grid, prepare_vao_box, prepare_vao_line
from load_shader import load_shaders
from shader import g_vertex_shader_src, g_fragment_shader_src, g_vertex_shader_src_lighting, g_fragment_shader_src_lighting, g_vertex_shader_src_uniform_color
import globals
from input_callback import key_callback, cursor_callback, scroll_callback, drop_callback
from draw import draw_axis, draw_grid, draw_node_line, draw_node_box
from node import Node

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
    window = glfwCreateWindow(1200, 1000, 'Project3', None, None)
    if not window:
        glfwTerminate()
        return
    glfwMakeContextCurrent(window)

    # register event callbacks
    glfwSetKeyCallback(window, key_callback);
    glfwSetCursorPosCallback(window, cursor_callback)
    glfwSetScrollCallback(window, scroll_callback)
    glfwSetDropCallback(window, drop_callback)

    # load shaders
    shader_program = load_shaders(g_vertex_shader_src, g_fragment_shader_src)
    shader_lighting = load_shaders(g_vertex_shader_src_lighting, g_fragment_shader_src_lighting)
    shader_line = load_shaders(g_vertex_shader_src_uniform_color, g_fragment_shader_src)

    # get uniform locations
    MVP_loc_frame = glGetUniformLocation(shader_program, 'MVP')
    MVP_loc_line = glGetUniformLocation(shader_line, 'MVP')
    color_loc = glGetUniformLocation(shader_line, 'color')
    MVP_loc_box = glGetUniformLocation(shader_lighting, 'MVP')
    view_pos_loc = glGetUniformLocation(shader_lighting, 'view_pos')
    material_color_loc = glGetUniformLocation(shader_lighting, 'material_color')
    M_loc_box = glGetUniformLocation(shader_lighting, 'M')

    # prepare vaos
    vao_axis = prepare_vao_axis()
    vao_grid = prepare_vao_grid()
    vao_box = prepare_vao_box()

    # loop until the user closes the window
    while not glfwWindowShouldClose(window):
        # render

        # enable depth test (we'll see details later)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        # render in "solid mode"
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glUseProgram(shader_program)

        # projection matrix
        # P = glm.perspective(np.radians(globals.g_cam_zoom), 1, 0.1, 100.)
        P = glm.perspective(45, 1, 0.1, 100.)
        if not globals.g_is_perspective :
            P = glm.ortho(-.02*(globals.g_cam_zoom+45.1),.02*(globals.g_cam_zoom+45.1),-.02*(globals.g_cam_zoom+45.1),.02*(globals.g_cam_zoom+45.1), -10, 90)

        # 타겟 위치
        cameraTarget = glm.vec3(1)
        cameraTarget.x = globals.g_origin_x * np.cos(np.radians(globals.g_azimuth)) + globals.g_origin_z * np.sin(np.radians(globals.g_azimuth))
        cameraTarget.y = 0
        cameraTarget.z = - globals.g_origin_x *np.sin(np.radians(globals.g_azimuth)) + globals.g_origin_z * np.cos(np.radians(globals.g_azimuth))
        glm.normalize(cameraTarget)

        # 카메라 위치
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

        view_pos = cameraPos

        V = glm.lookAt(cameraPos, cameraTarget, glm.vec3(0,1,0))

        # current frame: P*V*I (now this is the world frame)
        M = glm.mat4()
        MVP = P*V*M

        # draw
        draw_axis(vao_axis, MVP, MVP_loc_frame)
        draw_grid(vao_grid, MVP, MVP_loc_frame)

        if globals.g_lock is False:
            if globals.g_line_mode :
                glUseProgram(shader_line)
                if globals.g_animate_mode:
                    # line mode, animating
                    i = int(((glfwGetTime()-globals.g_time_press_space) / globals.g_frame_time) % globals.g_frame_cnt)
                    for node in globals.g_nodes:
                        link = glm.mat4()
                        joint = glm.mat4()
                        for j, type in zip(node.columnIndex, node.channels):
                            frame = globals.g_frame_arr[i][j]
                            if type.upper() == 'XROTATION':
                                joint = joint * glm.rotate(glm.radians(frame), glm.vec3(1,0,0))
                            elif type.upper() == 'YROTATION':
                                joint = joint * glm.rotate(glm.radians(frame), glm.vec3(0,1,0))
                            elif type.upper() == 'ZROTATION':
                                joint = joint * glm.rotate(glm.radians(frame), glm.vec3(0,0,1))
                            elif type.upper() == 'XPOSITION':
                                frame /= globals.g_scale
                                link = link * glm.translate(glm.vec3(frame,0,0))
                            elif type.upper() == 'YPOSITION':
                                frame /= globals.g_scale
                                link = link * glm.translate(glm.vec3(0,frame,0))
                            elif type.upper() == 'ZPOSITION':
                                frame /= globals.g_scale
                                link = link * glm.translate(glm.vec3(0,0,frame))
                        if node.parent is None:
                            node.set_link_transform(link)
                        node.set_joint_transform(joint)
                    globals.g_nodes[0].update_tree_global_transform()
                    # print(globals.g_nodes[0].link_transform_from_parent)
                    for node in globals.g_nodes[1:]:
                        vao_line = prepare_vao_line(node.parent.position, node.position)
                        draw_node_line(vao_line, node, MVP, MVP_loc_line, color_loc)
                else:
                    # line mode, rest pose
                    globals.g_nodes[0].update_tree_global_transform()
                    for node in globals.g_nodes[1:]:
                        vao_line = prepare_vao_line(node.parent.position, node.position)
                        draw_node_line(vao_line, node, MVP, MVP_loc_line, color_loc)
            else :
                glUseProgram(shader_lighting)
                if globals.g_animate_mode:
                    # box mode, animating
                    i = int(((glfwGetTime()-globals.g_time_press_space) / globals.g_frame_time) % globals.g_frame_cnt)
                    for node in globals.g_nodes:
                        link = glm.mat4()
                        joint = glm.mat4()
                        for j, type in zip(node.columnIndex, node.channels):
                            frame = globals.g_frame_arr[i][j]
                            if type.upper() == 'XROTATION':
                                joint = joint * glm.rotate(glm.radians(frame), glm.vec3(1,0,0))
                            elif type.upper() == 'YROTATION':
                                joint = joint * glm.rotate(glm.radians(frame), glm.vec3(0,1,0))
                            elif type.upper() == 'ZROTATION':
                                joint = joint * glm.rotate(glm.radians(frame), glm.vec3(0,0,1))
                            elif type.upper() == 'XPOSITION':
                                frame /= globals.g_scale
                                link = link * glm.translate(glm.vec3(frame,0,0))
                            elif type.upper() == 'YPOSITION':
                                frame /= globals.g_scale
                                link = link * glm.translate(glm.vec3(0,frame,0))
                            elif type.upper() == 'ZPOSITION':
                                frame /= globals.g_scale
                                link = link * glm.translate(glm.vec3(0,0,frame))
                        if node.parent is None:
                            node.set_link_transform(link)
                        node.set_joint_transform(joint)
                    globals.g_nodes[0].update_tree_global_transform()
                    # print(globals.g_nodes[0].link_transform_from_parent)
                    for node in globals.g_nodes[1:]:
                        draw_node_box(vao_box, node, P*V, MVP_loc_box, M_loc_box, material_color_loc, view_pos, view_pos_loc)
                else:
                    # box mode, rest pose
                    globals.g_nodes[0].update_tree_global_transform()
                    for node in globals.g_nodes:
                        draw_node_box(vao_box, node, P*V, MVP_loc_box, M_loc_box, material_color_loc, view_pos, view_pos_loc)

        # swap front and back buffers
        glfwSwapBuffers(window)

        # poll events
        glfwPollEvents()

    # terminate glfw
    glfwTerminate()

if __name__ == "__main__":
    main()
