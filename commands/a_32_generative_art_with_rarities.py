from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageSequence
from PIL import ImageFilter
from PIL import ImageEnhance
import os
import sys
from werkzeug.utils import secure_filename
import io
import random
import requests
import json
from PIL import Image
from base64 import b16encode
import logging
import time
import random
import a_27_upload_im_ipfs
logging.basicConfig(filename='/home/yop/Downloads/cardano/error_log.txt', level=logging.DEBUG)


# This Vending Machine runs in isolation on linux
project_name = sys.argv[1]

# Storage
code = ''
addTextCode = ''
path = f'/home/yop/Downloads/cardano/vending_machine/{project_name}'
finished_result = f'/home/yop/Downloads/cardano/vending_machine/{project_name}/to_upload'

def add_paths(path):
    '''
    The expected path has folders named layer1, layer2, layer3,...
    Inside each layer folder there are .png s and .txt s
    Structure path_files like this:
    [[[img1.png, text1.txt], [img2.png, text2.txt]], [img1.png, text1.txt], ...]
    path_files ex:
    [
    [["/usr/yop/collection_name/layer1/sunny.png",] "/usr/yop/collection_name/layer1/cloudy.png"],
    ["/usr/yop/collection_name/layer2/face1.png", "/usr/yop/collection_name/layer2/face2.png"],
    ["/usr/yop/collection_name/layer3/hair1.png", "/usr/yop/collection_name/layer3/hair1.png"]
    ]
    '''
    path_files = []
    projects_name = os.listdir(f'/home/yop/Downloads/cardano/vending_machine/{project_name}')
    projects_name.sort()
    for layer in projects_name:
        if 'layer' not in str(layer):
            continue
        x = int(str(layer)[-1:]) -1
        files = projects_name = os.listdir(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/{layer}/')
        files.sort()
        for file in files:
            filename = f'/home/yop/Downloads/cardano/vending_machine/{project_name}/{layer}/{file}'
            try:
                path_files[x].append(filename)
            except:
                path_files.append([])
                path_files[x].append(filename)

    return path_files


def fetch_img_size(path_files):
    # Fetch height and width of the last image
    for obj in path_files[0]:
        temp = secure_filename(obj).lower()
        if temp.endswith('png', -3):
            obj = Image.open(obj)
            img_w, img_h = obj.size
            size = img_w, img_h
            return size

    return size

def get_description_website_artist(project_name):
    # Descrition is handeled from an external descrition.txt file in # Storage section
    path = f'/home/yop/Downloads/cardano/vending_machine/{project_name}'
    description = ' '
    try:
        with open(path + '/description.txt', 'r') as text:
            description = text.read()
            if len(description) > 64:
                description = [description[y-x:y] for y in range(x, len(description)+x, x)]
    except:
        pass  # No description, '' will be instead

    # Website is handeled from an external website.txt file in # Storage section
    website = ' '
    try:
        with open(path + '/website.txt', 'r') as text:
            website = text.read()
            website = website.replace('\n', '')
        if len(website) > 64:
            website = [website[y-x:y] for y in range(x, len(website)+x, x)]
    except:
        pass  # No website, ' ' will be instead

    # Artist is handeled from an external artist.txt file in # Storage section
    artist = ''
    try:
        with open(path + '/artist.txt', 'r') as text:
            artist = text.read()
            artist = artist.replace('\n', '')
        if len(artist) > 64:
            artist = [artist[y-x:y] for y in range(x, len(artist)+x, x)]
    except:
        print('no artist name found')
        pass  # No website, '' will be instead    

    return description, website, artist



def store(obj, size):
    # Store the pictures' object and their metadata in a list
    obj_file = []
    imageMetadataPair = []
    for x in obj:
        filename = secure_filename(x)
        if ((filename.endswith('png', -3)) or (filename.endswith('PNG', -3))):
            x = Image.open(x)

            # Make sure all pictures are egual
            originalImage = x.convert('RGBA')
            originalImage = originalImage.resize(size) 
            imageMetadataPair.append(originalImage)

        # Open the .txt file content and append it to the list of the obj_file
        if filename.endswith('txt', -3):
            with open(x, 'r') as read:
                file_data = read.readlines()
                imageMetadataPair.append(file_data)
                obj_file.append(imageMetadataPair)
                imageMetadataPair = []  # Clear the buffer

    return obj_file


def link_img_and_attr(path_files):
    '''
    path_files has all paths of each layer
    store() returns the img object and attributes of that img
    '''
    images_and_metadata = []
    size = fetch_img_size(path_files)
    for y, layer in enumerate(path_files):
        temp = store(layer, size)
        if len(temp) == 1:  # In case there is no text file
            temp.append('')

        try:
            images_and_metadata[y].append(temp)
        except:
            images_and_metadata.append([])
            images_and_metadata[y].append(temp)

    return images_and_metadata


def create_layer_structure(images_and_metadata):
    '''
    Very important, this is the core of the iteration
    Very useful for vending machine, rarities and randomly selected items
    '''
    total_layers = len(images_and_metadata)
    LAYERSTRUCTURE = []
    currentPosition = []
    total_iterations = 1
    for x in range(total_layers):
        currentPosition.append(0)
    for layer in images_and_metadata:
        for x, layer in enumerate(layer):  # Real layer

            # Inside one layer is composed of [img.png, text.txt], [img2.png, text2.txt]
            # LAYERSTRUCTURE is like: [3,5,2,1,7,8]
            LAYERSTRUCTURE.append(len(layer))
            total_iterations *= len(layer)  # Total number of NFTs

    return LAYERSTRUCTURE, total_iterations, total_layers


def addAttr(metadata):
    # Create a dictionary of the metadata
    localAttributes = {}
    for elem in metadata:
        numberElements = elem.split(':')
        if len(numberElements) < 2: continue
        trait0, trait1 = elem.split(':')
        trait1 = trait1.replace('\n', '')
        trait0 = trait0.replace('\n', '')


        # Clean the attributes
        # trait0 is the name of the attribute, Background, chest, eyes,...
        trait0 = trait0.replace('\n', '').replace('\\', '')
        if trait0[:1] == ' ':  # If there is a space in front of the attribute, delete it
            trait0 = trait0[1:]

        trait1 = trait1.replace('\n', '').replace('\\', '')
        if trait1[:1] == ' ':  # If there is a space in at the end of the attribute, delete it
            trait1 = trait1[1:]
        
        # Search for rarities and make them a float
        if 'rarity' in trait0:
            trait1 = float(trait1)
            continue

        # If you want to randomize a certain value the structure should be: integer(1, 40)
        if 'integer(' in trait1:
            trait1 = trait1.replace('integer(', '').replace(')', '')
            try:
                random_value_1 = int(trait1.split(',')[0].replace(' ', ''))
                random_value_2 = int(trait1.split(',')[1].replace(' ', ''))
            except:
                random_value_1 = 0
                random_value_2 = 100

            trait1 = random.randint(random_value_1, random_value_2)
        localAttributes[trait0] = trait1
    return localAttributes


def calculate(current_iteration, LAYERSTRUCTURE, total_layers):
    '''
    Everytime it get instantiated the current_position is: [0, 0, 0, 0, 0, 0].
    The current_iteration might be 2500 (out of 10000) for example, meaning,
    we are currently building each NFT and it is in the process of 2500.
    The LAYERSTRUCTURE [3, 5, 2, 1, 7, 8] is fixed and tells the current_position
    when to jump and sets the last value to 0 and the new one adds 1. In case the
    next one is in its limits sets that to 0 and the next one to 1 until we reach
    the end:
    [3, 0, 0, 0, 0, 0] -> [0, 1, 0, 0, 0, 0]
    [3, 5, 2, 1, 0, 0] -> [3, 5, 2, 0, 1, 0]
    [3, 5, 2, 1, 7, 0] -> [3, 5, 2, 1, 0, 1]
    [3, 5, 2, 1, 7, 8] -> end

    This is the picture which is going to be created, [3, 5, 2, 1, 0, 0]:
    layer1, image3
    layer2, image5
    layer3, image2
    layer4, image1
    layer5, image0
    layer6, image0

    '''

    # Create the template to run [0, 0, 0, 0, 0, 0]
    currentPosition = []
    for x in range(total_layers):
        currentPosition.append(0)

    # We want to create the image 3500, current_iteration, without building the entire project
    # We simply iterate through an empty array  which is LAYERSTRUCTURE
    k = 0
    for tempPosition in range(current_iteration):
        currentPosition[k] += 1
        for Kscan in range(len(LAYERSTRUCTURE)):
            if currentPosition[Kscan] >= LAYERSTRUCTURE[Kscan]:
                currentPosition[Kscan] = 0
                currentPosition[Kscan+1] += 1

    return currentPosition


def downsize_image(img_path):
    time.sleep(0.2)
    # Cou create a thumbnail image to reduce costs since it is going to be the cover of the 3mb file
    im = Image.open(img_path)
    width, height = im.size  # resize to 400*400
    if width > height:
        ratio = ((300.0 * 100.0) / width) / 100.0
    else:
        ratio = ((300.0 * 100.0) / height) / 100.0
    x = int(width * ratio)
    y = int(height * ratio)
    im = im.resize((x,y),Image.ANTIALIAS)
    im.save(f'{img_path[:-4]}_thumbnail.png', optimize=True, quality=70)


def update_nft_list(nfts_array, project_name):
    old_nft_list = nfts_array.items()
    old_nft_list = iter(old_nft_list)
    new_nft_list = {}
    next(old_nft_list)
    for elem in old_nft_list:
        new_nft_list[elem[0]] = elem[1]

    with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/randomized_nfts.json', 'w') as text:
        text.write(json.dumps(new_nft_list))

def main(project_name):
    # Load data
    path_files = add_paths(path)
    images_and_metadata = link_img_and_attr(path_files)
    description, website, artist = get_description_website_artist(project_name)

    # Load next NFT in line (current_iteration) and its file structure (current_array)
    with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/randomized_nfts.json', 'r') as text:
        nfts_array = json.loads(text.read())

    for elem in nfts_array.items():
        current_iteration = elem[0]
        current_array = elem[1]
        break


    attributes = []
    newPicture = []
    
    # Create now the metadatas attributes for later not to be hell
    metadata = {}

    # Store layers to create image
    # Iterate through current_array [[im_path, txt_path],[im_path, txt_path]]
    for layerDepth, itemNumber in enumerate(current_array):
        newPicture.append(images_and_metadata[layerDepth][0][itemNumber][0])
        attributes.append(addAttr(images_and_metadata[layerDepth][0][itemNumber][1]))

    # Add attributes
    metadata["attributes"] = {}
    for dictionay in attributes:
        for key in dictionay:
            metadata["attributes"][key] = dictionay[key]

    # Set new image and iterate over all layers
    newImage = Image.alpha_composite(newPicture[0], newPicture[1])
    for x, im in enumerate(newPicture):
        if x < 2: continue  # Skip the first 2 images since they are alreay created
        newImage = Image.alpha_composite(newImage, im)

    # Store the image created
    img_path = finished_result + '/' + project_name + str(current_iteration) + '.png'
    newImage.save(img_path)

    # Create a thumbnail
    downsize_image(img_path)

    # if addTextCode != 'addText':

    #   # The user does not want custom text on the NFT
    #   newImage.save(imagePath)
    # else:
    #   # The user wants custom text on the NFT
    #   text = project_name + ' #' + str(current_iteration)
    #   draw = ImageDraw.Draw(newImage)
    #   font = ImageFont.truetype("C:/Users/yop/Desktop/proyects/NFT/font/Athlone DEMO.ttf", 70)
    #   size2 = (size[0] - ((size[0]/8) * 7)), (size[1] - (size[1]/8))
    #   draw.text(size2, text, (0, 0, 0), font=font)
    #   newImage.save(imagePath)

    '''# Upload files to ipfs
    pid = os.fork()    
    if pid == 0:
        os.system(f'python3 /home/yop/Downloads/cardano-node1.30.0/commands/spltCommands/27_upload_im_ipfs.py {img_path}')
    else:
        print('waiting')
        os.wait()        


    # Retrieve url data
    with open(f'{img_path[:-4]}_hash.txt', 'r') as text:
        img_url = text.read()
    with open(f'{img_path[:-4]}_thumbnail_hash.txt', 'r') as text:
        thumb_url = text.read()'''
    # thumb_url = 'a'
    # img_url = 'b'
    # Create metadata
    temp_name = project_name
    temp_name = temp_name.replace('_', ' ')
    metadata["name"] = f'{temp_name} {current_iteration}'
    metadata["artist"] = artist
    metadata["description"] = description
    metadata["image"] = thumb_url
    metadata["mediaType"] = "image/jpeg"
    metadata["files"] = [{
            "name": f'{temp_name} {current_iteration}',
            "src": img_url,
            "mediaType": "image/jpeg"
          }]
    metadata["external_url"] = website
    metadata["ID"] = f'{current_iteration}'

    # Curate metadata
    # metadata = str(metadata).replace('\"', '').replace('\\', '').replace('"\"', "'").replace('"', "'")

    # Store metadata
    metadata = json.dumps(metadata)
    with open(finished_result + '/' + project_name + str(current_iteration) + '.json', 'w') as text:
        text.write(metadata)

    # Update randomized nfts
    update_nft_list(nfts_array, project_name)


try:
    main(project_name)
except:
    logging.exception('Got exception on main handler')
    raise
