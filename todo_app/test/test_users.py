from .utils import *
from todo_app.routers.users import get_db,get_current_user
from fastapi import status
# from sqlalchemy.orm import declarative_base
# Base = declarative_base()


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK 
    assert response.json()['username'] == 'my-name'
    assert response.json()['username'] =='my-name'
    assert response.json()['email' ] == 'code@gmail.com'
    assert response.json()['first_name' ] == 'anas'
    assert response.json()['last_name' ] == 'bhai'
    assert response.json()['role' ] == 'admin'
    assert response.json()['phone_number' ] == '1234567890'
    
def test_change_password_success(test_user):
    response = client.put("/user/password",json={"password":"test1234",
                                                 "new_password":"newpassword"})
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    

def test_change_password_invalid_current_password(test_user):
    response = client.put("/user/password",json={"password":"wrong_password",
                                                 "new_password":"newpassword"})
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail':'Error on password changed'}
    

def test_change_phone_number_success(test_user):
    response = client.put("/user/phone_number", json={
        "phone_number": "1234567890",
        "new_phone_number": "2222222222"
    })
    assert response.status_code == status.HTTP_204_NO_CONTENT
