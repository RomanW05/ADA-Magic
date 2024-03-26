import random
import sys
import time
import os
import json
from os.path import exists

'''
What does this script do?
    Creates a unique list of NFTs based upon desired rarities and randomizes such list.
    A project with 5 layers ,for example, and 3 images within each layer the output will be:
    {0 :{0, 1, 2}, 1: {2, 2, 0}, 2{2, 0, 0}, 3: {1, 0, 0}, 4: {0, 0, 2}, ..., NFT_total -1, NFT_total}

Explanation, the array 0, 2, 2, for example tells us to use the first image of the first layer,
the third image of the second layer and the third image of the third layer. Then you will
only need to load such combination of files and their metadata to create a unique NFT. To finish
delete such combination from the stored file and when the next NFT gets asked to be minted
just load the next combination.

How does it work?
- Iterate over the folder with images and metadata files to obtain rarities percentages
    [[15.0, 15.0, 10.0, 10.0, 20.0, 20.0, 10.0], [75.0, 25.0], [10.0, 80.0, 10.0], ...]

-Use the total number of nfts and create another array with the total amount of times
    each image will be used in the collection, for a project with total 1000 NFTs:
    [[150, 150, 100, 100, 100, 200, 200, 100], [750, 25], [100, 800, 100], ...]

- Challenge, they might not be integers. Solution, round the numbers

- Next challenge, the sum of all images within one layer might not add up to the
    total number of NFTs in the collection. Solution, add one to the lowest element
    of each layer or subtract one from the highest element

- The core of the program. This is taken as a sodoku where you will first choose the highest
values from each layer to be minted, then all highest values from all layers except from 2 random
layers which will be not the highest value but some random ones, to finish all random values
from each layer.

- NOTE: I think of being at the top of a mountain and you need to work your way down. You don't
go down the steepest path but from the easiest with less slope. That way there are less chances
of finding a dead-end and not been able to continue 

'''

project_name = sys.argv[1]
total_nfts = int(sys.argv[2])

def add_paths(project_name):
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
    path = f'/home/yop/Downloads/cardano/vending_machine/{project_name}'
    files_in_project = os.listdir(path)
    files_in_project.sort()
    for layer in files_in_project:
        if 'layer' not in str(layer):
            continue

        x = int(str(layer)[-1:]) -1  # Extract layer number, make it array readable
        files = os.listdir(f'{path}/{layer}/')
        files.sort()

        # If there is no metadata, create it
        metadata_array = []
        for file in files:
            if '.png' in file:
                metadata_array.append(file)
        for file in metadata_array:
            if exists(f'{path}/{layer}/{file[:-4]}.txt'):
                continue
            with open(f'{path}/{layer}/{file[:-4]}.txt', 'w') as text:
                text.write('')

        for file in files:
            filename = f'{path}/{layer}/{file}'
            try:
                path_files[x].append(filename)
            except:
                path_files.append([])
                path_files[x].append(filename)

    return path_files


def read_rarities(path_files):
    layer_structure = []
    for layer_number, elem in enumerate(path_files):
        fields = []
        
        for number_spot, number_number in enumerate(elem):
            if ((number_number.endswith('png', -3)) or (number_number.endswith('PNG', -3))):
                continue
            try:
                with open(number_number, 'rb') as text:
                    metadata = text.read()
            except:
                with open(number_number, 'r') as text:
                    metadata = text.read()
            localAttributes = addAttr(metadata)
            try:
                rarity = float(localAttributes['rarity'])
                fields.append(rarity)
            except:
                # In case user does not provide with rarity
                fields.append(0)

        # In case user does not provide with rarity check
        # Take all metadata which actually have rarities
        # Add rarities together -> rarities_sum
        # Subtract 100 -> result
        # Divide total amount of metadata with 0 in it by result -> result2
        # Give each metadata with 0 in it the value result2
        metadata_array = []  # In case user does not provide with rarity
        if 0 in fields:
            rarities_sum = 0.0
            for position, rarity in enumerate(fields):
                if rarity == 0:
                    metadata_array.append(position)
                else:
                    rarities_sum += float(rarity)
            result = 100 - float(rarities_sum)
            result2 = result / len(metadata_array)

            for position, rarity in enumerate(fields):
                if rarity == 0:
                    result2 = round(result2, 2)
                    fields[position] = result2
        layer_structure.append(fields)

    return layer_structure


