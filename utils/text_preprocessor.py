import re

MAX_CHARS = 5000

def preprocess_text(text):

    replacements = {
        r"/s": "slash s",          
        r"TIFU": "Today I flipped Up",
        r"AITA": "Am I the a-hole?", 
        r"Fuck": "frick",
        r" asshole": "a-hole",
        r" ass": "booty",
        r"tits": "bazoingas",
        r"boobs": "bazoingas",
        r"OMG": "oh my glob",
        r"porn": "corn",
        r"WTF": "WHAT THE FLIP!",
        r"cum": "splooge",
        r"cummed": "shot rope",
        r"suicide": "sewer slide",
        r"kill": "unalive",
        r"killed": "unalived",

        
    }

    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)
    
    return text


def text_to_chunks(text, max_length=MAX_CHARS):
    chunks = []
    while len(text) > max_length:
        split_pos = text.rfind('.', 0, max_length) + 1
        if split_pos == 0:
            split_pos = max_length

        chunks.append(text[:split_pos].strip())
        text = text[split_pos:].strip()


    if len(text) > 0:
        chunks.append(text)

    return chunks
