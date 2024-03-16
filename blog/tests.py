from django.test import TestCase

# Create your tests here.
import pytest
from django.urls import reverse
from .models import Post
from .views import BlogListView

# Assuming the Django environment is properly set up for testing
# and pytest-django plugin is installed.

@pytest.mark.django_db
class TestBlogListView:
    # Happy path test with various realistic test values
    @pytest.mark.parametrize("posts_count, expected_count", [
        (0, 0, 'test_id_empty'),  # No posts
        (1, 1, 'test_id_single_post'),  # Single post
        (5, 5, 'test_id_multiple_posts'),  # Multiple posts
    ])
    def test_blog_list_view_happy_path(self, client, posts_count, expected_count):
        # Arrange
        Post.objects.bulk_create([Post(title=f"Post {i}", content="Content") for i in range(posts_count)])
        url = reverse('blog:list')  # Assuming 'blog:list' is the name of the URL pattern for BlogListView

        # Act
        response = client.get(url)

        # Assert
        assert response.status_code == 200
        assert len(response.context['object_list']) == expected_count

    # Edge cases
    @pytest.mark.parametrize("posts_count, expected_count", [
        (10, 10, 'test_id_page_limit'),  # Exactly at page limit
        (11, 10, 'test_id_page_over_limit'),  # Just over the page limit
    ])
    def test_blog_list_view_edge_cases(self, client, posts_count, expected_count):
        # Arrange
        Post.objects.bulk_create([Post(title=f"Post {i}", content="Content") for i in range(posts_count)])
        url = reverse('blog:list')  # Assuming pagination is set up and page limit is 10

        # Act
        response = client.get(url)

        # Assert
        assert response.status_code == 200
        assert len(response.context['object_list']) == expected_count

    # Error cases
    @pytest.mark.parametrize("url, expected_status", [
        ("/invalid-url/", 404, 'test_id_404'),  # Non-existent URL
    ])
    def test_blog_list_view_error_cases(self, client, url, expected_status):
        # Act
        response = client.get(url)

        # Assert
        assert response.status_code == expected_status
