from datetime import datetime
import hashlib 
from fastapi import Depends, FastAPI
import logging
from sqlalchemy.orm import Session

from database import db
from crud import write_access_data
from schema import Access_Data
from config import salt

app = FastAPI()


@app.get("/")
async def root():
    """ Root API """
    logging.info("Hello World")
    return {"message": "Hello World"}

@app.post("/access")
async def access(user_id: str, channel_id: str, access_time: datetime, access_db: Session = Depends(db.get_session)):
    """Access API"""
    logging.info("Access API")
    # make Access_Data
    access_id_raw = user_id + channel_id + str(access_time) + salt
    # hash each 5 times
    # for _ in range(5):
    access_id = hashlib.sha256(access_id_raw.encode('utf-8')).hexdigest()
    return write_access_data(access_id, channel_id, access_time, access_db)
