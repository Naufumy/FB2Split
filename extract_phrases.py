import csv
from bs4 import BeautifulSoup
import re
import os
import random

def text_from_fb2(filename):
    with open(filename, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "lxml-xml")
        body = soup.find("body")
        text = body.get_text(separator=' ', strip=True) if body else ""
    return text

def split(text, max_len, min_len=100, max_phrases=3000):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    phrases = []
    current_phrase = ""

    for sentence in sentences:

        if len(sentence) < 100:
            continue 

        if not sentence.strip():
            continue
        
        if len(current_phrase) + len(sentence) + 1 <= max_len:
            current_phrase += (" " if current_phrase else "") + sentence
        else:
            if len(current_phrase) >= min_len:
                phrases.append(current_phrase.strip())
            current_phrase = sentence
        if len(phrases) >= max_phrases:
            break

    if len(current_phrase) >= min_len and len(phrases) < max_phrases:
        phrases.append(current_phrase.strip())

    return phrases

if __name__ == "__main__":

    fb2_files = [f for f in os.listdir() if f.lower().endswith(".fb2")]

    for fb2_file in fb2_files:
        try:
            max_len = random.randint(100, 1000)
            text = text_from_fb2(fb2_file)
            phrases = split(text, max_len)
            print(max_len)

            csv_filename = os.path.splitext(fb2_file)[0] + ".csv"

            with open(csv_filename, "w", encoding="utf-8-sig", newline="") as csvfile:
                writer = csv.writer(csvfile)
                for phrase in phrases:
                    writer.writerow([phrase])
        except Exception as e:
            print(f" Переписывай код, криворукий, вот ошибка: {fb2_file}: {e}\n")