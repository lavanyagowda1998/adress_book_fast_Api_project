from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import HTTPException

from ..dao import db_model as address_db_model
from ..repository import address_book_repository
from ..dto import request_model





async def create_address_details(
    session:AsyncSession,
    address_model: request_model.CreateAddressInfo
):

    db_new_address = await address_book_repository.create_address_details(
        session=session, address_model=address_model
    )
    return db_new_address



async def get_address_details(
    session: AsyncSession,
    search_criteria: request_model.AddressSearchCriteria,
):
    offset = (search_criteria.current_page - 1) * search_criteria.page_size
    limit = search_criteria.page_size

    query_statement = (
        generate_address_query_statement(
            search_criteria=search_criteria
        ).offset(offset).limit(limit)
    )

    address_list = (
        await address_book_repository.get_address_by_search_criteria(
            query_statement=query_statement,
            session=session
        )
    )
    
    total_address_list = len(address_list)
    last_page = True
    if total_address_list == limit:
        last_page = False
    
    return {"address_list": address_list, "is_last_page": last_page}


def generate_address_query_statement(
    search_criteria: request_model.AddressSearchCriteria,
   
):
    
    query_statement = select(address_db_model.AddressInfo)

    if search_criteria.state != None:
        query_statement = query_statement.where(
            address_db_model.AddressInfo.state.ilike("{}%".format(search_criteria.state))
        )

    if search_criteria.city != None:
        query_statement = query_statement.where(
            address_db_model.AddressInfo.city.ilike("{}%".format(search_criteria.city))
        )    


    if search_criteria.area != None:
        query_statement = query_statement.where(
            address_db_model.AddressInfo.area.ilike("{}%".format(search_criteria.area))
        )     
        
    if search_criteria.pincode != None:
        query_statement = query_statement.where(
            address_db_model.AddressInfo.pincode == search_criteria.pincode
        )

    if search_criteria.latitude != None:
        query_statement = query_statement.where(
            address_db_model.AddressInfo.latitude == search_criteria.latitude
        ) 

    if search_criteria.longitude != None:
        query_statement = query_statement.where(
            address_db_model.AddressInfo.longitude == search_criteria.longitude
        )          

    if search_criteria.landmark != None:
        query_statement = query_statement.where(
            address_db_model.AddressInfo.landmark.ilike("{}%".format(search_criteria.landmark))
        )     
    
    if search_criteria.is_active != None:
        query_statement = query_statement.where(
          address_db_model.AddressInfo.is_active == search_criteria.is_active
        )
                         
    return query_statement



async def update_address_details_by_id(
    update_model: request_model.UpdateAddress, 
    id: int,
    session: AsyncSession,
   
):
    get_address_by_id = await address_book_repository.get_address_details_by_id(
        session=session,
        id = id,
        
    )
    if get_address_by_id is None:
        raise HTTPException(
            status_code=400,
            detail="address id {} doesnot exists!".format(id)
        )
    
    
    updated_data = await address_book_repository.update_address_information(
        session=session, dbo=get_address_by_id, items=update_model
    )

    return updated_data



async def delete_address_by_id(
    id: int,
    session: AsyncSession
):
 
    address = await address_book_repository.get_address_details_by_id(
        session=session, id=id
    )
    if address is None:
        raise HTTPException(
            status_code=400,
            detail="address id {} not exist!".format(id)
        )
    delete_address = await address_book_repository.delete_address_by_id(
        session=session, address_data=address,
    
    )
    return delete_address
