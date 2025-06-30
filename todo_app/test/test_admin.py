from .utils import *
from todo_app.routers.admin import get_db,get_current_user
from fastapi import status
from todo_app.models import Todos


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_readAll_authenticated(test_todo):
    response = client.get("/auth/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete':False,'title':'learn to code',
                                'description':'need to learn','id':1,
                                'priority':5,'owner_id':1}]
    
    
def test_admin_delete_todo(test_todo):
    response = client.delete("/auth/todo/1")
    assert response.status_code == 204
    
    db = TestingSessionlocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None
    

def test_admin_delete_todo_not_found():
    resopnse = client.delete("/auth/todo/9999")
    assert resopnse.status_code == 404
    assert resopnse.json() == {'detail':'todos not found'}

    
    
    
    
    
    
    
    
    