"""Stores the Node class"""
from data import Split, Rect


class Node:
    """Stores all information on a window.

    Attributes:
        children (list): holds all childen Nodes.
        parent (Node): parent Node.
        window (Window): the window held by this Node.
        split (Split): Direction node is split for children.
        rect (Rect): x, y, w, h coordinates of window
        ratio (int): ratio of split for children.
    """

    def __init__(self, window=None, parent=None, rootSize=None):
        """Initializes the node. Tells the parent this is a child.
        Calculates the type of split.
        """
        self.parent = parent
        self.window = window

        self.first = None
        self.second = None

        self.rect = None
        self.split = None

        # TODO change ratio
        self.ratio = .5

    def update(self):
        """Updates a window by setting new split and rect.
            IF the rect has changed, then the window will move.
        """
        if self.window is not None:
            old_rect = Rect(*self.window.get_rect())
        else:
            old_rect = self.rect

        self.set_split()
        self.set_rect()
        if self.rect != old_rect and self.window is not None:
            self.window.move(self.rect)

    def set_split(self):
        """Updates the node's split if it is None to be opposite of parents.
        """
        if self.split is None:
            self.split = self.parent.split.swap() if self.parent is not None \
                else Split.horz

    def set_rect(self):
        """Updates the node's rect. Based on parent.
        """
        if self.parent is None:
            return self.rect

        # TODO: gap
        if self.parent.split == Split.horz:
            self.rect = Rect(self.parent.rect.x,
                             self.parent.rect.y +
                             (0 if self.is_first_child()
                              else self.parent.rect.h * self.parent.ratio),
                             self.parent.rect.w,
                             self.parent.rect.h * self.parent.ratio)
        else:
            self.rect = Rect(self.parent.rect.x +
                             (0 if self.is_first_child()
                              else self.parent.rect.w * self.parent.ratio),
                             self.parent.rect.y,
                             self.parent.rect.w * self.parent.ratio,
                             self.parent.rect.h)

    def __str__(self):
        """Returns a string representation of the Node.
        """
        if self.window:
            return '[*Node*,h:{0}]'.format(self.window.hwnd)
        else:
            return '[Internal,p:{0}]'.format(self.parent)

    def is_first_child(self):
        """Returns if the node is the first child of its parent.
        """
        return self.parent is not None and self.parent.first == self

    def is_second_child(self):
        """Returns if the node is the second child of its parent.
        """
        return self.parent is not None and self.parent.second == self

    def is_leaf(self):
        """Returns if the node is a leaf node.
        """
        return self.first is None or self.second is None
