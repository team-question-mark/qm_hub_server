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



# Function

### 데이터 모델 정의
class Ksl_translater_into_req(BaseModel):
    text: str

class Ksl_translater_from_req(BaseModel):
    text: str

class Ksl_animation_req(BaseModel):
    text: str

class Ner_req(BaseModel):
    text: str

class Tts_req(BaseModel):
    text: str


### 확인을 위한 함수
def print_to_check(api_name,req,res):
    print(api_name, "\nreqest : ", req, "response : ", res, sep="\n")

### KSL Translater API
#### 구어 -> 수어 문법 번환 및 애니메이션 맵핑
async def ksl_translater_into(req: Ksl_translater_into_req):
    async with httpx.AsyncClient() as client:
        res = await client.get(os.environ['KSL_TRANSLATER_API_URL'])
        print_to_check('ksl_translater_into', req, res)
        return res

#### 수어 -> 구어 문법 변환
async def ksl_translater_from(req: Ksl_translater_from_req):
    async with httpx.AsyncClient() as client:
        res = await client.get(os.environ['KSL_TRANSLATER_API_URL'])
        print_to_check('ksl_translater_from', req, res)
        return res


### NER Tagging API
#### 객체명 인식 후 태깅
async def ner_tagging(req: Ner_req):
    async with httpx.AsyncClient() as client:
        res = await client.get(os.environ['NER_TAGGING_API_URL'])
        print_to_check('ner_tagging', req, res)
        return res


### TTS API
#### 텍스트 -> 음성 변환 후 S3 업로드 주소 반환
async def tts(req : Tts_req):
    async with httpx.AsyncClient() as client:
        res = await client.get(os.environ['TTS_API_URL'])
        print_to_check('tts', req, res)
        return res






# API Endpoint

### 데이터 모델 정의
class KSL_To(BaseModel):
    text: str

class KSL_From(BaseModel):
    text: str


### Endpoint
#### 구어 -> 수어
@app.get('/server/ksl/to')
# def to_ksl(req: KSL_To):
async def to_ksl():
    req = ''
    # NER 태깅
    after_ner = await ner_tagging(req)
    # KSL 문법 변환 및 애니메이션 맵핑
    after_ksl = await ksl_translater_into(after_ner)
    res = after_ksl
    return res.json()

#### 수어 -> 구어
@app.get('/server/ksl/from')
# def from_ksl(req: KSL_From):
async def from_ksl():
    req= ''
    # 구어 문법 변환
    after_ksl = await ksl_translater_from(req)
    # TTS
    after_tts = await tts(after_ksl)
    res = after_tts
    return res.json()