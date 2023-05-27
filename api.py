from fastapi import FastAPI

import uvicorn

app = FastAPI()



@app.get("/")
async def read_root():
    return {"Hello": "raspberry"}

@app.get("/sensors")
async def sensors_value():

    return {
        "temperature_eau" : 20,
        "niveau_eau" : 50,
        "niveau_lait" : 67
    }


uvicorn.run(app, host="0.0.0.0", port=8080)
