

## Installation

Create a virtual environment:
```
virtualenv -p python3 ~/.venv-py3
```

Each new terminal session requires you to reactivate your virtualenv

```
source ~/.venv-py3/bin/activate
```

Install from requirement file
```
pip install -r requirements.txt
```

Register Infura and create project https://infura.io/ 
```
export WEB3_INFURA_PROJECT_ID=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
export WEB3_INFURA_API_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

## Usage

Show all commands
```
python generate.py -h
```
