import pandas as pd

break_char = [":","|", ",", "•"]
CPU = ["m3", "m2", "m1", "i3", "i5", "i7","i9","intel", "amd"]
storage_keyword = ["ssd","storage","emmc" ]
GPU_keyword = ["graphics", "GPU"]
manufacturer = ['lenovo', "apple", "dell", "hp","acer","razor", "asus"]

test = "ASUS ROG Strix G16 (2024) Gaming Laptop, 16” 16:10 FHD 165Hz Display, NVIDIA® GeForce RTX™ 4060, Intel Core i7-13650HX, 16GB DDR5, 1TB PCIe Gen4 SSD, Wi-Fi 6E, Windows 11, G614JV-AS74	"
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

    return None
    
def find_manufacturer(word):
    for corp in manufacturer:
        if corp in word and corp =="hp":
            return "HP"
        elif corp in word:
            return corp.capitalize()

    return None

def find_ram(word):
    RAM_index = max(word.find("ram"), max(word.find("unified"), word.find("ddr5")))
    for i in range(RAM_index, 0, -1) :
        if word[i] in break_char:
            left_break = i
            break
    for i in range(RAM_index, len(word)):
        if word[i] in break_char or i == len(word)-1:
            right_break = i
            break
    try:
        return word[left_break+1:right_break].strip()
    except:
        return None

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
        if word[i] in break_char or i == len(word)-1:
            right_break = i
            break

    try:
        return word[left_break+1:right_break].strip()
    except:
        return None

def get_specs(word):
    return_this = {"CPU":find_cpu(word),
            "RAM": find_ram(word), 
            "Storage":find_storage(word)
            }
    is_full_of_none = all(value is None for value in return_this.values())

    if is_full_of_none:
        return None
    return return_this

# print(get_specs(test.lower()))