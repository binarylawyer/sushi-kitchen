from fastapi import FastAPI
from .chain import chain
from langserve import add_routes

app = FastAPI()
add_routes(app, chain, path="/chain")
