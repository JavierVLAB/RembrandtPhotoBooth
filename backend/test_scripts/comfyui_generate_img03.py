import json
from urllib import request
import os

#This is the ComfyUI api prompt format.

#If you want it for a specific workflow you can "enable dev mode options"
#in the settings of the UI (gear beside the "Queue Size: ") this will enable
#a button on the UI to save workflows in api format.

#keep in mind ComfyUI is pre alpha software so this format will change a bit.

#this is the one for the default workflow


def queue_prompt(image_name= "test01"):

    with open("rembrant_workflowTest.json", "r") as workflow_file:
        prompt = json.loads(workflow_file.read())

    prompt["9"]["inputs"]["image"] = image_name + '.jpg'
    prompt["37"]["inputs"]["filename_prefix"] = image_name + '1out'
    
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req =  request.Request("http://127.0.0.1:8188/prompt", data=data)
    #request.urlopen(req)
    with request.urlopen(req) as response:
        response_content = response.read()
        print(response_content)



if __name__ == "__main__":

    queue_prompt()
