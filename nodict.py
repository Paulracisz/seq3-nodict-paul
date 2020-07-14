#!/usr/bin/env python3
"""
Implementation of the NoDict assignment
"""

__author__ = 'Paul Racisz + Ruben Espino'


class Node:
    def __init__(self, key, value=None):
        """
        Makes several new instance variable,
        and sets up an instance` of an object.
        """
        self.key = key
        self.value = value
        self.hash = hash(key)

    def __repr__(self):
        """
        Returns a representation of an object that is
        passed in with the self variable.
        """
        return f'{self.__class__.__name__}({self.key}, {self.value})'

    def __eq__(self, other):
        """
        Grabs the keys of two objects and compares them to see
        if they are equal and returns a boolean.
        """
        return self.key == other.key


class NoDict:
    def __init__(self, num_buckets=10):
        """
        Class initializer to create the buckets according to a size parameter.
        If nothing is given, default value is 10.
        """
        self.buckets = [[] for _ in range(num_buckets)]
        self.size = num_buckets

    def __repr__(self):
        """
        Return a string representing the no-dict contents.
        """
        # We want to show all the buckets vertically
        return '\n'.join([f'{self.__class__.__name__}.{i}:{bucket}'
                         for i, bucket in enumerate(self.buckets)])

    def add(self, key, value):
        """
        This class method should accept a new key and value, and store
        it in the bucket.
        """
        new_node = Node(key, value)
        bucket = self.buckets[new_node.hash % self.size]
        # iterate through bucket if i is = to node, remove bucket,
        # otherwise append new node to bucket.
        for i in bucket:
            if i == new_node:
                bucket.remove(i)
                break
        bucket.append(new_node)

    def get(self, key):
        """
        This class method should perform a key lookup in the no-dict class.
        It should accept just one parameter: the key to look up.
        If the key is found in the no-dict class, return it's associated value.
        If the key is not found, raise a key error exception.
        """
        node_to_find = Node(key)
        bucket = self.buckets[node_to_find.hash % self.size]
        for i in bucket:
            if i == node_to_find:
                return i.value
        raise KeyError(f'{key} not found')

    def __getitem__(self, key):
        """
        Implement this magic dunder method within the no-dict class,
        to enable square bracket reading behavior.
        """
        value = self.get(key)
        return value

    def __setitem__(self, key, value):
        """
        Implement this magic dunder method within the no-dict class,
        to enable square bracket assignment behavior.
        """
        self.add(key, value)
