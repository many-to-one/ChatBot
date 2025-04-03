from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from fastapi import HTTPException, Depends, status

from models.models import User
from settings.security import verify_password, get_tokens_pair

class OrmService:
    def __init__(self, db):
        self.db = db

    
    async def login(self, form):
        print('------------------LOGIN--FORM--------------', form)
        result = await self.db.execute(select(User).filter(User.username == form.username))  # Await the query execution
        user = result.scalar_one_or_none() 
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

        if not verify_password(form.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
        
        user.is_active = True
        await self.db.commit()
 
        return await get_tokens_pair(db=self.db, id=user.id)

    
    async def all(self, model, name):

        result = await self.db.execute(select(model))
        obj = result.scalars().all()

        if obj is None:
            raise HTTPException(status_code=404, detail=f"No {name}")
        
        return obj
    

    async def create(self, model, form):

        print(f'create {model} *****************************', model)
        print(f'create {form} *****************************', form)

        if isinstance(form, dict):
            print(f'dict *****************************')
            obj_dict = form
            # obj_dict["chat_user"] = str(obj_dict["chat_user"]) 
            print(f'obj_dict - dict *****************************', obj_dict)
        else:
            print(f'not dict *****************************')
            obj_dict = form.dict()
        # if isinstance(form, RedirectResponse):
        #     form = await form.json()
        # obj_dict = form if isinstance(form, dict) else form.dict()

        obj = model(**obj_dict)
        print(f'create end {obj} *****************************', obj)

        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj
    

    async def get(self, id: int, model, name):

        result = await self.db.execute(select(model).filter(model.id == id))
        obj = result.scalar_one_or_none()

        if obj is None:
            raise HTTPException(status_code=404, detail=f"No {name}")
        
        return obj
    

    async def update(self, form, id, model, name):

        obj = await self.get(id=id, model=model, name=name)
    
        if not obj:
            raise HTTPException(status_code=404, detail=f"No such {name}")
        
        for field, value in form.dict().items():
            if value is not None:
                setattr(obj, field, value)

        await self.db.commit()  
        await self.db.refresh(obj)
        return obj
    

    async def delete(self, id: int, model, name):

        result = await self.db.execute(select(model).filter(model.id == id))
        obj = result.scalar_one_or_none()

        if obj is None:
            raise HTTPException(status_code=404, detail=f"No {name}")
        
        await self.db.delete(obj)
        await self.db.commit()
        await self.db.flush()
        
        return {
            "message": f"{name} deleted successfully!",
            "userMessage": f"Objekt {name} został usunięty!",
            }