# Willmojis

Have you felt that your default emojis are just a little bland? That you just
wanted to replace them with pictures of you (or your friend's) faces?

Well, want no more! Willmojis (named after our lovely friend Will, of course)
are designed to automatically generate a downloadable TTF emoji font from a
small album of photos. Our website will take a zip file containing photos,
run them through Azure's Face API to help identify the most appropriate
emoji, and then crop the images to the perfect size.

## Running

Since this was made at a hackathon, it probably won't work for you (or even
us again) :(

Anyway, these are some instructions that *might* help you get it installed.

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
