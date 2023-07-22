import shutil
from fastapi import FastAPI, UploadFile, File, APIRouter,Form
from typing import List
from schemas import UploadVideo

video_router = APIRouter()

@video_router.post('/')
async def root(title: str = Form(...), description: str = Form(...), file: UploadFile = File(...)):
    info = UploadVideo(title=title, description=description)
    with open(f'{file.filename}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {'file_name': file.filename, 'info': info}


@video_router.post('/photos')
async def root(files: List[UploadFile] = File(...)):
    for image in files:
        with open(f'{image.filename}', 'wb') as buffer:
            shutil.copyfileobj(image.file, buffer)

    return {'file_name': 'All good'}


@video_router.post('/info')
async def info_set(info: UploadVideo):
    return info


@video_router.get('/info')
async def info_get():
    title = 'Test'
    desc = 'Description'
    return UploadVideo(title=title, description=desc)