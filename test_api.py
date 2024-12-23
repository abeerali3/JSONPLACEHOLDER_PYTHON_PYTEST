import time
import pytest
import requests
import json


@pytest.fixture
def api_setup():
    base_url = 'https://jsonplaceholder.typicode.com'
    header = {'Content-Type': 'application/json'}
    return base_url, header


#GET REQUEST
def test_get_request_status_code(api_setup):
    base_url, header = api_setup
    response = requests.get(url=base_url + '/posts/2')  
    assert response.status_code == 200

def test_get_comment_status_code(api_setup):
    base_url, header = api_setup
    response = requests.get(url=base_url + '/posts/1/comments')  
    assert response.status_code == 200
    
    
def test_get_request_title(api_setup):
    base_url, header = api_setup
    response = requests.get(url=base_url + '/posts/50')  
    response_json = response.json()
    assert 'title' in response_json



def test_get_request_body(api_setup):
    base_url, header = api_setup
    response = requests.get(url=base_url + '/posts/25')  
    response_json = response.json()
    assert 'body' in response_json

def test_get_request_content_type(api_setup): 
    base_url, header = api_setup 
    response = requests.get(url=base_url + '/posts/2') 
    assert response.headers['Content-Type']
    
def test_get_request_specific_field(api_setup): 
    base_url, header = api_setup 
    response = requests.get(url=base_url + '/posts/2') 
    response_json = response.json() 
    assert 'title' in response_json 
    assert response_json['title'] == 'qui est esse'

#POST REQUEST
def test_post_request_status_code(api_setup):
    base_url, header = api_setup
    with open('./test_data.json') as json_file:
        json_load = json.load(json_file)
    response = requests.post(url=base_url + '/posts', headers=header, json=json_load[1])
    assert 201 == response.status_code


def test_post_request_contains_user_id(api_setup):
    base_url, header = api_setup
    with open('./test_data.json') as json_file:
        json_load = json.load(json_file)
    response = requests.post(url=base_url + '/posts', headers=header, json=json_load[2])
    response_json = response.json()
    # Assert that 'userId' is in the response
    assert 'userId' in response_json


def test_post_request_contains_title(api_setup):
    base_url, header = api_setup
    with open('./test_data.json') as json_file:
        json_load = json.load(json_file)
    response = requests.post(url=base_url + '/posts', headers=header, json=json_load[1])
    response_json = response.json()
    assert 'body' in response_json


def test_post_request_data_correctness(api_setup):
    base_url, header = api_setup
    with open('./test_data.json') as json_file:
        json_load = json.load(json_file)
    response = requests.post(url=base_url + '/posts', headers=header, json=json_load[0])
    response_json = response.json()
    
    # Assert that the title and body are returned correctly in the response
    assert json_load[0]['title'] == response_json['title']
    assert json_load[0]['body'] == response_json['body']

def test_create_post_response_time(api_setup): 
    base_url, header = api_setup 
    new_post = {"userId": 1, "title": "Response Time Check", "body": "Checking response time."} 
    start_time = time.time() 
    response = requests.post(url=base_url + '/posts', data=json.dumps(new_post), headers=header) 
    end_time = time.time() 
    assert response.status_code == 201 
    assert end_time - start_time < 0.7
    
#PUT REQUEST
def test_put_request_status_code(api_setup):
    base_url, header = api_setup
    with open('./test_data.json') as json_file:
        data = json.load(json_file)
    response = requests.put(url=base_url + '/posts/1', json=data, headers=header)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"



def test_put_request_response_body(api_setup):
    base_url, header = api_setup
    with open('./test_data.json') as json_file:
        data = json.load(json_file)
    response = requests.put(url=base_url + '/posts/1', json=data, headers=header)
    response_json = response.json()
    assert 'id' in response_json, "Response does not contain 'id' field"
    assert response_json['id'] == 1, f"Expected 'id' to be 1, got {response_json['id']}"


def test_put_request_no_error_in_response(api_setup):
    base_url, header = api_setup
    with open('./test_data.json') as json_file:
        data = json.load(json_file)
    response = requests.put(url=base_url + '/posts/1', json=data, headers=header)
    response_json = response.json()
    assert 'error' not in response_json, f"Response contains error: {response_json.get('error')}"
    
def test_put_update_post_title(api_setup): 
    base_url, header = api_setup 
    post_id = 50 
    updated_post = {"title": "Updated Title", "body": "This is a new post."} 
    response = requests.put(url=f"{base_url}/posts/{post_id}", data=json.dumps(updated_post), headers=header) 
    assert response.status_code == 200
    assert response.json().get('title') =="Updated Title"
    
    
#DELETE REQUEST 
def test_delete_request_status_code(api_setup):
    base_url, header = api_setup
    response = requests.delete(url=base_url + '/posts/3')  
    assert response.status_code in [200, 202, 204], f"Unexpected status code: {response.status_code}"


def test_delete_request_response_time(api_setup):
    base_url, header = api_setup
    start_time = time.time()
    response = requests.delete(url=base_url + '/posts/3')  
    response_time = time.time() - start_time
    assert response_time < 0.5 
    
    
def test_delete_request_empty_body(api_setup):
    base_url, header = api_setup
    response = requests.delete(url=base_url + '/posts/3') 
    response_json = response.json()
    assert response_json == {}, f"Response body is not empty: {response_json}"


def test_delete_request_no_error(api_setup):
    base_url, header = api_setup
    response = requests.delete(url=base_url + '/posts/3') 
    response_json = response.json()
    assert 'error' not in response_json, f"Response contains error: {response_json.get('error')}"


#PATCH
def test_patch_update_post_title(api_setup): 
    base_url, header = api_setup 
    post_id = 60 
    updated_field = {"title": "Partially Updated Title"} 
    response = requests.patch(url=f"{base_url}/posts/{post_id}", data=json.dumps(updated_field), headers=header) 
    assert response.status_code == 200 
    assert response.json().get('title') == "Partially Updated Title"
    
    
def test_patch_update_post_title_and_body(api_setup): 
    base_url, header = api_setup 
    post_id = 62 
    updated_fields = {"title": "Partially Updated Title", "body": "Partially updated content of the post."} 
    response = requests.patch(url=f"{base_url}/posts/{post_id}", data=json.dumps(updated_fields), headers=header) 
    assert response.status_code == 200 
    assert response.json().get('title') == "Partially Updated Title" 
    assert response.json().get('body')
    
    
#GET
def test_get_request_status_code2(api_setup):
    base_url, header = api_setup
    response = requests.get(url=base_url + '/posts/5/comments')  
    assert response.status_code == 200
    
    
def test_get_request_content_type2(api_setup): 
    base_url, header = api_setup 
    response = requests.get(url=base_url + '/posts/2/comments') 
    assert response.headers['Content-Type']