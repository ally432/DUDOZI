from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Literal
from firestore.client import get_db

app = FastAPI(title="AGV Observation API")  # 서버 생성

YoloLabel = Literal["normal", "abnormal", "unknown"]

class YoloIn(BaseModel):
    result: YoloLabel
    confidence: float = Field(ge=0.0, le=1.0)

class ObservationIn(BaseModel):
    node: str
    image_url: str
    yolo: YoloIn

class UploadObservationRequest(BaseModel):  # JSON 형식 검사 
    cycle_id: str
    agation: str
    timestamp: str        
    observations: List[ObservationIn]

@app.post("/agv/upload_observation")    # JSON 보내기
def upload_observation(req: UploadObservationRequest):
    try:
        db = get_db()

        agv_id = req.agation

        agv_doc = {
            "cycle_id": req.cycle_id,
            "agation": agv_id,
            "timestamp": req.timestamp,         
            "observations": [o.model_dump() for o in req.observations],
        }

        db.collection("cycles").document(agv_id).set(   # cycles/{agation}/agv 저장
            {"agv": agv_doc},
            merge=True
        )

        return {"status": "ok"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))