Command line packages
- `pngquant`

Requires Python 3.6 or above.
```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r compose/nototools/requirements.txt
pip3 install compose/nototools/
```

To test:
```bash
cd tester
./test.sh
```
Then open 'test.html' in Chrome.
