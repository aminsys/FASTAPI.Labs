from .. import models, schemas, utils
from fastapi import status, HTTPException, Depends, APIRouter
from ..database import engine, get_db
from sqlalchemy.orm import Session


# Creating a router obejct which will be included in our main file
router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut) # decorator
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Hash the password - user.password
    hashed_pw = utils.hash(user.password)
    user.password = hashed_pw # This will update the pydantic user model.
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/users/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id : {id} does not exist")

    return user