from http import HTTPStatus

import factory.fuzzy
import pytest

from fast_zero.models import Todo, TodoState


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker('text')
    description = factory.Faker('text')
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1


# POST /todos/


def test_create_todo(client, token):
    response = client.post(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test todo',
            'description': 'Test todo description',
            'state': 'draft',
        },
    )
    assert response.json() == {
        'id': 1,
        'title': 'Test todo',
        'description': 'Test todo description',
        'state': 'draft',
        'created_at': response.json()['created_at'],
        'updated_at': response.json()['updated_at'],
    }


def test_create_todo_state_error(client, token):
    response = client.post(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test todo',
            'description': 'Test todo description',
            'state': 'invalid',
        },
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


# GET /todos/


@pytest.mark.asyncio
async def test_list_todos_should_return_5_todos(session, client, user, token):
    expected_todos = 5
    todos = TodoFactory.create_batch(expected_todos, user_id=user.id)
    session.add_all(todos)
    await session.commit()

    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
    )

    for i in range(len(response.json()['todos'])):
        assert response.json()['todos'][i]['title'] == todos[i].title
        assert (
            response.json()['todos'][i]['description'] == todos[i].description
        )
        assert response.json()['todos'][i]['state'] == todos[i].state.value


@pytest.mark.asyncio
async def test_list_todos_pagination_should_return_2_todos(
    session, user, client, token
):
    expected_todos = 2
    todos = TodoFactory.create_batch(5, user_id=user.id)
    session.add_all(todos)
    await session.commit()

    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos
    for i in range(len(response.json()['todos'])):
        assert response.json()['todos'][i]['title'] == todos[i + 1].title
        assert (
            response.json()['todos'][i]['description']
            == todos[i + 1].description
        )
        assert response.json()['todos'][i]['state'] == todos[i + 1].state.value


@pytest.mark.asyncio
async def test_list_todos_filter_title_should_return_5_todos(
    session, user, client, token
):
    expected_todos = 5
    todos = TodoFactory.create_batch(5, user_id=user.id, title='Test todo 1')
    session.add_all(todos)
    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, title='Other title')
    )
    await session.commit()

    response = client.get(
        '/todos/?title=Test todo 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos

    for i in range(len(response.json()['todos'])):
        assert response.json()['todos'][i]['title'] == todos[i].title
        assert (
            response.json()['todos'][i]['description'] == todos[i].description
        )
        assert response.json()['todos'][i]['state'] == todos[i].state.value


@pytest.mark.asyncio
async def test_list_todos_filter_description_should_return_5_todos(
    session, user, client, token
):
    expected_todos = 5
    todos = TodoFactory.create_batch(
        5, user_id=user.id, description='description'
    )
    session.add_all(todos)
    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, description='other')
    )
    await session.commit()

    response = client.get(
        '/todos/?description=desc',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos

    for i in range(len(response.json()['todos'])):
        assert response.json()['todos'][i]['title'] == todos[i].title
        assert (
            response.json()['todos'][i]['description'] == todos[i].description
        )
        assert response.json()['todos'][i]['state'] == todos[i].state.value


@pytest.mark.asyncio
async def test_list_todos_filter_state_should_return_5_todos(
    session, user, client, token
):
    expected_todos = 5
    todos = TodoFactory.create_batch(5, user_id=user.id, state=TodoState.draft)
    session.add_all(todos)
    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, state=TodoState.todo)
    )
    await session.commit()

    response = client.get(
        '/todos/?state=draft',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos

    for i in range(len(response.json()['todos'])):
        assert response.json()['todos'][i]['title'] == todos[i].title
        assert (
            response.json()['todos'][i]['description'] == todos[i].description
        )
        assert response.json()['todos'][i]['state'] == todos[i].state.value


@pytest.mark.asyncio
async def test_list_todos_filter_combined_should_return_5_todos(
    session, user, client, token
):
    expected_todos = 5
    todos = TodoFactory.create_batch(
        5,
        user_id=user.id,
        title='Test todo combined',
        description='combined description',
        state=TodoState.done,
    )
    session.add_all(todos)

    session.add_all(
        TodoFactory.create_batch(
            3,
            user_id=user.id,
            title='Other title',
            description='other description',
            state=TodoState.todo,
        )
    )
    await session.commit()

    response = client.get(
        '/todos/?title=Test todo combined&description=combined&state=done',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos

    for i in range(len(response.json()['todos'])):
        assert response.json()['todos'][i]['title'] == todos[i].title
        assert (
            response.json()['todos'][i]['description'] == todos[i].description
        )
        assert response.json()['todos'][i]['state'] == todos[i].state.value


# PATCH /todos/{id}


def test_patch_todo_error(client, token):
    response = client.patch(
        '/todos/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


@pytest.mark.asyncio
async def test_patch_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    await session.commit()

    response = client.patch(
        f'/todos/{todo.id}',
        json={'title': 'teste!'},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'teste!'


# DELETE /todos/{id}


@pytest.mark.asyncio
async def test_delete_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    await session.commit()

    response = client.delete(
        f'/todos/{todo.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Task has been deleted successfully.'
    }


def test_delete_todo_error(client, token):
    response = client.delete(
        f'/todos/{10}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}
