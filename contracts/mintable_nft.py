from .base import *

from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware


class MintableNFTContract:
    def __init__(self, contract_info: ContractInfo, infura_key: str):
        self.contract_info = contract_info

        self.w3 = Web3(HTTPProvider(f"https://{contract_info.network_name.lower()}.infura.io/v3/{infura_key}"))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        with open(contract_info.abi_path) as file:
            abi = file.read()

        self.contract = self.w3.eth.contract(address=contract_info.address, abi=abi)

    def total_supply(self) -> int:
        return self.contract.functions.totalSupply().call()

    def mint(self, user: UserInfo, owner: str, unique_hash: str, media_url: str) -> str:
        nonce = self.w3.eth.get_transaction_count(user.address)
        tx = self.contract.functions.mint(owner, unique_hash, media_url).buildTransaction({
            "chainId": self.contract_info.chain_id,
            "nonce": nonce,
        })
        signed_tx = self.w3.eth.account.sign_transaction(tx, user.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_hash.hex()
