# mintable-nft-backend

Test task for backend developer at Rock'n'Block

### Technology stack
- [ethereum/web3.py](https://github.com/ethereum/web3.py) - interacts with smart contract
- [tiangolo/fastapi](https://github.com/tiangolo/fastapi) - used to build API
- [tortoise/tortoise-orm](https://github.com/tortoise/tortoise-orm) - used to connect SQLite3 database

### Installing

```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configuration

```bash
# now you can change config.yml with actual values
cp config.example.yml config.yml
```

### Launching

#### Local

```bash
# production
uvicorn backend.main:app
# development
uvicorn backend.main:app --reload
```

##### Exiting from project env

```bash
deactivate
```

#### Inside docker container
```bash
git clone git@github.com:buff3r0verfl0w/mintable-nft-backend.git
cd mintable-nft-backend

cp config.example.yml config.yml

docker build -t mintable-nft-backend .
docker run --rm -itd --name backend -p 8000:8000 mintable-nft-backend
```

### Interaction with API
If you're running it in docker you can open <http://127.0.0.1:8000/docs> in your browser
