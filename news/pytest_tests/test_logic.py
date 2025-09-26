from pytest_django.asserts import assertRedirects, assertFormError
import pytest

from django.urls import reverse
from news.models import News, Comment
from http import HTTPStatus
from pytest_lazy_fixtures import lf
from news.forms import BAD_WORDS, WARNING

@pytest.mark.django_db
def test_user_can_create_comment(
    news, news_id_for_args, form_data, author_client
):
    url = reverse('news:detail', args=news_id_for_args)
    response = author_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == 1


@pytest.mark.django_db
def test_anonymous_cant_create_comment(
    client, news, news_id_for_args, form_data
):
    url = reverse('news:detail', args=news_id_for_args)
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    assertRedirects(response, f'{login_url}?next={url}')
    assert Comment.objects.count() == 0

@pytest.mark.django_db
def test_user_cant_use_bad_words(
    news, news_id_for_args, author_client
):
    url = reverse('news:detail', args=news_id_for_args)
    bad_words_date = {'text': f'Какой то текс, {BAD_WORDS[0]}, ещё текст'}
    response = author_client.post(url, data=bad_words_date)
    form = response.context['form']
    assertFormError(
        form=form,
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == 0

@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, status, text',
    (
        (lf('author_client'), HTTPStatus.FOUND, 'Новый текст'),
        (lf('not_author_client'), HTTPStatus.NOT_FOUND, 'Текст комментария'),
    )
)
def test_user_author_edit_comment(
    parametrized_client, status, text, news, comment, comment_id_for_args, form_data
):
    url = reverse('news:edit', args=comment_id_for_args)
    response = parametrized_client.post(url, data=form_data)
    assert response.status_code == status
    comment.refresh_from_db()
    assert comment.text == text

@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, status, count',
    (
        (lf('author_client'), HTTPStatus.FOUND, 0),
        (lf('not_author_client'), HTTPStatus.NOT_FOUND, 1),
    )
)
def test_user_author_delet_comment(
    parametrized_client, status, count, news, comment, comment_id_for_args
):
    url = reverse('news:delete', args=comment_id_for_args)
    response = parametrized_client.delete(url)
    assert response.status_code == status
    assert Comment.objects.count() == count
