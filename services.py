import shutil
from uuid import uuid4
import aiofiles
from fastapi import UploadFile, BackgroundTasks
from schemas import UploadVideo
from models import Video



async def save_video(
        user: int,
        file: UploadFile,
        title: str,
        description: str,
        background_tasks: BackgroundTasks
):
    file_name = f'media/{user}_{uuid4()}.mp4'
    if file.content_type == 'video/mp4':
        background_tasks.add_task(write_video, file_name, file)
    else:
        raise HTTPException(status_code=418, detail='It is not mp4 file')
    info = UploadVideo(title=title, description=description)
    return await Video.objects.create(file=file.filename, user=user, **info.dict())



def write_video(file_name: str, file: UploadFile):
    # async with aiofiles.open(file_name, 'wb') as buffer:
    #     data = await file.read()
    #     await buffer.write(data)
    with open(file_name, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)