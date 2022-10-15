import spacy

# loading and creating the corpus
nlp = spacy.load('en_core_web_sm')

def get_tokens(text):
    # tokenize the text
    # lemmatize the tokens
    # return the lemmatized tokens
    nlp_text = nlp(text) 
    token_list = [token for token in nlp_text] 

    filtered_tokens = []
    for word in token_list:
        lexeme = nlp.vocab[word.text]
        if lexeme.is_stop == False:
            filtered_tokens.append(word.lemma_)

        
    return filtered_tokens