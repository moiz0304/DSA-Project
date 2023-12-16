import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer #TF-IDF Vectorization METHOD
from sklearn.metrics.pairwise import cosine_similarity # measure of similarity
from nltk.corpus import stopwords # import stop words
from nltk.tokenize import word_tokenize # split text to individual parts

# Load the CSV data into a DataFrame
df = pd.read_csv('data/data.csv')

# Preprocess the descriptions
stop_words = set(stopwords.words('english')) # the stop words in english language

def preprocess_text(text):
    word_tokens = word_tokenize(text.lower()) # tokenize the words
    filtered_text = [word for word in word_tokens if word.isalnum() and word not in stop_words] # alphanumeric words - stop words
    return ' '.join(filtered_text)

df['Processed_Description'] = df['Description'].apply(preprocess_text) # apply tokenization to the desciptions

# Vectorize the descriptions using TF-IDF
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df['Processed_Description'])

def search_images(query, df, tfidf_matrix, tfidf_vectorizer):
    # Preprocess the query
    processed_query = preprocess_text(query)
    
    # Vectorize the query
    query_vector = tfidf_vectorizer.transform([processed_query])
    
    # Calculate cosine similarity between the query and all image descriptions
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    
    # Rank images based on similarity
    df['Similarity'] = cosine_similarities
    ranked_df = df.sort_values(by='Similarity', ascending=False)
    
    # Extract relevant information
    result_image_names = ranked_df['Image Name'].tolist()
    result_similarity_scores = ranked_df['Similarity'].tolist()
    
    return result_image_names, result_similarity_scores

# Example usage
query = "blue bicycle"
result_image_names, result_similarity_scores = search_images(query, df, tfidf_matrix, tfidf_vectorizer)
i = 1
# Display the results
for image_name, similarity_score in zip(result_image_names, result_similarity_scores):
    if i > 3: # only top 3 results
        break
    else:
        if similarity_score > 0:
            print(f"Image: {image_name}, Similarity Score: {similarity_score}") # if top 3 has a zero similarity score don't display
        else:
            break
    i=i+1