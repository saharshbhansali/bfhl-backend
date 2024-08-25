from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ValidationError
from typing import List, Union
import json

app = FastAPI(
    title="21BCI0028", description="My Task for Bajaj Finserv", version="1.0.1"
)


class DataInput(BaseModel):
    data: List[str]


class SuccessResponse(BaseModel):
    is_success: bool
    user_id: str
    email: str
    roll_number: str
    numbers: List[str]
    alphabets: List[str]
    highest_lowercase_alphabet: List[str]


class ErrorResponse(BaseModel):
    is_success: bool
    error: str


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422, content={"is_success": False, "error": str(exc)}
    )


@app.post("/bfhl", response_model=Union[SuccessResponse, ErrorResponse])
async def process_data(input_data: DataInput):
    try:
        numbers = [item for item in input_data.data if item.isdigit()]
        alphabets = [item for item in input_data.data if item.isalpha()]

        lowercase_alphabets = [char for char in alphabets if char.islower()]
        highest_lowercase = max(lowercase_alphabets) if lowercase_alphabets else None

        return SuccessResponse(
            is_success=True,
            user_id="saharsh_bhansali_15032003",
            email="saharsh.bhansali2021@vitstudent.ac.in",
            roll_number="21BCI0028",
            numbers=numbers,
            alphabets=alphabets,
            highest_lowercase_alphabet=[highest_lowercase] if highest_lowercase else [],
        )
    except Exception as e:
        return JSONResponse(
            status_code=400, content={"is_success": False, "error": str(e)}
        )


@app.get("/bfhl")
async def get_operation_code():
    return {"operation_code": 1}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
