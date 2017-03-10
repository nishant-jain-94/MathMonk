import math
from nltk import word_tokenize, sent_tokenize
from collections import Counter

def cosine_distance(statement, other_statement):
    
    tokenized_statement = word_tokenize(statement.lower())
    tokenized_other_statement = word_tokenize(other_statement.lower())
    
    vector1 = Counter(tokenized_statement)
    vector2 = Counter(tokenized_other_statement)
    
    intersection = set(vector1) & set(vector2)
    numerator = sum([vector1[word] * vector2[word] for word in intersection])
    
    squared_sum_of_vector1 = sum([vector1[word] ** 2 for word in vector1.keys()])
    squared_sum_of_vector2 = sum([vector2[word] ** 2 for word in vector2.keys()])
    
    root_of_squared_sum_of_vector1 = math.sqrt(squared_sum_of_vector1)
    root_of_squared_sum_of_vector2 = math.sqrt(squared_sum_of_vector2)
    
    denominator = root_of_squared_sum_of_vector1 * root_of_squared_sum_of_vector2
    
    if not denominator:
        return 0
    else:
        return float(numerator) / denominator