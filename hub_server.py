import httpx
from fastapi import FastAPI
from pydantic import BaseModel

from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# API TEST
### 비동기 통신 테스트
### 결과 : 체감이 될 정도로 빠르다.
@app.get("/")
async def root():
    async with httpx.AsyncClient() as client:
        r = await client.get("http://localhost:8000/test")
        return r.json()

@app.get("/test")
def test():
    return {"message": "I'm test"}



# Request 정의
class Ksl_translater_req(BaseModel):
    text: str

class Ner_req(BaseModel):
    text: str

class Tts_req(BaseModel):
    text: str

# 확인을 위한 함수
def print(api_name,req,res):
    print(api_name)
    print('req : '+req.json())
    print('res' + res.json())

## KSL Translater API
#### 구어 -> 수어 문법 번환
@app.get("/ksl/translater/into")
async def ksl_translater_into(req: Ksl_translater_req):
    async with httpx.AsyncClient() as client:
        res = await client.get(os.environ['KSL_TRANSLATER_API_URL'])
        print('ksl_translater_into',req, res)
        return res.json()

#### 수어 -> 구어 문법 변환
@app.get("/ksl/translater/from")
async def ksl_translater_from(req: Ksl_translater_req):
    async with httpx.AsyncClient() as client:
        res = await client.get(os.environ['KSL_TRANSLATER_API_URL'])
        print('ksl_translater_into',req, res)
        return res.json()

#### 수어 애니메이션 맵핑
@app.get("ksl/animation")
async def ksl_animation(req: Ksl_translater_req):
    async with httpx.AsyncClient() as client:
        res = await client.get(os.environ['KSL_TRANSLATER_API_URL'])
        print('ksl_translater_into',req, res)
        return res.json()


## NER Tagging API
#### 객체명 인식 후 태깅
@app.get("/ner/tagging")
async def ner_tagging(req: Ner_req):
    async with httpx.AsyncClient() as client:
        res = await client.get(os.environ['NER_TAGGING_API_URL'])

        return res.json()


## TTS API
#### 텍스트 -> 음성 변환 후 S3 업로드 주소 반환
@app.get("/tts")
async def tts(req : Tts_req):
    async with httpx.AsyncClient() as client:
        res = await client.get(os.environ['TTS_API_URL'])

        return res.json()