def addAttr(metadata):
    # Create a dictionary of the metadata
    localAttributes = {}
    try:
        metadata = metadata.split('\n')
    except:
        metadata = str(metadata)
        metadata = metadata.split('\n')

    for elem in metadata:
        try:
            numberElements = elem.split(':')
        except:
            continue

        if len(numberElements) < 2: continue  # Document why this
        trait0, trait1 = elem.split(':')
        trait0 = trait0.replace('\n', '')
        trait1 = trait1.replace('\n', '')

        # Clean the attributes
        trait0 = trait0.replace('\n', '').replace('\\', '')
        if trait0[:1] == ' ':
            trait0 = trait0[1:]
        trait1 = trait1.replace('\n', '').replace('\\', '')
        if trait1[:1] == ' ':
            trait1 = trait1[1:]

        localAttributes[trait0] = trait1

    return localAttributes


def random_int():
    random_number1 = random.randint(0, 100)
    random_number2 = float(random.randint(0, 100))/100.0
    random_number = random_number1 + random_number2
    if random_number > 100.0:
        random_number = 100.0

    return random_number


def create_layer_structure(imagesAndMetadata):
    '''
    Very important, this is the core of the iteration
    Very useful for vending machine, rarities and randomly selected items

    '''
    total_layers = len(imagesAndMetadata)
    LAYERSTRUCTURE = []
    currentPosition = []
    total_iterations = 1
    for x in range(total_layers):
        currentPosition.append(0)
    for layer in imagesAndMetadata:

        # Layer is composed of [img.png, text.txt], [img2.png, text2.txt]
        # LAYERSTRUCTURE is like: [3,5,2,1,7,8]
        LAYERSTRUCTURE.append(len(layer))
        total_iterations *= len(layer)  # Total number of NFTs

    return LAYERSTRUCTURE, total_iterations, total_layers


def calculate(LAYERSTRUCTURE, currentPosition):
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

    for tempPosition in range(1):
        currentPosition[0] += 1
        for Kscan in range(len(LAYERSTRUCTURE)):

            # This is like regular addition, then a number is greater than 9 it gets
            # Reset to 0 adding one to the carrier and onto the next number
            if currentPosition[Kscan] >= LAYERSTRUCTURE[Kscan]:
                currentPosition[Kscan] = 0
                currentPosition[Kscan+1] += 1

    return currentPosition


def create_structure(layers):
    structure = []
    for layer in layers:
        structure.append(len(layer))

    return structure


def create_image_structure(structure, layers):
    imgs_structure = []
    imgs_structure_copy = []
    for x, number in enumerate(structure):
        fields = []
        for layer in layers[x]:
            fields.append(int(layer * total_nfts / 100.0))
        imgs_structure.append(fields[:])

    return imgs_structure


def round_structure(imgs_structure):
    # Round the structure so the addition of each layer adds up to the total number of NFTs
    # Start by rounding each element in the total-to-be-minted of each file
    for layer_number, elem in enumerate(imgs_structure):
        for spot, number in enumerate(elem):
            imgs_structure[layer_number][spot] = round(imgs_structure[layer_number][spot], 0)

    # Check for unbalaces in each layer
    for layer_number, elem in enumerate(imgs_structure):
        x = 0
        for number_spot, number_number in enumerate(elem):
            x += number_number
        if x != total_nfts:
            # print(f'ooops {x} elements and should there be {total_nfts} in {elem}')

            # Distance between target and actual state
            distance = total_nfts - x
            if distance > 0:

                # Add one more to the lowest number
                temp_spot = elem[0]
                temp = 0
                for iterations_needed in range(distance):
                    for number_spot, number_number in enumerate(elem):
                        if number_number < temp_spot:
                            temp = number_spot
                    elem[temp] += 1
                    # print(f'Fixing array, now there is one more number of the lowest image {elem}')
            else:

                # Subtract one more to the biggest number
                temp_spot = elem[0]
                temp2 = 0
                for iterations_needed in range(distance):
                    for number_spot2, number_number2 in enumerate(elem):
                        if temp_spot > number_number2:
                            temp2 = number_spot2
                    elem[temp2] -= 1

    return imgs_structure


def highest(imgs_structure):
    fields = []
    for layer_number, elem in enumerate(imgs_structure):
        index = elem.index(max(elem))
        fields.append(index)

    return fields


def one_random(imgs_structure):
    fields = []

    # Layer randomness
    random_layer = random.randint(0, len(imgs_structure)-1)
    while len(imgs_structure[random_layer]) == 1:
        random_layer = random.randint(0, len(imgs_structure)-1)

    for layer_number, elem in enumerate(imgs_structure):
        if layer_number == random_layer:

            # Array randomness
            random_array = random.randint(0, len(elem)-1)
            while elem[random_array] == max(elem):
                random_array = random.randint(0, len(elem)-1)

            fields.append(random_array)
            continue

        index = elem.index(max(elem))
        fields.append(index)


    return fields


