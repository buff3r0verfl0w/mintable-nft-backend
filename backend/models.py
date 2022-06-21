from pydantic import BaseModel, Field

from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Tokens(models.Model):
    id = fields.IntField(pk=True)

    unique_hash = fields.CharField(max_length=20, unique=True)  # max len 20 from spec
    tx_hash = fields.CharField(max_length=66)  # max len of ETH tx hash
    media_url = fields.CharField(max_length=2048)  # taken from RFC 2616 (Hypertext Transfer Protocol HTTP/1.1)
    owner = fields.CharField(max_length=42)  # max len of ETH address


Token_Pydantic = pydantic_model_creator(Tokens, name="Token")


# looks like we don't  need it
# TokenIn_Pydantic = pydantic_model_creator(Tokens, name="TokensIn", exclude_readonly=True)

class TokenIn_Pydantic(BaseModel):
    media_url: str = Field(..., max_length=2024)
    owner: str = Field(..., max_length=42)
