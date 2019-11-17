from PIL import Image, ImageOps

def resize(file):
    im = Image.open(file)
    SIZE = 128, 128
    im = ImageOps.fit(im, SIZE, method=Image.ANTIALIAS)
    im.save(file)
