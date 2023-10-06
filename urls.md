### auth/api/token/
- **Method:** POST
- **Data:** {  
  "username": "",  
  "password": ""  
}

### auth/api/token/refresh/
- **Method:** POST
- **Data:** {  
  "refresh": "{{refresh}}"  
}

### auth/api/token/verify/
- **Method:** POST
- **Data:** {  
  "token": "{{access}}"  
}

### auth/api/user/
- **Method:** GET, POST, PATCH, DELETE
- **Permissões:** Authenticated, Admin, IsOwner (GET/PK)
- **Data:** {  
  "username": "",  
  "email": "@aluno.ce.gov.br",  
  "password": "",  
  "confirm_password": ""  
}

### client/api/teacher/
- **Method:** GET, POST, PUT, PATCH, DELETE
- **Permissões:** Authenticated, Admin
- **Data:** {  
  "name": ""  
}

### client/api/discipline/
- **Method:** GET, POST, PUT, PATCH, DELETE
- **Permissões:** Authenticated, Admin
- **Data:** {  
  "name": ""  
}

### client/api/itemlist/
- **Method:** GET, POST, PUT, PATCH, DELETE
- **Permissões:** Authenticated, Admin, IsOwnerItemList (GET/PK, Update)
- **Data:** {  
  "title": "",  
  "content": "",  
  "due_date": "2023-07-22",  
  "status": "TODO / DOING / DONE",  
  "type": "Opcional default P",  
  "discipline": ID,  
  "teacher": ID  
}

### client/api/itemlist-admin/
- **Method:** GET, POST, PUT, PATCH, DELETE
- **Permissões:** Authenticated, Admin
- **Data:** {  
  "title": "",  
  "content": "",  
  "due_date": "2023-07-22",  
  "status": "TODO / DOING / DONE",  
  "type": "Opcional default A",  
  "discipline": ID,  
  "teacher": ID  
}

### client/api/person/
- **Method:** GET
- **Permissões:** Authenticated, Admin, IsOwnerPerson (GET/PK, Update)
