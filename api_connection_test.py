import httpx
from fastapi import FastAPI
from pydantic import BaseModel

import json

from dotenv import load_dotenv
import os
load_dotenv()

app_to_test = FastAPI()



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


### KSL TRANSLATER TEST
@app_to_test.post("/ksl_translater/to",response_model=KSL_translater_to_res)
async def ksl_translater_to_test(req: KSL_translater_to_req):
    return {
        'ksl_animation_array': ["1","2","3"]
    }

### KSL TRANSLATER TEST
@app_to_test.post("/ksl_translater/from",response_model=KSL_translater_from_res)
async def ksl_translater_from_test(req: KSL_translater_from_req):
    return {
        'translated_sentence': "test___translated_sentence"
    }


# API TEST
### NER TEST
@app_to_test.post("/ner",response_model=NER_res)
async def ner_test(req: NER_req):
    return {
        'request_text': req.sentence,
        'NER_result': "test___NER_result",
        'NER_tag': {
            "지명":["서울"],
            "인명":["홍길동"],
            "기관명":["선문대학교"]
        }
    }



### TTS TEST
@app_to_test.post("/tts",response_model=TTS_res)
async def tts_test(req: TTS_req):
    return {
        "speaking_audio": "test___speaking_audio"
    }

