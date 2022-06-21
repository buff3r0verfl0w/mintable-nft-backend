from os import urandom
from typing import List

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from contracts.base import UserInfo, ContractInfo
from contracts.mintable_nft import MintableNFTContract

from .models import Token_Pydantic, TokenIn_Pydantic, Tokens

app = FastAPI()

# TODO: envs/configs
user_info = UserInfo(
    "0x7B17559C240aE7793B658B703da74Ce512cF955b",
    "ff00436583fcaaa0ccc6d1015356a92b0f5210e3c5b204b7507cce1a3e8f0352",
)

with open("resources/abi.json") as file:
    abi = file.read()

contract_info = ContractInfo("Rinkeby", 4, "0x92e098deF0CA9577BD50ca61B90b9A46EC1F2040", abi)
contract = MintableNFTContract(contract_info, "2033296f17d9420d8109f6e61312d96d")


@app.post("/tokens/create", response_model=Token_Pydantic)
async def create_token(token: TokenIn_Pydantic):
    unique_hash = urandom(10).hex()
    tx_hash = contract.mint(user_info, token.owner, unique_hash, token.media_url)

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
