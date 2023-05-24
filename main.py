from fastapi import Response, status
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from controller import inference

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=['GET', 'POST'],
    allow_headers=["*"],
)


@app.post("/predict/", status_code=200)
async def predict(fileUpload: UploadFile, response: Response):
    res, responseBody = inference(file=fileUpload)
    if res:
        return responseBody
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'message': 'ERROR'}


@app.get("/")
async def root():
    return {"message": "Hello I'm Beefy AI"}
