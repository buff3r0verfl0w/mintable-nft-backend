from os import urandom
from typing import List
from yaml import safe_load
from marshmallow_dataclass import class_schema

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from contracts.mintable_nft import MintableNFTContract

from .models import Token_Pydantic, TokenIn_Pydantic, Tokens
from .config import Config

with open("config.yml") as file:
    yaml = safe_load(file.read())

    ConfigSchema = class_schema(Config)
    config: Config = ConfigSchema().load(yaml)

app = FastAPI()

contract = MintableNFTContract(config.contract_info, config.infura_key)


@app.post("/tokens/create", response_model=Token_Pydantic)
async def create_token(token: TokenIn_Pydantic):
    unique_hash = urandom(10).hex()
    tx_hash = contract.mint(config.user_info, token.owner, unique_hash, token.media_url)

    token_obj = await Tokens.create(
        unique_hash=unique_hash,
        tx_hash=tx_hash,
        media_url=token.media_url,
        owner=token.owner
    )

    return await Token_Pydantic.from_tortoise_orm(token_obj)


# TODO: pagination (see https://github.com/uriyyo/fastapi-pagination/blob/main/examples/pagination_tortoise.py)
@app.get("/tokens/list", response_model=List[Token_Pydantic])
async def get_tokens():
    return await Token_Pydantic.from_queryset(Tokens.all())


@app.get("/tokens/total_supply", response_model=int)
def total_supply():
    return contract.total_supply()


register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={"models": ["backend.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
