# Willmojis

## Running

Follow the installation instructions in `font/README.md`, then run:

    $ pip install -r requirements.txt
    $ FLASK_APP=server flask run

Ensure that the following environment variables are present and filled with
appropriate values:

- AZURE_FACE_KEY
- AZURE_FACE_ENDPOINT
- AZURE_BING_KEY
- AZURE_BING_ENDPOINT

You can create a `.credentials` file that you can then source:

```bash
export AZURE_FACE_KEY=...
export AZURE_FACE_ENDPOINT=...

export AZURE_BING_KEY=...
export AZURE_BING_ENDPOINT=...
```

## Contributors

- [Daniel Spencer](https://github.com/danielfspencer)
- [Justin Chadwell](https://github.com/jedevc)
- [Aryaman Reddi](https://github.com/AryamanReddi99)
- [Will Russell](https://github.com/wrussell1999)
