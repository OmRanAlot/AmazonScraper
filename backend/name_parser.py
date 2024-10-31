import pandas as pd

break_char = [":","|", ",", "•"]
CPU = ["m3", "m2", "m1", "i3", "i5", "i7","i9","intel", "amd"]
storage_keyword = ["ssd","storage","emmc" ]
GPU_keyword = ["graphics", "GPU"]
manufacturer = ['lenovo', "apple", "dell", "hp","acer","razor", "asus"]

test = "HP Newest Essential 15.6\" FHD Laptop | Optimal AMD Processor for Entertainment and Personal Use | FHD Anti-Glare Display | Ethernet RJ-45 | SD Card Reader (Windows 11 Home, 16GB RAM | 1TB SSD)"
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
    RAM_index = max(word.find("ram"), word.find("unified"))
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

def get_data(word):
    return_this = {"CPU":find_cpu(word),
            "RAM": find_ram(word), 
            "Storage":find_storage(word)
            }
    is_full_of_none = all(value is None for value in return_this.values())

    if is_full_of_none:
        return None
    return return_this

# print(get_data(test.lower()))