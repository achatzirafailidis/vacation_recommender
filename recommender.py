import pandas as pd
import spacy
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

def text_processing(sentence):
    """
    Lemmatize, lowercase, remove numbers and stop words
    
    Args:
      sentence: The sentence we want to process.
    
    Returns:
      A list of processed words
    """
    sentence = [token.lemma_.lower()
                for token in nlp(sentence) 
                if token.is_alpha and token.pos_=='NOUN' and not token.is_stop]
    
    return sentence

def recommendation_calc(text, feature):
    clean_text = text_processing(text)

    feature_df = pd.read_csv('/home/alex/Spiced/final_project/full_feature_list.csv')
    feature_df = feature_df[feature_df['label']==feature]

    similarity_list = []
    clean_text_token = nlp(" ".join(clean_text))
    feature_list = feature_df.values.tolist()

    for t in feature_list:
        tag_tokens = nlp(t[3])
        for i in tag_tokens:
            for c in clean_text_token:
                #print(i.text, c.text,i.similarity(c))
                similarity_list.append([t[1], i.text,c.text,i.similarity(c)])

    similarity_df = pd.DataFrame(similarity_list, columns = ['Destination', 'tag_user_input', 'tag_flickr', 'similarity_mean'])
    sim = similarity_df.groupby([0, 3])[3].count().max(level=0).reset_index()
    sim_mean = similarity_df.groupby([0])[3].mean().sort_values(ascending=False)
    #print("sim",sim)
    recommendation = sim.sort_values(by=3, ascending=False).head(5)
    
    rec1 = recommendation.merge(sim_mean, how='left', on=0)

    return rec1['Destination']