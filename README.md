# mintable-nft-backend

Test task for backend developer at Rock'n'Block

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

```bash
# production
uvicorn backend.main:app
# development
uvicorn backend.main:app --reload
```

### Exiting from project env

```bash
deactivate
```