def two_random(imgs_structure):
    fields = []

    # Layer randomness
    random_layer1 = random.randint(0, len(imgs_structure)-1)
    random_layer2 = random.randint(0, len(imgs_structure)-1)
    while ((random_layer1 == random_layer2) or (len(imgs_structure[random_layer1]) == 1) or (len(imgs_structure[random_layer2]) == 1)):
        random_layer1 = random.randint(0, len(imgs_structure)-1)
        random_layer2 = random.randint(0, len(imgs_structure)-1)

    for layer_number, elem in enumerate(imgs_structure):
        if layer_number in [random_layer1, random_layer2]:

            # Array randomness
            random_array = random.randint(0, len(elem)-1)
            while elem[random_array] == max(elem):
                random_array = random.randint(0, len(elem)-1)

            fields.append(random_array)
            continue
        
        index = elem.index(max(elem))
        fields.append(index)

    return fields


def all_random(imgs_structure):
    fields = []
    for layer_number, elem in enumerate(imgs_structure):
        random_number = random.randint(0, len(elem)-1)
        if len(elem) == 1:
            fields.append(0)
            continue
        fields.append(random_number)

    return fields


def check_fields(fields, imgs_structure, randomized):
    flag = False

    if fields not in randomized:
        is_good = True
        for layer_number, spot in enumerate(fields):
            if imgs_structure[layer_number][spot] == 0:  # You can still use this image
                is_good = False
        if is_good:
            randomized.append(fields)
            flag == True

    return randomized, flag



# Initiate values
path_files = add_paths(project_name)
layers = read_rarities(path_files)

# structure = [7, 6, 9, 3, 4, 8]
structure = create_structure(layers)
LAYERSTRUCTURE, total_iterations, total_layers = create_layer_structure(layers)
imgs_structure = create_image_structure(structure, layers)
imgs_structure = round_structure(imgs_structure)

START_POSITION = []
for x in range(total_layers):
    START_POSITION.append(0)

randomized = []
# This while loop is where all the thinking goes
while len(randomized) < total_nfts:
    # print(len(randomized))
    highest_flag = False
    one_random_flag = False
    two_random_flag = False

    fields = highest(imgs_structure)
    randomized, highest_flag = check_fields(fields, imgs_structure, randomized)

    # if not highest_flag:
    #   fields = one_random(imgs_structure)
    #   randomized, one_random_flag = check_fields(fields, imgs_structure, randomized)

    # if ((not highest_flag) and (one_random_flag)):
    fields = two_random(imgs_structure)
    randomized, two_random_flag = check_fields(fields, imgs_structure, randomized)

    fields = all_random(imgs_structure)
    randomized, two_random_flag = check_fields(fields, imgs_structure, randomized)


# Make sure there are no repeats in the list
new_list = []
for x in randomized:
    if x not in new_list:
        new_list.append(x)
    else:
        with open('/home/yop/Downloads/cardano/error_log.txt', 'a') as test:
            error = f'\n List of NFTs to be minted is not unique \n'
            text.write(error)

# Create rarity sheat:
rarity_sheat = []
rarity_sheat_string = ''
for layer_number, elem in enumerate(imgs_structure):
    rarity_sheat_string += f'Layer {layer_number+1}:\n'
    fields = [f'Layer {layer_number+1}:']
    for position, picture_amount in enumerate(elem):
        number = float(picture_amount) / float(total_nfts) * 100
        number = f'{format(number, ".2f")}% '  # format(myFloat, '.2f')
        file_name = path_files[layer_number][(position*2)].split('/')[-1][:-4]
        number = f'{file_name}: {number}\n'
        rarity_sheat_string += number
        fields.append(number)
    # rarity_sheat.append(fields)
    rarity_sheat_string += '\n\n'
rarity_sheat_string = rarity_sheat_string[:-1]

random.shuffle(new_list)
random_dict = {}

for x, elem in enumerate(new_list):
    random_dict[x] = elem

finished_list = json.dumps(random_dict)
with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/randomized_nfts.json', 'w') as text:
    text.write(finished_list)

with open(f'/home/yop/Downloads/cardano/vending_machine/{project_name}/rarity_sheat.txt', 'w') as text:
    text.write(rarity_sheat_string)

print(f'key555word{rarity_sheat_string}key555word')
sys.exit()