from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from typing import List, Union

app = FastAPI()


class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)
        self.is_success = False


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


@app.exception_handler(CustomHTTPException)
async def custom_exception_handler(request: Request, exc: CustomHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(is_success=False, error=exc.detail).dict(),
    )


@app.post("/bfhl", response_model=Union[SuccessResponse, ErrorResponse])
async def process_data(input_data: DataInput):
    try:
        # Validate input
        if not input_data.data:
            raise CustomHTTPException(status_code=400, detail="Input data is empty")

        # Process data
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
    except ValidationError as e:
        raise CustomHTTPException(status_code=400, detail="Invalid input data format")
    except Exception as e:
        raise CustomHTTPException(
            status_code=500, detail="An unexpected error occurred"
        )


@app.get("/bfhl")
async def get_operation_code():
    return {"operation_code": 1}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
