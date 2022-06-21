from dataclasses import dataclass


@dataclass(frozen=True)
class UserInfo:
    address: str
    private_key: str


@dataclass(frozen=True)
class ContractInfo:
    network_name: str
    chain_id: int
    address: str
    abi: str
