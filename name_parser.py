import pandas as pd

break_char = [":","|", ","]
CPU = ["m3", "m2", "m1", "intel", "amd"]
storage_keyword = ["ssd","storage","emmc" ]
GPU_keyword = ["graphics", "GPU"]
manufacturer = ['lenovo', "apple", "dell", "hp","acer","razor", "asus"]

test = ["Lenovo V15 G4 Business Laptop, 15.6\" FHD Screen, 13th Gen Intel 10 Cores i7-1355U up to 5.0GHz, 24GB RAM, 1TB PCIe SSD, HD Camera with Privacy Shutter, Wi-Fi, HDMI, Windows 11 Pro, Black".lower()]

def find_cpu(word):
    length = int (len(word))
    index = -1
    for i in CPU:
        current_index = word.find(i)
        if (index == -1 and current_index != -1) or (current_index != -1 and current_index < index):
            index = current_index
            
    if index >-1:
        temp = word[index-1:length]

        for j in break_char:
            if temp.find(j) > -1:
                return temp[:temp.find(j)].strip()

    return "Unable to find CPU"
    
def find_manufacturer(word):
    for corp in manufacturer:
        if corp in word and corp =="hp":
            return "HP"
        elif corp in word:
            return corp.capitalize()

    return "Unable to find manufacturer"

def find_ram(word):
    RAM_index = max(word.find("ram"), word.find("unified"))
    for i in range(RAM_index, 0, -1):
        if word[i] in break_char:
            left_break = i
            break
    for i in range(RAM_index, len(word)):
        if word[i] in break_char:
            right_break = i
            break
    try:
        return word[left_break+1:right_break].strip()
    except:
        return "Unable to find RAM"

def find_storage(word):
    ssd = word.find("ssd")
    storage = word.find("storage")
    emmc = word.find("emmc")
    storage_index = ssd if ssd>-1 else storage if storage>-1 else emmc
    

    #find break char on the left
    for i in range(storage_index, 0, -1):
        if word[i] in break_char:
            left_break = i
            break
    #find break char on the right
    for i in range(storage_index, len(word)):
        if word[i] in break_char:
            right_break = i
            break

    try:
        return word[left_break+1:right_break].strip()
    except:
        return "Unable to find Storage"


def get_data(word):
    return {"manufacturer": find_manufacturer(word), 
            "CPU":find_cpu(word),
            "RAM": find_ram(word), 
            "Storage":find_storage(word)
            }

# for i in test:
#     print(get_data(i))