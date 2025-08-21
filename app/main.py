from fastapi import FastAPI
from app.manager import Manager
from multiprocessing import Value


app = FastAPI()


@app.get("/")
def read_root():
    flag = Value('b', True) # creating a flag for error handling
    manager = Manager(flag) ##passing the flag
    if not flag.value:
        return {"error": "error in loading mongo"}
    manager.process()
    data = manager.get_data()
    return {"data": data}




