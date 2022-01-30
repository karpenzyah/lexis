import spacy
import memory_profiler
import os.path
import time
import csv


# @memory_profiler.profile
def spacy_process(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)

    lemma_list = []
    for token in doc:
        if token.is_alpha and token.__len__() > 1:
            lemma = token.lemma_.lower()
            lemma_list.append(lemma)
    del doc
    lemms_len = lemma_list.__len__()
    # Filter the stopword
    filtered_sentence = []
    for word in lemma_list:
        lexeme = nlp.vocab[word]
        if not lexeme.is_stop:
            filtered_sentence.append(word)
    words_len = filtered_sentence.__len__()

    del lemma_list

    unique = list(set(filtered_sentence))
    unique_len = unique.__len__()

    return lemms_len, words_len, unique_len, unique


path_to_file = 'base.txt'

start_time = time.time()
buff_size = 100000
all_lemms_len = 0
all_words_len = 0
all_words = []

with open(path_to_file) as file:
    pointer = 0
    while pointer < os.path.getsize(path_to_file):
        text = file.read(buff_size)
        pointer = file.tell()
        # print(pointer)
        res = spacy_process(text)
        all_lemms_len += res[0]
        all_words_len += res[1]
        all_words += res[3]
        # print('Lemms:', lemms_len)
        # print('Unique words:', unique_len)
        # print('Words:', words_len)

unique = list(set(all_words))

print('All lemms:', all_lemms_len)
print('All words:', all_words_len)
print('All processed unique:', all_words.__len__())
print(sorted(unique))
print('All unique:', unique.__len__())

print("--- %s seconds ---" % (time.time() - start_time))


def find_unknown(text, where):
    unknown = []
    str = ''
    for row in where:
        str += row["word"]
    # sorted_s = sorted(str)
    for word in text:
        if str.find(word) == -1:
            unknown.append(word)
    return sorted(unknown)


start_time = time.time()
with open('dict.csv', newline='\n') as base_dict:
    reader = csv.DictReader(base_dict)
    dict_f = []
    for row in reader:
        dict_f.append(row)

uknwn = find_unknown(unique, dict_f)
print(uknwn, '\n', uknwn.__len__())
print("--- %s seconds ---" % (time.time() - start_time))
input(f'Совпадений в словаре {unique.__len__()-uknwn.__len__()}\nНажмите для начала ввода')
os.system('clear')


def write_dict(words):
    dict_write = open('dict.csv', 'a')
    cnt_w = 0
    for word in words:
        os.system('clear')
        weight = input(f'{word}:\t')
        if weight == 'e':
            dict_write.close()
            return cnt_w
        elif weight == 'p':
            continue
        else:
            dict_write.write(f'{word},{weight}\n')
            cnt_w += 1


r = write_dict(uknwn)
print(f'Записано слов в словарь: {r}\nВсего в словаре: {r+reader.line_num}')
