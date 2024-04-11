import re
from typing import Optional
from pydantic import BaseModel, validator
from fastapi import  Query



class CreateAddressInfo(BaseModel):
    country: str
    state: str
    city: str
    area: str
    pincode: int
    latitude: float
    longitude: float
    landmark: Optional[str]
   
    @validator('pincode')
    def validate_pincode(cls, value):
        pincode = str(value)
        PINCODE_REGEX = "^[1-9]{1}[0-9]{5}$"
        pincode = re.match(PINCODE_REGEX, pincode)
        if (pincode is None):
            raise ValueError('Pincode value should be of 6 digits only.')
        return value
    class Config:
        orm_mode=True

    



class AddressSearchCriteria(BaseModel):
    country: Optional[str]
    state: Optional[str]
    city: Optional[str]
    area: Optional[str]
    pincode: Optional[int]
    latitude: Optional[float]
    longitude:Optional[float]
    landmark: Optional[str]
    is_active: Optional[bool]

    page_size: Optional[int] = Query(20, strict=True, ge=20, le=200, multiple_of=1)
    current_page: Optional[int] = Query(1, strict=True, ge=1)

    class Config:
        orm_mode=True




class UpdateAddress(BaseModel):
    country: Optional[str]
    state: Optional[str]
    city: Optional[str]
    area: Optional[str]
    pincode: Optional[int]
    latitude: Optional[float]
    longitude:Optional[float]
    landmark: Optional[str]
    is_active: Optional[bool]
    
    class Config:
        orm_mode=True        