from OpenGL.GL import *
import glm
import globals

def draw_axis(vao_axis, MVP, MVP_loc):
    glUniformMatrix4fv(MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP))
    glBindVertexArray(vao_axis)
    glDrawArrays(GL_LINES, 0, 4)

def draw_grid(vao_grid, MVP, MVP_loc):
    glUniformMatrix4fv(MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP))
    glBindVertexArray(vao_grid)
    for i in range(9):
        for j in range(9):
            MVP_grid = MVP * glm.translate(glm.vec3(2*(i-4), 0, 2*(j-4)))
            glUniformMatrix4fv(MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP_grid))
            glDrawArrays(GL_LINES, 0, 76)

def draw_obj(vao_obj, MVP, M, material_color, view_pos, MVP_loc, M_loc, material_color_loc, view_pos_loc):
    glUniformMatrix4fv(MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP))
    glUniformMatrix4fv(M_loc, 1, GL_FALSE, glm.value_ptr(M))
    glUniform3f(material_color_loc, material_color.r, material_color.g, material_color.b)
    glUniform3f(view_pos_loc, view_pos.x, view_pos.y, view_pos.z)
    
    glBindVertexArray(vao_obj)
    glDrawArrays(GL_TRIANGLES, 0, len(globals.g_vertex_arr)//2)

def draw_node(vao, node, VP, MVP_loc, color_loc, len,view_pos, view_pos_loc, M_loc):
    M = node.get_global_transform() * glm.scale(node.get_scale())
    MVP = VP * M
    color = node.get_color()
    glUniformMatrix4fv(MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP))
    glUniformMatrix4fv(M_loc, 1, GL_FALSE, glm.value_ptr(M))
    glUniform3f(color_loc, color.r, color.g, color.b)
    glUniform3f(view_pos_loc, view_pos.x, view_pos.y, view_pos.z)

    glBindVertexArray(vao)
    glDrawArrays(GL_TRIANGLES, 0, len)
