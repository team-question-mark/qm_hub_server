import httpx
from fastapi import FastAPI
from pydantic import BaseModel


import json

from dotenv import load_dotenv
import os
load_dotenv()

app = FastAPI()

class Test(BaseModel):
    text: str = None
    tt : str = None
# API TEST
### 비동기 통신 테스트
### 결과 : 체감이 될 정도로 빠르다.
@app.post("/")
async def root(req: dict):
    print(req)
    async with httpx.AsyncClient() as client:
        r = await client.post(os.environ['TEST_URL'], data=json.dumps(req))
        return r.json()


@app.post("/hi")
def hi(test: Test):
    print(type(test))
    return test.dict()

@app.post("/test")
def test(req: Test):
    print(req)
    return {"message": "I'm test"}



# Function


class KSL_translater_to_req(BaseModel):
    sentence: str

class KSL_translater_to_res(BaseModel):
    ksl_animation_array: list


class KSL_translater_from_req(BaseModel):
    word_arr: list

class KSL_translater_from_res(BaseModel):
    translated_sentence: str


class NER_req(BaseModel):
    sentence: str

class NER_res(BaseModel):
    request_text: str
    NER_result: str
    NER_tag: dict


class TTS_req(BaseModel):
    sentence: str

class TTS_res(BaseModel):
    speaking_audio: str



### 확인을 위한 함수
def print_to_check(api_name,req,res):
    print(api_name, "\nreqest : ", req, "response : ", res.json(), sep="\n")

### KSL Translater API
#### 구어 -> 수어 문법 번환 및 애니메이션 맵핑
async def ksl_translater_to(req: KSL_translater_to_req):
    async with httpx.AsyncClient() as client:
        res = await client.post(os.environ['KSL_TRANSLATER_TO_API_URL'],data=json.dumps(req))
        print_to_check('ksl_translater_into', req, res)
        return res.json()

#### 수어 -> 구어 문법 변환
async def ksl_translater_from(req: KSL_translater_from_req):
    async with httpx.AsyncClient() as client:
        res = await client.post(os.environ['KSL_TRANSLATER_FROM_API_URL'],data=json.dumps(req))
        print_to_check('ksl_translater_from', req, res)
        return res.json()


### NER Tagging API
#### 객체명 인식 후 태깅
async def ner_tagging(req: NER_req):
    async with httpx.AsyncClient() as client:
        print(req)
        res = await client.post(os.environ['NER_TAGGING_API_URL'],data=json.dumps(req))
        print_to_check('ner_tagging', req, res)
        return res.json()


### TTS API
#### 텍스트 -> 음성 변환 후 S3 업로드 주소 반환
async def tts(req : TTS_req):
    async with httpx.AsyncClient() as client:
        res = await client.post(os.environ['TTS_API_URL'],data=json.dumps(req))
        print_to_check('tts', req, res)
        return res.json()







# API Endpoint

### 데이터 모델 정의
class KSL_To(BaseModel):
    stt_recog_sentence: str

class KSL_TO_RES(BaseModel):
    ner_tagging: dict
    ksl_animation_array: list

class KSL_From(BaseModel):
    ksl_recog_word_arr: list

class KSL_From_RES(BaseModel):
    speaking_audio: str

### Endpoint
#### 구어 -> 수어
@app.post('/server/ksl/to',response_model=KSL_TO_RES)
# def to_ksl(req: KSL_To):
async def to_ksl(req: KSL_To):

    ner_req = {
        'sentence' : req.stt_recog_sentence,
    }
    # NER 태깅
    after_ner = await ner_tagging(ner_req)


    ksl_translater_into_req = {
        'sentence' : after_ner['NER_result'],
    }
    # KSL 문법 변환 및 애니메이션 맵핑
    after_ksl = await ksl_translater_to(ksl_translater_into_req)


    res = {
        "ner_tagging" : after_ner['NER_tag'],
        "ksl_animation_array" : after_ksl['ksl_animation_array'],
    }
    return res

#### 수어 -> 구어
@app.post('/server/ksl/from' ,response_model=KSL_From_RES)
# def from_ksl(req: KSL_From):
async def from_ksl(req: KSL_From):


    ksl_translater_from_req = {
        'word_arr': req.ksl_recog_word_arr,
    }
    # 구어 문법 변환
    after_ksl = await ksl_translater_from(ksl_translater_from_req)


    tts_req = {
        'sentence': after_ksl['translated_sentence'],
    }
    # TTS
    after_tts = await tts(tts_req)


    res = {
        "speaking_audio" : after_tts['speaking_audio'],
    }
    return res