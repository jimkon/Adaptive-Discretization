#!/usr/bin/python3

import numpy as np


class Node:

    BRANCH_MATRIX = None

    def __init__(self, location, radius, parent):
        self._value = 0
        self._location = location
        self._radius = radius
        self._low_limit = location - radius
        self._high_limit = location + radius
        self._branches = [None] * len(self.BRANCH_MATRIX)
        self._parent = parent

        self.reset_value()

        self.__achieved_precision_limit = False

        if parent is not None:
            self._level = parent._level + 1
            self._value = parent._value
        else:
            self._level = 0

        if np.array_equal(self._low_limit, self._high_limit):
            # print('expansion of', self, 'stopped')
            raise ArithmeticError('Node: Low == High :{}=={}'.format(
                self._low_limit, self._high_limit))

    def expand(self, towards_point=None):
        if not self.is_expandable():
            return []
        new_radius = self._radius / 2

        new_nodes = []
        for i in range(len(self.BRANCH_MATRIX)):
            if self._branches[i] is not None:
                continue

            new_location = self._location + self.BRANCH_MATRIX[i] * new_radius

            try:
                new_node = Node(new_location, new_radius, self)
            except Exception as e:
                self.__achieved_precision_limit = True
                return new_nodes

            if (towards_point is not None) and (not new_node._covers_point(towards_point)):
                continue
            self._branches[i] = new_node
            new_nodes.append(new_node)

        return new_nodes

    def search(self, point, min_dist_till_now=1):
        if not self._covers_point(point):
            return None, 0

        dist_to_self = np.linalg.norm(self._location - point)

        if min_dist_till_now > dist_to_self:
            min_dist_till_now = dist_to_self

        branches = self.get_branches()
        for branch_i in range(len(branches)):
            branch = branches[branch_i]
            res, branch_dist = branch.search(point, min_dist_till_now)
            if res is not None:
                # print('dist to child', branch, '=', branch_dist)

                if branch_dist > dist_to_self:
                    self._value += dist_to_self
                    return res, dist_to_self
                else:
                    self._value_without_branch[branch_i] += dist_to_self
                    return res, branch_dist

        # print(self, point, dist_to_self if min_dist_till_now == dist_to_self else 0)
        self._value += dist_to_self if min_dist_till_now == dist_to_self else 0
        return self, dist_to_self

    def delete(self):
        if self.is_root():
            return
        # uncaught exception !!!!
        self._parent._branches[self._parent._branches.index(self)] = None

    def recursive_collection(self, result_array, func, traverse_cond_func, collect_cond_func):
        if not traverse_cond_func(self):
            return
        if collect_cond_func(self):
            result_array.append(func(self))
        for branch in self.get_branches():
            branch.recursive_collection(result_array, func, traverse_cond_func, collect_cond_func)

    def get_value(self):
        return self._value

    def get_cut_overhead(self):
        temp = self._parent._value_without_branch[self._parent._branches.index(self)]
        return temp - self._value

    def reset_value(self):
        self._value = 0
        self._value_without_branch = np.zeros(len(self.BRANCH_MATRIX))

    def get_level(self):
        return self._level

    def get_location(self):
        return self._location

    def get_connection_with_parent(self):
        if self._parent is None:
            return self._location, self._location

        return self._parent._location, self._location

    def get_branches(self):
        res = []
        for branch in self._branches:
            if branch is not None:
                res.append(branch)
        return res

    def number_of_childs(self):
        return len(self.get_branches())

    def is_root(self):
        return self._parent is None

    def is_leaf(self):
        return len(self.get_branches()) == 0

    def is_expandable(self):
        return self.number_of_childs() < len(self.BRANCH_MATRIX) or self.__achieved_precision_limit

    def _covers_point(self, point):
        check1 = self.point_less_or_equal_than_point(self._low_limit, point)
        check2 = self.point_less_or_equal_than_point(point, self._high_limit)
        return check1 and check2

    def _equals(self, node):
        return np.array_equal(self.get_location(), node.get_location())

    def __str__(self):
        return 'loc={} level={} r={} br={} v={} parent_loc={}'.format(self._location,
                                                                      self._level,
                                                                      self._radius,
                                                                      len(self.get_branches()),
                                                                      self._value,
                                                                      self._parent.get_location() if self._parent is not None else None)

    __repr__ = __str__

    @staticmethod
    def point_less_or_equal_than_point(point1, point2):
        assert len(point1) == len(point2), 'points must have same lenght'
        for i in range(len(point1)):
            if point1[i] > point2[i]:
                return False
        return True

    @staticmethod
    def _init_branch_matrix(dims):
        import itertools
        Node.BRANCH_MATRIX = np.array(list(itertools.product([0, 1], repeat=dims))) * 2 - 1