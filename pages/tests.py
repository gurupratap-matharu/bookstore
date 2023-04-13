from django.test import SimpleTestCase
from django.urls import resolve, reverse

from .views import AboutPageView, HomePageView


class HomepageTests(SimpleTestCase):
    def setUp(self):
        url = reverse("home")
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, "home.html")

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, "Homepage")

    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "hi there! I should be on the page")

    def test_homepage_url_resolves_homepageview(self):
        view = resolve("/")
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)


class AboutPageTests(SimpleTestCase):
    def setUp(self):
        url = reverse("about")
        self.response = self.client.get(url)

    def test_about_page_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_about_page_template(self):
        self.assertTemplateUsed(self.response, "about.html")

    def test_about_page_contains_correct_html(self):
        self.assertContains(self.response, "About Page")

    def test_about_page_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hey, I should not be on the page")

    def test_about_page_url_resolves_about_page_view(self):
        view = resolve("/about/")
        self.assertEqual(view.func.__name__, AboutPageView.as_view().__name__)
