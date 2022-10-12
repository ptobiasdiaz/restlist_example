#!/usr/bin/env python3

import unittest

import restlist.lista

ITEM0 = 'value1'

class TestListImplementation(unittest.TestCase):

    def test_creation(self):
        '''Test instantiation'''
        mylist = restlist.lista.List()
        self.assertEqual(mylist.len(), 0)

    def test_append(self):
        '''Test append item'''
        mylist = restlist.lista.List()
        mylist.append(ITEM0)

        self.assertEqual(mylist.len(), 1)
        self.assertTrue(mylist.exists(ITEM0))
        self.assertEqual(mylist.element_at(0), ITEM0)

    def test_remove(self):
        '''Test remove item'''
        mylist = restlist.lista.List()
        mylist.append(ITEM0)
        self.assertEqual(mylist.len(), 1)
        self.assertTrue(mylist.exists(ITEM0))
        mylist.remove(ITEM0)
        self.assertEqual(mylist.len(), 0)
        self.assertFalse(mylist.exists(ITEM0))

    def test_remove_all(self):
        '''Test remove all occurences of item'''
        mylist = restlist.lista.List()
        mylist.append(ITEM0)
        mylist.append(ITEM0)
        mylist.append(ITEM0)
        self.assertEqual(mylist.len(), 3)
        self.assertTrue(mylist.exists(ITEM0))
        mylist.remove(ITEM0, all_occurrences=True)
        self.assertEqual(mylist.len(), 0)
        self.assertFalse(mylist.exists(ITEM0))
