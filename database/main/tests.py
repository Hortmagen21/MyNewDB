from django.test import TestCase
import unittest
from django.test.client import RequestFactory
from . import views
# Create your tests here.


class SimpleTest(unittest.TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_del_same_rows(self):
        request = self.factory.delete('home/db/ForTestPurpose/table/Test/del_same_rows')
        response = views.del_same_rows(request, "ForTestPurpose", "Test")
        self.assertEqual(response.status_code, 200)

    def test_delete_row(self):
        request = self.factory.delete('home/db/ForTestPurpose/table/Test/delete_row/1')
        response = views.delete_row(request, "ForTestPurpose", "Test", "1")
        self.assertEqual(response.status_code, 200)

    def test_delete_table(self):
        request = self.factory.delete('home/db/ForTestPurpose/table/Test/delete_table')
        response = views.del_same_rows(request, "ForTestPurpose", "Test")
        self.assertEqual(response.status_code, 200)
