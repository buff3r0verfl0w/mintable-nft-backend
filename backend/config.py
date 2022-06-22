from dataclasses import dataclass
from contracts.base import UserInfo, ContractInfo


@dataclass(frozen=True)
class Config:
    user_info: UserInfo
    contract_info: ContractInfo
    infura_key: str
