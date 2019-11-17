from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.search.imagesearch import ImageSearchAPI

from .utils import settings

FACE_KEY = settings("azure", "face", "key")
FACE_ENDPOINT = settings("azure", "face", "endpoint")

BING_KEY = settings("azure", "bing", "key")
BING_ENDPOINT = settings("azure", "bing", "endpoint")

face_client = FaceClient(FACE_ENDPOINT, CognitiveServicesCredentials(FACE_KEY))
bing_client = ImageSearchAPI(
    CognitiveServicesCredentials(BING_KEY), base_url=BING_ENDPOINT
)
