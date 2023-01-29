from django.shortcuts import render
from django.http import HttpResponse
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
from .forms import ImageForm
import json
import os
import sys
import requests
import time
# If you are using a Jupyter Notebook, uncomment the following line.
# %matplotlib inline
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image
from io import BytesIO

def index(request):
    return render(request, 'portfolio/index.html')

def image_to_text(request):
    '''
    Authenticate
    Authenticates your credentials and creates a client.
    '''
    subscription_key = "a918e6b93bf44deeaa117fac9ad76074"
    endpoint = "https://nbhushancvdemo.cognitiveservices.azure.com/"

    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    '''
    END - Authenticate
    '''

    text_recognition_url = endpoint + "/vision/v3.1/read/analyze"

    # Set image_url to the URL of an image that you want to recognize.
    #image_url = "https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/master/articles/cognitive-services/Computer-vision/Images/readsample.jpg"

    headers = {'Ocp-Apim-Subscription-Key': subscription_key,'Content-Type': 'application/octet-stream'}
    # with open('image_to_text.png', 'rb') as f:
    #     data = f.read()
    data = request.FILES["oi_image"].read()
    response = requests.post(
    text_recognition_url, headers=headers, data=data)
    response.raise_for_status()

    # Extracting text requires two API calls: One call to submit the
    # image for processing, the other to retrieve the text found in the image.

    # Holds the URI used to retrieve the recognized text.
    operation_url = response.headers["Operation-Location"]

    # The recognized text isn't immediately available, so poll to wait for completion.
    analysis = {}
    poll = True
    while (poll):
        response_final = requests.get(
            response.headers["Operation-Location"], headers=headers)
        analysis = response_final.json()
        
        print(json.dumps(analysis, indent=4))

        time.sleep(1)
        if ("analyzeResult" in analysis):
            poll = False
        if ("status" in analysis and analysis['status'] == 'failed'):
            poll = False

    polygons = []
    if ("analyzeResult" in analysis):
        # Extract the recognized text, with bounding boxes.
        polygons = [(line["boundingBox"], line["text"])
                    for line in analysis["analyzeResult"]["readResults"][0]["lines"]]

    # Display the image and overlay it with the extracted text.
    image = Image.open(request.FILES["oi_image"])
    ax = plt.imshow(image)
    for polygon in polygons:
        vertices = [(polygon[0][i], polygon[0][i+1])
                    for i in range(0, len(polygon[0]), 2)]
        text = polygon[1]
        patch = Polygon(vertices, closed=True, fill=False, linewidth=2, color='y')
        ax.axes.add_patch(patch)
        plt.text(vertices[0][0], vertices[0][1], text, fontsize=20, va="top")
    plt.show()
    return render(request, "portfolio/index.html")