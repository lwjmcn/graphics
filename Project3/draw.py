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

def draw_node_line(vao, node, MVP, MVP_loc, color_loc):
    # color = node.get_color()
    glBindVertexArray(vao)
    glUniformMatrix4fv(MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP))
    # glUniform3f(color_loc, color.r, color.g, color.b)
    glUniform3f(color_loc, 0, 0, 1)
    glDrawArrays(GL_LINES, 0, 2)

def draw_node_box(vao, node, VP, MVP_loc, M_loc, material_color_loc, view_pos, view_pos_loc):
    M = node.get_global_transform() # * node.get_shape_transform()
    MVP = VP * M
    color = node.get_color()
    glUniformMatrix4fv(MVP_loc, 1, GL_FALSE, glm.value_ptr(MVP))
    glUniformMatrix4fv(M_loc, 1, GL_FALSE, glm.value_ptr(M))
    glUniform3f(material_color_loc, color.r, color.g, color.b)
    glUniform3f(view_pos_loc, view_pos.x, view_pos.y, view_pos.z)
    glBindVertexArray(vao)
    glDrawArrays(GL_TRIANGLES, 0, 36)