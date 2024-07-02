from fastapi import FastAPI
from pydantic import BaseModel
from retriver import retrieve_and_answer,search

app = FastAPI()

class Query(BaseModel):
    query: str

@app.post("/answer")
async def answer_query(query: Query):
    results,list_res, responseModel = retrieve_and_answer(query.query)
    return {"answer": results,"context":list_res, "respostaLLM":responseModel}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

