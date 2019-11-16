import asyncio, io, glob, os, sys, time, uuid, requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType

# Set the FACE_SUBSCRIPTION_KEY environment variable with your key as the value.
# This key will serve all examples in this document.
KEY = os.environ['COGNITIVE_SERVICE_KEY']

# Set the FACE_ENDPOINT environment variable with the endpoint from your Face service in Azure.
# This endpoint will be used in all examples in this quickstart.
ENDPOINT = os.environ['FACE_ENDPOINT']

# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

print('Client Loaded')

#%%

# def functions

def face_data(url):
    detected_faces = face_client.face.detect_with_url(url=url)
    return(detected_faces)
    
def target_face(url):
    detected_faces = face_data(url)
    if len(detected_faces)>1:
        raise Exception('Only input 1 face')
    if len(detected_faces) == 0:
        raise Exception('No faces detected')
    target_face = face_data(url)[0]
    return(target_face)
    
def locate(sample_url, compare_url):
    sample = target_face(sample_url)
    compare = face_data(compare_url)
    sample_id = sample.face_id
    compare_ids = list(map(lambda x: x.face_id, compare))
    # list of similar faces
    similar_faces = face_client.face.find_similar(face_id=sample_id, face_ids=compare_ids)
    similar_face = similar_faces[0]
    for face in compare:
        if face.face_id == similar_face.face_id:
            located_face = face
    return(located_face)

def get_rectangle(face, scale):
    rect = face.face_rectangle
    print(rect)
    left = rect.left
    top = rect.top
    right = left + rect.height
    bottom = top + rect.width
    # expand margins
    height = rect.height
    width = rect.width
    ox = left + 0.5*height
    oy = top + 0.5*width
    expleft = ox - (height/2)*scale
    exptop = oy - (width/2)*scale
    expright = ox + (height/2)*scale
    expbottom = oy + (width/2)*scale
    return (expleft, exptop, expright, expbottom)

def draw_rectangle(face, img_url, scale=1.5):
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    rect_coords = get_rectangle(face, scale)
    img_crop = img.crop(rect_coords)
    img_crop.show()
    #draw = ImageDraw.Draw(img)
    #draw.rectangle(get_rectangle(face, scale), outline='red')
    #img.show()

#%%
sample_url  = 'https://upload.wikimedia.org/wikipedia/commons/5/56/Donald_Trump_official_portrait.jpg'
compare_url = 'https://www.dw.com/image/50172356_303.jpg'
located_face = locate(sample_url,compare_url)
draw_rectangle(located_face,compare_url, 2)








