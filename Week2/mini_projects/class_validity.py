from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

class UserProfile(BaseModel):
    id: int
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr
    age: Optional[int] = Field(None, ge=0, le=120)
    tags: List[str] = []

def validate_user():
    user_data = {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "age": 25,
        "tags": ["python", "pydantic"]
    }
    
    user = UserProfile(**user_data)
    print(user.model_dump_json(indent=2))

if __name__ == "__main__":
    validate_user()
