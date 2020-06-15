def create_lda(story_list, num_topics):  
    from nltk import sent_tokenize
    import pyLDAvis.gensim
    import re
    for i in range(len(story_list)):
        story = story_list[i]
        sents = sent_tokenize(story)
        for j in range(len(sents)):
            sent = sents[j]
            sent = sent.strip().replace('\n','')
            sent = re.sub('[0-9]', '', sent)
            sents[j] = sent
        story_list[i] = '. '.join(sents)

    texts = [[word for word in story.lower().split()
            if word not in STOPWORDS and word.isalnum() and not word.lower() == 'technology' and not word.lower() == 'science']
            for story in story_list]

    corpus = [dictionary.doc2bow(text) for text in texts] #(word_id,freq) pairs by sentence
    num_topics = num_topics #The number of topics that should be generated
    passes = 10
    lda = LdaModel(corpus,
                  id2word=dictionary,
                  num_topics=num_topics,
                  passes=passes)
    lda_display = pyLDAvis.gensim.prepare(lda, corpus, dictionary, sort_topics=False)
    return (lda, lda_display)



import pandas as pd

#Get data from files
bodies1 = pd.read_csv("top_bodies1.csv").drop(columns = {"Unnamed: 0", "urls"})
bodies2 = pd.read_csv("top_bodies2.csv").drop(columns = {"Unnamed: 0", "urls"})
bodies3 = pd.read_csv("top_bodies3.csv").drop(columns = {"Unnamed: 0", "urls"})

all_bodies = pd.concat([bodies1, bodies2, bodies3])
all_bodies['text'] = all_bodies['text'].astype(str)
all_bodies['Month'] = pd.to_datetime(all_bodies['Month'],format='(%Y, %m)')
all_bodies['year'] = all_bodies['Month'].apply(lambda x: x.year)
all_bodies['month'] = all_bodies['Month'].apply(lambda x: x.month)
all_bodies = all_bodies.drop(columns = {'Month'})



import math  
all_bodies['decade'] = all_bodies['year'].apply(lambda x: math.floor(x/10))

text_lists_yearly = pd.DataFrame(all_bodies[['year','text']].groupby(['year'])['text'].apply(list))
text_lists_decade = pd.DataFrame(all_bodies[['decade','text']].groupby(['decade'])['text'].apply(list))


import nltk
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from gensim.parsing.preprocessing import STOPWORDS
import pprint

texts = [[word for word in story.lower().split()
            if word not in STOPWORDS and word.isalnum() and not word.lower() == 'technology']
            for story in list(all_bodies['text'])]

dictionary = corpora.Dictionary(texts)

#Create LDAs
lda_80 = create_lda(text_lists_decade['text'][198], 25)
lda_90 = create_lda(text_lists_decade['text'][199], 25)
lda_00 = create_lda(text_lists_decade['text'][200], 25)
lda_10 = create_lda(text_lists_decade['text'][201], 25)

#Show Visualization
import pyLDAvis.gensim
pyLDAvis.display(lda_80[1])
pyLDAvis.display(lda_90[1])
pyLDAvis.display(lda_00[1])
pyLDAvis.display(lda_10[1])


