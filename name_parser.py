'''
ML/AI model that retrives the info from the display name

see the CPU weght and GPU(if there) weight
Company name - DONE
CPU - DONE
RAM - -DONE
Storage - DONE
Screen size
'''


import pandas as pd
df = pd.read_csv("output.csv")

break_char = [":","|", ",",]
CPU = ["m3", "m2", "m1", "intel", "amd"]
storage_keyword = ["ssd","storage","emmc" ]
GPU_keyword = ["graphics", "GPU"]
manufacturer = ['lenovo', "apple", "dell", "hp","acer","razor"]

test = ["Lenovo V15 Laptop, 15.6"" FHD Display, AMD Ryzen 5 5500U Hexa-core Processor (Beat Intel i7-1065G7), 16GB RAM, 1TB SSD, HDMI, RJ45, Numeric Keypad, Wi-Fi, Windows 10 Home, 1.7Kg, Black".lower(),
        "HP Newest 15.6’’ FHD Laptop, 16GB DDR5 RAM, 1TB PCIe SSD, AMD Ryzen 5 7520U, AMD Radeon Graphics, Windows 11 Home, Webcam, Wi-Fi, Bluetooth, Long Battery Life, Alpacatec Accessories, Silver".lower(),
        "Apple 2024 MacBook Air 13-inch Laptop with M3 chip: 13.6-inch Liquid Retina Display, 8GB Unified Memory, 256GB SSD Storage, Backlit Keyboard, 1080p FaceTime HD Camera, Touch Bar, Silver".lower()]

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
    RAM_index = word.find("ram")
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


for i in test:
    # print(find_manufacturer(i))
    # print(find_cpu(i))
    print(find_storage(i))