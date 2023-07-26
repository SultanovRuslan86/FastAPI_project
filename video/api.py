import shutil
from uuid import uuid4
from fastapi import FastAPI, UploadFile, File, APIRouter, Form, Request, BackgroundTasks, HTTPException
from typing import List
from schemas import UploadVideo, GetVideo, Message, GetListVideo
# from starlette.responses import JSONResponse
from models import Video, User
from services import save_video
from starlette.responses import StreamingResponse

video_router = APIRouter()

@video_router.post('/')
async def create_video(
    background_tasks: BackgroundTasks,
    title: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),
):
    user = await User.objects.first()
    print(user)
    return await save_video(user, file, title, description, background_tasks)



# @video_router.post('/video_post')
# async def create_video(video: Video):
#     await video.save()
#     return video


@video_router.post('/user_create')
async def create_user(user: User):
    await user.save()
    return user



@video_router.get('/video/{video_pk}', responses={404: {'model': Message}})
async def get_video(video_pk: int):
    file = await Video.objects.select_related('user').get(pk=video_pk)
    file_like = open(file.dict().get('file'), mode='rb')
    return StreamingResponse(file_like, media_type='video/mp4')


@video_router.get('/user/{user_pk}', response_model=List[GetListVideo])
async def get_user(user_pk: int):
    video_list = await Video.objects.filter(user=user_pk).all()
    return video_list