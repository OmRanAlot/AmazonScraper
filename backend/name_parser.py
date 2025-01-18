import pandas as pd

break_char = [":","|", ",", "•"]
CPU = ["core", "m4", "m3", "m2", "m1", "i3", "i5", "i7","i9","intel", "amd", "cpu", "ryzen", "processor"]
storage_keyword = ["ssd","storage","emmc", "hdd"]
GPU = ["graphics", "gpu", "rtx", "geforce"]
manufacturer = ['lenovo', "apple", "dell", "hp","acer","razor", "asus"]

test = "ASUS ROG Strix G16 (2024) Gaming Laptop, 16” 16:10 FHD 165Hz Display, NVIDIA® GeForce RTX™ 4060, Intel Core i7-13650HX, 16GB DDR5, 1TB PCIe Gen4 SSD, Wi-Fi 6E, Windows 11, G614JV-AS74"
def find_cpu(word):
    temp = word.lower()
    
    index = -1
    for keyword in CPU:
        current_index = temp.find(keyword)
        if (index == -1 and current_index != -1) or (current_index != -1 and current_index < index):
            index = current_index

    if index > -1:
        # Move backward to find the start of the phrase (e.g., "8-Cores Intel Core i3")
        start = index
        while start > 0 and temp[start - 1] not in break_char:
            start -= 1
        
        # Move forward to find the end of the phrase
        end = index + 1
        while end < len(temp) and temp[end] not in break_char:
            end += 1
        
        return word[start:end].strip()
    
    return None
    
# def find_manufacturer(word):
#     for corp in manufacturer:
#         if corp in word and corp =="hp":
#             return "HP"
#         elif corp in word:
#             return corp.capitalize()

#     return None

def find_ram(word):
    temp = word.lower()

    RAM_index = max(temp.find("ram"), max(temp.find("unified"), max(temp.find("ddr5"), temp.find("ddr4"))))    #find break char on the left

    for i in range(RAM_index, 0, -1) :
        if temp[i] in break_char:
            left_break = i
            break
    #find break char on the right
    for i in range(RAM_index, len(temp)):
        if temp[i] in break_char or i == len(temp)-1 or temp[i] == " ":
            right_break = i
            break
    try:
        return word[left_break+1:right_break].strip()
    except:
        return None

def find_storage(word):
    temp = word.lower()
    ssd = temp.find("ssd")
    storage = temp.find("storage")
    emmc = temp.find("emmc")
    storage_index = ssd if ssd>-1 else storage if storage>-1 else emmc
    
    ram_index = max(temp.find("ram"), max(temp.find("unified"), max(temp.find("ddr5"), temp.find("ddr4"))))
    #find break char on the left
    for i in range(storage_index, 0, -1):
        if temp[i] in break_char or i == ram_index+2:
            left_break = i
            break
    #find break char on the right
    for i in range(storage_index, len(temp)):
        if temp[i] in break_char or i == len(temp)-1:
            right_break = i
            break

    try:
        return word[left_break+1:right_break].strip()
    except:
        return None

def find_GPU(word):
    temp = word.lower()
    index = -1
    for keyword in GPU:
        current_index = temp.find(keyword)
        if (index == -1 and current_index != -1) or (current_index != -1 and current_index < index):
            index = current_index

    #find break char on the left
    for i in range(index, 0, -1):
        if temp[i] in break_char:
            
            left_break = i
            break
    #find break char on the right
    for i in range(index, len(temp)):
        if temp[i] in break_char or i == len(temp)-1:
            right_break = i
            break

    try:
        return word[left_break+1:right_break].strip()
    except:
        return None

def get_specs(word):
    return_this = {
        "CPU":find_cpu(word),
            "RAM": find_ram(word), 
            "Storage":find_storage(word),
            "GPU":find_GPU(word)
            }
    is_full_of_none = all(value is None for value in return_this.values())

    if is_full_of_none:
        return None
    return return_this


