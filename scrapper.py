#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lxml import html
import requests

main = "https://jisho.org/search/"

# Gets all 'possible' meanings of the japanese word and asks 
# user for actual answer.
def get_meaning(japanese_word):
    page = requests.get(main + japanese_word)
    tree = html.fromstring(page.content)
    meanings = tree.xpath('//span[@class="meaning-meaning"]/text()')

    for i, meaning in enumerate(meanings):
        print(str(i + 1) + ": " + meaning)
    print(str(len(meanings) + 1) + ": other")
    meaning_tab = input()
    while not meaning_tab.isdigit():
        meaning_tab = input()
    meaning_tab = int(meaning_tab)
    if meaning_tab <= len(meanings):
        return meanings[meaning_tab - 1].replace(";", " /")
    else:
        return input()

if __name__ == "__main__":
    count = 0
    tag = input("Tag for all the cards : ")

    with open("output.txt", 'w', encoding='utf8') as output_obj:
        with open("input.txt", 'r', encoding='utf8') as input_obj:
            for line in input_obj.readlines():
                print("\n" * 50) # because clrscreen doesn't work for me 
                line = line[:-1]
                if count % 2 == 0:
                    if len(line.split("(")) > 1:
                        kanji, hiragana = line.split("(")[0], line.split("(")[1]
                        kanji = kanji.rstrip()
                        hiragana = hiragana[:hiragana.find(")")]
                        print("OUT : " + hiragana + " " + kanji)

                        meaning = get_meaning(kanji)
                        output_obj.write(meaning + ";" + hiragana + ";" + kanji + ";" + str(tag) + "\n")
                    else:
                        hiragana = line.strip()
                        print("OUT : " + hiragana)
                        meaning = get_meaning(hiragana)
                        output_obj.write(meaning + ";" + hiragana + ";;" + str(tag) + "\n")
                count += 1
