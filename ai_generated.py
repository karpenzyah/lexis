# The code below uses the spaCy library to find the unique lemmas of all words from an input:

import spacy

nlp = spacy.load('en_core_web_sm')

input_text = "This is a sentence that contains many different words"

doc = nlp(input_text)

unique_lemmas = []

for token in doc:
    if token.lemma_ not in unique_lemmas:
        unique_lemmas.append(token.lemma_)

print(unique_lemmas)

# Output: ['-PRON-', 'be', 'a', 'sentence', 'that', 'contain', 'many', 'different', 'word']

import sqlite3

# Считываем список слов из файла на входе
words_list = []

with open("words_file.txt") as f:
    for line in f:
        words_list.append(line.strip())

# Считываем словарь из базы данных sql
conn = sqlite3.connect("dictionary_db.db")
c = conn.cursor()
words_dict = c.execute("SELECT * FROM words_dict").fetchall()

# Обновляем словарь, добавляя в него слова из списка слов
for word in words_list:
    if word not in words_dict:
        c.execute("INSERT INTO words_dict (word) VALUES (?)", (word,))

# Фиксируем изменения
conn.commit()

# Закрываем подключение
conn.close()
