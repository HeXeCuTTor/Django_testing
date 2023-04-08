import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def make_courses():
    def courses(*args,**kwargs):
        return baker.make(Course,*args, **kwargs)
    
    return courses

@pytest.mark.django_db
def test_find_id(client, make_courses):
    courses = make_courses(_quantity = 10)
    response = client.get('/api/v1/courses/?id=7')
    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == 7

@pytest.mark.django_db
def test_find_name_course(client, make_courses):
    courses = make_courses(_quantity = 10)
    courses.append(Course.objects.create(name = 'Course_4'))
    response = client.get('/api/v1/courses/?name=Course_4')
    assert response.status_code == 200
    data = response.json()
    assert data != []
    assert data[0]['name'] == 'Course_4'

@pytest.mark.django_db
def test_create_course(client):
    response = client.post('/api/v1/courses/', {'id':'1', 'name': 'Course_test'})
    assert response.status_code == 201
    assert Course.objects.values()[0]['name'] == 'Course_test'


@pytest.mark.django_db
def test_update_course(client):
    Course.objects.create(name = 'Course_4')
    id_course = Course.objects.filter(name='Course_4').first().id
    response = client.patch(f'/api/v1/courses/{id_course}/', {'name': 'Course_fix'})
    data = response.json()
    assert response.status_code == 200
    assert Course.objects.filter(id = id_course).values()[0]['name'] == 'Course_fix'

@pytest.mark.django_db
def test_delete_course(client):
    Course.objects.create(name = 'Course_4')
    assert Course.objects.count() == 1
    id = Course.objects.filter(name='Course_4').first().id
    response = client.delete(f'/api/v1/courses/{id}/')
    assert response.status_code == 204
    assert Course.objects.count() == 0


@pytest.mark.django_db
def test_first_id(client, make_courses):
    courses = make_courses(_quantity = 10)
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == courses[0].id

@pytest.mark.django_db
def test_list_name(client, make_courses):
    courses = make_courses(_quantity = 10)
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200
    data = response.json()
    for index, cours in enumerate(data):
        assert cours['name'] == courses[index].name



