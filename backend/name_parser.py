import pandas as pd
import re

#gpu
test = "Gaming Laptop, Laptop with AMD Ryzen 7 5825U (8C/16T, Up to 4.5GHz), 16GB RAM 512GB NVMe SSD Laptop Computer, Radeon RX Vega 8 Graphics, 16.1-inch FHD Display, WiFi 6, 53Wh Battery, Backlit KB	"

def find_cpu(word):
    '''
    \d{3,5}[A-Za-z]{1,3} -> 3=5 numbers followed by 1-3 letters eg - 1234AB
    '''

    # expression = r'(?:(?:amd|intel|ryzen)[\S\s]*?(?:\d{3,5}[A-Za-z]{1,3}|[A-Za-z]{1}\d+)|(?:\S+)?Core[\S\s]*?(?:cpu|processor)|m\d(?:max)?|n5095 [\S\s]*?(?:cpu|processor|\)))'
    # expression1 = r'(?:\S+)?Core[\S\s]*?(?:\d{3,5}[A-Za-z]{1,3}|[A-Za-z]{1}\d+)' #has keyword "core"
    # expression2 = r'(?:amd|intel|ryzen)[\S\s]*?(?:\d{3,5}[A-Za-z]{1,3}|[A-Za-z]{1}\d+)' #has no keyword "core"
    # expression3 = r'(?:amd|intel) [\S\s]*? (?:cpu|processor)'
    # expression4 = r'(?:\S+)?Core[\S\s]*?(?:cpu|processor)'
   
    patterns = [
        r'm\d (?:max)?', #Apple M series chips
        r'(?:amd|intel|ryzen|(?:\S+)?Core)[\S\s]*?\d{4,5}[A-Za-z]{1,3}(\d)?', #Major specic AMD/Intel CPUs with numbers and specifics(like AMD Ryzen 5 5500X or i7-12300X)
        r'(?:amd|intel|ryzen|(?:\S+)?Core)[\S\s]*?[A-Za-z]{1}\d+',
        r'(?:amd|intel|(?:\S+)?Core)[\S\s]*?(?:cpu|processor|core)', #Major specic AMD/Intel CPUs without numbers and specfics(like AMD Ryzen 5 or Intel 4-core CPU)
        r'n\d+ ([\S\s]*? (?:cpu|processor|\)))?' #Intel N series chips
    ]


    
    for p in patterns:
        match = re.search(p,word, re.IGNORECASE)
        if match and len(match.group()) < 40:
            return match.group()
 
    return None



def find_GPU(word):
    # expression = r'(?:nvidia|geforce|rtx)[\S\s]*?\d{4}(\s?Ti)?' #has keyword "GPU"
    # expression2 = r'(?:amd|intel|iris)(?!.*(?:ryzen|cpu|processor))[\S\s]*?graphics'
    # expression4 = r'(?:\S+)?Core[\S\s]*?(?:gpu)'

    patterns = [
        r'(?:nvidia|geforce|rtx)[\S\s]*?\d{4}(\s?Ti)?', #has keyword "GPU"
        r'(?:amd|intel|iris|radeon)(?!.*(?:ryzen|cpu|processor))[\S\s]*?graphics',
        r'(?:\S+)?Core[\S\s]*?(?!\s*(?:CPU))(?:gpu)',
        r'(?:radeon|amd|intel|(?:\S+)?Core)[\S\s]*?(?:gpu|graphics)'
    ]

    for p in patterns:
        match = re.search(p,word, re.IGNORECASE)
        if match and len(match.group()) < 40:
            return match.group()
 
    return None


def find_ram(word):
    # expression = r'(?:\S+)?RAM[\S\s]*?\d{3,5}[A-Za-z]{1,3}' #has keyword "RAM"
    expression = r'\d+\s?GB\s?(?:DDR\d\s?|RAM|Unified Memory)' #has keyword "RAM"
    match = re.search(expression,word, re.IGNORECASE)
    if match:
        return match.group()

    return None

def find_storage(word):
    # expression = r'\d+(?:TB|GB)\s*(?:(?!RAM|DDR)[\S\s])*(?:storage|ssd|hdd)'
    expression = r'\d+(?:\s?)(?:TB|GB)(?!\s*(?:RAM|DDR|Unified Memory))[\S\s]*?(?:storage|SSD|HDD|eMMC)'
    match = re.search(expression,word, re.IGNORECASE)

    if match:
        return match.group()
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


print(find_GPU(test))

# print(find_cpu(test2))
# print(find_cpu(test3))
# print(find_cpu(test4))