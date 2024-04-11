from pydantic.main import BaseModel
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from ..dto import request_model
from ..dao import db_model


async def create_address_details(
    session:AsyncSession,
    address_model: request_model.CreateAddressInfo,
):

    db_address_info = db_model.AddressInfo.from_orm(address_model)
    session.add(db_address_info)
    await session.flush()
    await session.commit()
    await session.refresh(db_address_info)
    return db_address_info



async def get_address_by_search_criteria(session: AsyncSession, query_statement: BaseModel):
    result = await session.execute(query_statement)
    postoffice = result.scalars().all()
    return postoffice




async def update_address_information(
    session: AsyncSession,
    dbo: db_model.AddressInfo,
    items: request_model.UpdateAddress,
   
):    
  
    dbo_obj = items.dict(exclude_unset=True)
    for key, value in dbo_obj.items():
        if value is not None:
            setattr(dbo, key, value)
            
    session.add(dbo)
    await session.commit()
    await session.refresh(dbo)
    return dbo


async def get_address_details_by_id(
    session:AsyncSession,
    id:int,
   
):
    query_statement = select(db_model.AddressInfo).where(db_model.AddressInfo.id == id)
    execute_query = await session.execute(query_statement)
    response = execute_query.scalars().first()
    return response





async def delete_address_by_id(
    session: AsyncSession, 
    address_data: db_model.AddressInfo,
  
):    
    await session.delete(address_data)    
    await session.commit()
    return address_data
