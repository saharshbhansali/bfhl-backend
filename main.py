from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import re

app = FastAPI()


class DataInput(BaseModel):
    data: List[str]


class DataResponse(BaseModel):
    is_success: bool
    user_id: str
    email: str
    roll_number: str
    numbers: List[str]
    alphabets: List[str]
    highest_lowercase_alphabet: List[str]


@app.post("/bfhl")
async def process_data(input_data: DataInput):
    try:
        numbers = [item for item in input_data.data if item.isdigit()]
        alphabets = [item for item in input_data.data if item.isalpha()]

        lowercase_alphabets = [char for char in alphabets if char.islower()]
        highest_lowercase = max(lowercase_alphabets) if lowercase_alphabets else None

        return DataResponse(
            is_success=True,
            user_id="saharsh_bhansali_15032003",
            email="saharsh.bhansali2021@vitstudent.ac.in",
            roll_number="21BCI0028",
            numbers=numbers,
            alphabets=alphabets,
            highest_lowercase_alphabet=[highest_lowercase] if highest_lowercase else [],
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/bfhl")
async def get_operation_code():
    return {"operation_code": 1}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
