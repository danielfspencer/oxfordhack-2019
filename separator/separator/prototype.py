from torchvision import models
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib
import torch
import numpy as np
import cv2

# Apply the transformations needed
import torchvision.transforms as T

def init():
    global dlab
    print("loading dnn...")
    dlab = models.segmentation.deeplabv3_resnet101(pretrained=1).eval()

# Define the helper function
def decode_segmap(image, source, nc=21):

  label_colors = np.array([(0, 0, 0),  # 0=background
               # 1=aeroplane, 2=bicycle, 3=bird, 4=boat, 5=bottle
               (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128),
               # 6=bus, 7=car, 8=cat, 9=chair, 10=cow
               (0, 128, 128), (128, 128, 128), (64, 0, 0), (192, 0, 0), (64, 128, 0),
               # 11=dining table, 12=dog, 13=horse, 14=motorbike, 15=person
               (192, 128, 0), (64, 0, 128), (192, 0, 128), (64, 128, 128), (192, 128, 128),
               # 16=potted plant, 17=sheep, 18=sofa, 19=train, 20=tv/monitor
               (0, 64, 0), (128, 64, 0), (0, 192, 0), (128, 192, 0), (0, 64, 128)])

  r = np.zeros_like(image).astype(np.uint8)

  for l in range(0, nc):
    idx = image == l
    r[idx] = label_colors[l, 0]

  classification = np.stack([r], axis=2)

  # Load the foreground input image
  foreground = cv2.imread(source)

  # Change the color of foreground image to RGB
  # and resize image to match shape of R-band in RGB output map
  foreground = cv2.cvtColor(foreground, cv2.COLOR_BGR2RGBA)
  foreground = cv2.resize(foreground,(r.shape[1],r.shape[0]))

  # Convert uint8 to float
  foreground = foreground.astype(float)

  # Create a binary mask of the RGB output map using the threshold value 0
  th, alpha = cv2.threshold(np.array(classification),0,255, cv2.THRESH_BINARY)

  # Apply a slight blur to the mask to soften edges
  alpha = cv2.GaussianBlur(alpha, (7,7),0)

  foreground[:,:,3] = alpha

  # Return a normalized output image for display
  return foreground/255

def segment(net, inpath, outpath, dev='cpu'):
  img = Image.open(inpath)
  # Comment the Resize and CenterCrop for better inference results
  trf = T.Compose([T.Resize(450),
                   #T.CenterCrop(224),
                   T.ToTensor(),
                   T.Normalize(mean = [0.485, 0.456, 0.406],
                               std = [0.229, 0.224, 0.225])])
  inp = trf(img).unsqueeze(0).to(dev)
  out = net.to(dev)(inp)['out']
  om = torch.argmax(out.squeeze(), dim=0).detach().cpu().numpy()

  rgb = decode_segmap(om, inpath)

  matplotlib.image.imsave(outpath, rgb)

def seperate(inpath, outpath):
    print(f"seperate image '{inpath}'...")
    segment(dlab, inpath, outpath)
