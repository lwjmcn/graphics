import glm
import globals

class Node:
    def __init__(self, name, parent):
        # hierarchy
        self.name = name
        self.parent = parent
        self.children = []
        self.offset = glm.vec3(0)
        self.columnIndex = []
        self.channels = []
        self.position = glm.vec3(0)
        if parent is not None:
            parent.children.append(self)

        # transform
        self.link_transform_from_parent = glm.mat4()
        self.joint_transform = glm.mat4()
        self.global_transform = glm.mat4()

        # shape
        # self.shape_transform = glm.mat4()
        self.color = glm.vec3(0,0,1)

    def set_link_transform(self, link_transform):
        self.link_transform_from_parent = link_transform

    def set_joint_transform(self, joint_transform):
        self.joint_transform = joint_transform

    def update_tree_global_transform(self):
        if self.parent is not None:
            self.link_transform_from_parent = glm.translate(self.offset / globals.g_scale)

        if self.parent is not None:
            self.global_transform = self.parent.get_global_transform() * self.link_transform_from_parent * self.joint_transform
        else:
            self.global_transform = self.link_transform_from_parent * self.joint_transform

        self.position = (self.global_transform * glm.vec4(0,0,0,1)).xyz

        for child in self.children:
            child.update_tree_global_transform()

    def get_global_transform(self):
        return self.global_transform
    # def get_shape_transform(self):
    #     return self.shape_transform
    def get_color(self):
        return self.color