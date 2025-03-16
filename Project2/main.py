from OpenGL.GL import *
from glfw.GLFW import *
import glm
import numpy as np

from vao import prepare_vao_axis, prepare_vao_grid, prepare_vao_obj, prepare_vao_objfile
from load_shader import load_shaders
from shader import g_vertex_shader_src, g_fragment_shader_src, g_vertex_shader_src_lighting, g_fragment_shader_src_lighting
import globals
from input_callback import key_callback, cursor_callback, scroll_callback, drop_callback
from draw import draw_axis, draw_grid, draw_obj, draw_node
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
    window = glfwCreateWindow(1200, 1000, 'Project2', None, None)
    if not window:
        glfwTerminate()
        return
    glfwMakeContextCurrent(window)

    # register event callbacks
    glfwSetKeyCallback(window, key_callback)
    glfwSetCursorPosCallback(window, cursor_callback)
    glfwSetScrollCallback(window, scroll_callback)
    glfwSetDropCallback(window, drop_callback)

    # load shaders
    shader_program = load_shaders(g_vertex_shader_src, g_fragment_shader_src)
    shader_lighting = load_shaders(g_vertex_shader_src_lighting, g_fragment_shader_src_lighting)

    # get uniform locations
    MVP_loc_frame = glGetUniformLocation(shader_program, 'MVP')
    MVP_loc = glGetUniformLocation(shader_lighting, 'MVP')
    M_loc = glGetUniformLocation(shader_lighting, 'M')
    view_pos_loc = glGetUniformLocation(shader_lighting, 'view_pos')
    material_color_loc = glGetUniformLocation(shader_lighting, 'material_color')

    # prepare vaos
    vao_axis = prepare_vao_axis()
    vao_grid = prepare_vao_grid()

    vao_scene, len_scene = prepare_vao_objfile("./obj/Rectangular_Grass.obj")
    vao_plant, len_plant = prepare_vao_objfile("./obj/house_plant.obj")
    vao_table, len_table = prepare_vao_objfile("./obj/table.obj")
    vao_chair, len_chair = prepare_vao_objfile("./obj/wooden_stool.obj")
    vao_cola, len_cola = prepare_vao_objfile("./obj/coca_cola.obj")

    # create a hierarchical model 
    # parent, scale, color, transfrom
    scene = Node(None, glm.vec3(.03,.03,.03), glm.vec3(.7,.7,.7))
    plant = Node(scene, glm.vec3(.1,.1,.1), glm.vec3(0,1,0))
    table = Node(scene, glm.vec3(2,2,2),glm.vec3(0,0,1))
    chair = Node(table, glm.vec3(.3,.3,.3), glm.vec3(0,0,1))
    cola = Node(table, glm.vec3(.2,.2,.2),glm.vec3(1,0,0))

    # loop until the user closes the window
    while not glfwWindowShouldClose(window):
        # enable depth test (we'll see details later)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        # render in wireframe mode
        if globals.g_is_wireframe :
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        # render in solid mode
        else :
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glUseProgram(shader_program)

        # projection matrix
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

        draw_axis(vao_axis, MVP, MVP_loc_frame)
        draw_grid(vao_grid, MVP, MVP_loc_frame)

        # render object with lighting
        glUseProgram(shader_lighting)
        
        # M = glm.scale(glm.vec3(0.01,0.01,0.01)) # grid 위로 보이도록
        # MVP = P*V*M
        t = glfwGetTime()

        if not globals.g_is_hierarchical and globals.g_vao_obj :
            draw_obj(globals.g_vao_obj, MVP, M, glm.vec3(1,0,0), view_pos, MVP_loc, M_loc, material_color_loc, view_pos_loc)
        elif globals.g_is_hierarchical :          
            # set local transformations of each node
            scene.set_transform(glm.rotate(t/5, glm.vec3(0,1,0))*glm.rotate(glm.radians(-90),glm.vec3(1,0,0)))
            plant.set_transform(glm.translate(glm.vec3(1.5,1.5,.2))*glm.rotate(glm.radians(90),glm.vec3(1,0,0)))
            table.set_transform(glm.translate(glm.vec3(0,np.sin(t),0))*glm.translate(glm.vec3(-1,-1,.5))*glm.rotate(glm.radians(90),glm.vec3(1,0,0)))
            chair.set_transform(glm.translate(glm.vec3(-2,-.2,.5)))
            cola.set_transform(glm.translate(glm.vec3(0,(np.sin(3*t)+1)/4,0))*glm.translate(glm.vec3(0,1.45,0)))

            # recursively update global transformations of all nodes
            scene.update_tree_global_transform()

            # draw nodes
            draw_node(vao_scene, scene, P*V, MVP_loc, material_color_loc,len_scene, view_pos, view_pos_loc, M_loc)
            draw_node(vao_plant, plant, P*V, MVP_loc, material_color_loc, len_plant, view_pos, view_pos_loc, M_loc)
            draw_node(vao_table, table, P*V, MVP_loc, material_color_loc, len_table, view_pos, view_pos_loc, M_loc)
            draw_node(vao_chair, chair, P*V, MVP_loc, material_color_loc, len_chair, view_pos, view_pos_loc, M_loc)
            draw_node(vao_cola, cola, P*V, MVP_loc, material_color_loc, len_cola, view_pos, view_pos_loc, M_loc)           

        # swap front and back buffers
        glfwSwapBuffers(window)

        # poll events
        glfwPollEvents()

    # terminate glfw
    glfwTerminate()

if __name__ == "__main__":
    main()
