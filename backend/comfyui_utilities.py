import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
from urllib import request, parse
import asyncio

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())

def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req =  request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(request.urlopen(req).read())

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = parse.urlencode(data)
    with request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()

def get_history(prompt_id):
    with request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())

async def get_images(wsnextjs, image_name = "test01"):
    
    with open("darkroom_v04.json", "r") as workflow_file:
        prompt = json.loads(workflow_file.read())

    prompt["20"]["inputs"]["image"] = image_name + '.jpg'
    prompt["26"]["inputs"]["image"] = image_name + '.jpg'
    prompt["28"]["inputs"]["image"] = image_name + '.jpg'

    prompt["53"]["inputs"]["filename_prefix"] = image_name + 'out'
    
    prompt["3"]["inputs"]["seed"] = 0

    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))

    prompt_id = queue_prompt(prompt)['prompt_id']
    output_images = {}
    
    while True:
        out = ws.recv()

        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break #Execution is done
            elif message['type'] == 'progress':
                progress = str(message['data']['value']/message['data']['max'])
                #print(progress)
                await wsnextjs.send_text('text_message:progress:'+progress)
                await asyncio.sleep(0.01)
                #print(str(message['data']['value']) + '/' + str(message['data']['max']))


        else:
            continue #previews are binary data

    history = get_history(prompt_id)[prompt_id]
    for o in history['outputs']:
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_data = get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
            output_images[node_id] = images_output

    return output_images["53"][0]

async def generate_image(wsnextjs, image_name = "test01"):
    
    with open("darkroom_v04.json", "r") as workflow_file:
        prompt = json.loads(workflow_file.read())

    prompt["20"]["inputs"]["image"] = image_name + '.jpg'
    prompt["26"]["inputs"]["image"] = image_name + '.jpg'
    prompt["28"]["inputs"]["image"] = image_name + '.jpg'

    prompt["53"]["inputs"]["filename_prefix"] = image_name + 'out'
    
    prompt["3"]["inputs"]["seed"] = 0

    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))

    prompt_id = queue_prompt(prompt)['prompt_id']
    output_images = {}
    
    while True:
        out = ws.recv()

        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break #Execution is done
            elif message['type'] == 'progress':
                progress = str(message['data']['value']/message['data']['max'])
                #print(progress)
                await wsnextjs.send_text('text_message:progress:'+progress)
                await asyncio.sleep(0.01)
                #print(str(message['data']['value']) + '/' + str(message['data']['max']))


        else:
            continue #previews are binary data


if __name__ == "__main__":
    print(client_id)
    images = generate_image("img20240515185952")
    
    for node_id in images:
        for image_data in images[node_id]:
            from PIL import Image
            import io
            image = Image.open(io.BytesIO(image_data))
            image.show()
            print(node_id)
