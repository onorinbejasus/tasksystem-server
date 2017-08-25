from django.test import TestCase
from rest_framework.test import APIRequestFactory

factor = APIRequestFactory()

class LoginTestCase(TestCase):
  def test_login_success(self):
    pass
  def test_login_failure(self):
    pass
  def test_logout(self):
    pass

class TaskSelectionTestCase(TestCase):
  def test_list_available_tasks(self):
    pass
  def test_list_user_tasks(self):
    pass
  def test_accept_task_available(self):
    pass
  def test_accept_task_unavailable(self):
    pass
  def test_remove_task_success(self):
    pass
  def test_remove_task_wrong_user(self):
    pass
  def test_remove_task_nontaken(self):
    pass

