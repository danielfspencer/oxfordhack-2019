#### Required command line packages
- `pngquant`
- `make`

#### Requires Python 3.6 or above
```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r compose/nototools/requirements.txt
pip3 install compose/nototools/
```

#### To test
```bash
python3 test.py
```
Then open `tester/test.html` in Chrome.

#### API usage
See `test.py`
