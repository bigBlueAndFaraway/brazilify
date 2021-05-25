'''
creates word lists for language learners to track their vocabulary.
Texts that the learner read & fully understood can be put in a folder and processed automatically.

currently only supports portuguese
can't identify inifitive of a verb but adds all forms of the verb if it encounters an infinitive

next up: I'll write a function that, given a text, returns a list of all words
    currently not in the learners vocabulary
'''

import pandas as pd
import mlconjug3 as mlc
import os
import re


PATH = 'G:\Meine Ablage\Portugiesisch'
FOLDERPATH = 'G:\Meine Ablage\Portugiesisch\Articles for frequency list'
'''PATH is the working directory. FOLDERPATH is the path to the folder with texts to process'''

os.chdir(PATH)
CON = mlc.Conjugator(language='pt')

def get_forms(verb, con=mlc.Conjugator(language='pt')):
    '''given a verb returns a list of all conjugations of the verb'''

    full_list = con.conjugate(verb).iterate()
    form_list = [form[-1] for form in full_list if form[-1]]

    return form_list


def add_text_to_list(file_name, current_vocab):
    '''adds all new words from the given file to the given vocabulary list'''

    with open(file_name, encoding='UTF8') as text:
        wordList = pd.Series(text.read().split(), name='words')
    current_vocab = current_vocab.append(pd.DataFrame(wordList))
    '''NEEDS DROP DUPLICATES?'''
    return current_vocab


def create_freq_list(folder_path):
    '''reads txt files in folder_path, returns dataframe of words and occurences'''

    os.chdir(folder_path)
    frequency_list = pd.DataFrame({'words':[], 'occurences':[]})

    file_list = [f for f in os.listdir(folder_path) if f[-4:] == '.txt']
    for file in file_list:
        with open(file, encoding='UTF8') as text:
            raw_text = text.read()
            text = re.sub('\W+', ' ', raw_text)
            word_list = pd.Series(text.split()).value_counts()
            df_words = pd.DataFrame({'words': word_list.index, 'occurences': word_list})
            frequency_list = frequency_list.append(df_words)

    frequency_list = frequency_list[~frequency_list.words.str.isdigit()]
    frequency_list = frequency_list.groupby(by='words').sum()
    frequency_list = frequency_list.sort_values('occurences', ascending=False)
    frequency_list = frequency_list.reset_index()
    os.chdir(PATH)

    return frequency_list


dw_frequency = create_freq_list(FOLDERPATH)
current_vocab = pd.Series(['bom', 'dia'], name='words')
current_vocab.to_csv('pt_vocab.csv', index=False)
current_vocab = pd.read_csv('pt_vocab.csv')
new = add_text_to_list('pt_test.txt', current_vocab)

out = pd.merge(new, dw_frequency, how='inner', on='words')
