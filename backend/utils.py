from random import choices
from string import ascii_letters, punctuation

CHARS = ascii_letters + punctuation
# TAKE FROM: https://stackoverflow.com/questions/201323/how-can-i-validate-an-email-address-using-a-regular-expression/
EMAIL_CHECKER_REGEX = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"

def generate_random_string(count: int) -> str:
    return "".join(choices(CHARS, k=count))


def get_metadata(arr):
    max1 = max2 = max3 = None
    min1 = min2 = min3 = None
    count = 0
    s = 0
 
    for a in arr:
        if max1 is None or a > max1:
            max1, max2, max3 = a, max1, max2
        elif max2 is None or a > max2:
            max2, max3 = a, max2
        elif max3 is None or a > max3:
            max3 = a
        
        if min1 is None or a < min1:
            min1, min2, min3 = a, min1, min2
        elif min2 is None or a < min2:
            min2, min3 = a, min2
        elif min3 is None or a < min3:
            min3 = a
        s += a
        count += 1
    
    count = max(count, 1)
    return [max3, max2, max1], [min3, min2, min1], s / count