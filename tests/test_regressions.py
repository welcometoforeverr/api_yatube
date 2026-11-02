"""Проверки вложенных адресов и неизменяемых связей."""
import pytest

from posts.models import Comment, Post

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize('method', ['get', 'put', 'patch', 'delete'])
def test_comment_cannot_be_accessed_through_another_post(
        user_client, post, comment_1_another_post, method):
    """Комментарий нельзя читать или менять через адрес чужого поста."""
    url = (f'/api/v1/posts/{post.pk}/comments/'
           f'{comment_1_another_post.pk}/')
    response = getattr(user_client, method)(url, {'text': 'Новый текст'})
    assert response.status_code == 404
    comment_1_another_post.refresh_from_db()
    assert comment_1_another_post.text == 'Коммент 12'


@pytest.mark.parametrize('method', ['get', 'post'])
def test_missing_parent_post_returns_404(user_client, method):
    """Даже пустой список комментариев требует существующего поста."""
    response = getattr(user_client, method)(
        '/api/v1/posts/999999/comments/', {'text': 'Комментарий'},
    )
    assert response.status_code == 404


def test_post_author_cannot_be_spoofed(user_client, user, another_user):
    """Присланный автор игнорируется при создании поста."""
    response = user_client.post('/api/v1/posts/', {
        'text': 'Новый пост', 'author': another_user.pk,
    })
    assert response.status_code == 201
    assert Post.objects.get(pk=response.data['id']).author == user


def test_comment_relations_cannot_be_spoofed(
        user_client, user, another_user, post, another_post):
    """Автор задаётся токеном, а пост — вложенным адресом."""
    response = user_client.post(f'/api/v1/posts/{post.pk}/comments/', {
        'text': 'Новый комментарий',
        'author': another_user.pk,
        'post': another_post.pk,
    })
    assert response.status_code == 201
    comment = Comment.objects.get(pk=response.data['id'])
    assert comment.author == user
    assert comment.post == post


@pytest.mark.parametrize('method', ['put', 'patch'])
def test_comment_relations_cannot_be_changed(
        user_client, user, another_user, post, another_post,
        comment_1_post, method):
    """При изменении текста нельзя переназначить автора и пост."""
    response = getattr(user_client, method)(
        f'/api/v1/posts/{post.pk}/comments/{comment_1_post.pk}/',
        {'text': 'Изменено', 'author': another_user.pk,
         'post': another_post.pk},
    )
    assert response.status_code == 200
    comment_1_post.refresh_from_db()
    assert comment_1_post.author == user
    assert comment_1_post.post == post


def test_author_can_delete_comment(user_client, post, comment_1_post):
    """Автор удаляет комментарий; исходный набор пропускает этот случай."""
    pk = comment_1_post.pk
    response = user_client.delete(
        f'/api/v1/posts/{post.pk}/comments/{pk}/',
    )
    assert response.status_code == 204
    assert not Comment.objects.filter(pk=pk).exists()
