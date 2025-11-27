# Configuration

You can configure what and how this script will scrape by editing the
[`config.py`](./config.py) file. The variables are well documented.

# Running it

As always, just install the requirements and run `main.py`. 

On the first run
```sh
chmod +x ./main.py
python -m venv ./venv
source ./venv/bin/activate
python -m pip install -r ./requirements.txt
./main.py
```

On subsequent runs
```sh
source ./venv/bin/activate
./main.py
```
