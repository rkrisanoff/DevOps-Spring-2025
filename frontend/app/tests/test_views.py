import json
from unittest.mock import Mock, patch

from django.test import Client, TestCase
from django.urls import reverse


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.mock_response = Mock()
        self.mock_response.status_code = 200
        self.mock_response.json.return_value = {
            "id": 1,
            "title": "Test Book",
            "author": "Test Author",
        }

    @patch("requests.get")
    def test_get_books(self, mock_get):
        mock_get.return_value = self.mock_response

        response = self.client.get(reverse("get_books"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), self.mock_response.json())

    @patch("requests.get")
    def test_get_books_with_pagination(self, mock_get):
        mock_get.return_value = self.mock_response

        response = self.client.get(reverse("get_books"), {"offset": 5, "limit": 10})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), self.mock_response.json())

    @patch("requests.get")
    def test_get_book(self, mock_get):
        mock_get.return_value = self.mock_response

        response = self.client.get(reverse("get_book", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), self.mock_response.json())

    @patch("requests.post")
    def test_create_book(self, mock_post):
        mock_post.return_value = self.mock_response
        book_data = {"title": "New Book", "author": "New Author"}

        response = self.client.post(
            reverse("create_book"), data=json.dumps(book_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), self.mock_response.json())

    @patch("requests.patch")
    def test_update_book(self, mock_patch):
        mock_patch.return_value = self.mock_response
        book_data = {"id": 1, "title": "Updated Book", "author": "Updated Author"}

        response = self.client.patch(
            reverse("update_book"), data=json.dumps(book_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), self.mock_response.json())

    @patch("requests.delete")
    def test_delete_book(self, mock_delete):
        mock_delete.return_value = Mock(status_code=204)

        response = self.client.delete(reverse("delete_book", args=[1]))
        self.assertEqual(response.status_code, 204)

    @patch("requests.get")
    def test_get_recommendations(self, mock_get):
        mock_get.return_value = self.mock_response

        response = self.client.get(reverse("get_recommendations", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), self.mock_response.json())

    @patch("requests.get")
    def test_get_recommendations_with_pagination(self, mock_get):
        mock_get.return_value = self.mock_response

        response = self.client.get(
            reverse("get_recommendations", args=[1]), {"offset": 5, "limit": 10}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), self.mock_response.json())

    @patch("requests.Session")
    def test_backend_health_check_success(self, mock_session):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"version": "1.0.0"}
        mock_session_instance = Mock()
        mock_session_instance.get.return_value = mock_response
        mock_session.return_value = mock_session_instance

        response = self.client.get(reverse("backend_health_check"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"version": "1.0.0"})

    @patch("requests.Session")
    def test_backend_health_check_failure(self, mock_session):
        mock_session_instance = Mock()
        mock_session_instance.get.side_effect = Exception("Connection error")
        mock_session.return_value = mock_session_instance

        response = self.client.get(reverse("backend_health_check"))
        self.assertEqual(response.status_code, 500)
        self.assertEqual(json.loads(response.content), {})

    def test_frontend_health_check(self):
        response = self.client.get(reverse("frontend_health_check"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"version": "0.1.0"})

    def test_main_screen(self):
        response = self.client.get(reverse("main_screen"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "simple.html")

    # Error cases
    @patch("requests.get")
    def test_get_books_error(self, mock_get):
        mock_get.side_effect = Exception("Connection error")

        response = self.client.get(reverse("get_books"))
        self.assertEqual(response.status_code, 500)
        self.assertEqual(json.loads(response.content), {"error": "Connection error"})

    @patch("requests.post")
    def test_create_book_invalid_method(self, mock_post):
        response = self.client.get(reverse("create_book"))
        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            json.loads(response.content), {"status": "error", "message": "Invalid request method"}
        )

    @patch("requests.patch")
    def test_update_book_invalid_method(self, mock_patch):
        response = self.client.get(reverse("update_book"))
        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            json.loads(response.content), {"status": "error", "message": "Invalid request method"}
        )
