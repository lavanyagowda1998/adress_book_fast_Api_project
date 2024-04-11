from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi.params import Depends
from fastapi import APIRouter
from fastapi_versioning import version

from app.web.db import get_session
from ..services import address_book_services
from ..dto import request_model



router = APIRouter()


@router.post("", status_code=200)
@version(1)
async def create_address_details(
    address_model: request_model.CreateAddressInfo,
    session: AsyncSession =Depends(get_session),
):
    
    address_data = await address_book_services.create_address_details(
        session=session,
        address_model=address_model,
    )
    return address_data


@router.get("",status_code=200)
@version(1)
async def get_address_details_by_search(
    search_address_criteria:request_model.AddressSearchCriteria=Depends(),
    session:AsyncSession=Depends(get_session)
):

    address_list = await address_book_services.get_address_details(
        session=session, search_criteria=search_address_criteria,
    )

    return address_list


@router.put("/{id}", status_code=200)
@version(1)
async def update_address_details_by_id(
    update_model: request_model.UpdateAddress,
    id:int,
    session:AsyncSession=Depends(get_session),
):
   
    details= await address_book_services.update_address_details_by_id(
        session=session,id=id,update_model=update_model
    )
    return details




@router.delete("/{id}", status_code=200)
@version(1)
async def delete(id:int,  session: AsyncSession = Depends(get_session)):
    
    address_data = await address_book_services.delete_address_by_id(
        id=id, session=session
    )
    return address_data
