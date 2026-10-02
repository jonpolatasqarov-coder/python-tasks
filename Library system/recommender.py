from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def recommend_books(books, selected_book):
    descriptions = [book.description for book in books]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(descriptions)

    similarity = cosine_similarity(tfidf_matrix)

    selected_index = books.index(selected_book)
    scores = similarity[selected_index]

    recommendations = []

    for index, score in enumerate(scores):
        if index != selected_index:
            recommendations.append((books[index], score))

    recommendations.sort(key=lambda x: x[1], reverse=True)

    return recommendations[:3]