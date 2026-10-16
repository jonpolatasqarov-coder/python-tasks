
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def recommend_books(books, selected_book):
    if len(books) < 2:
        return []

    texts = []

    for book in books:
        description = getattr(book, "description", "") or ""

        text = f"{book.title} {description}"
        texts.append(text)

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    matrix = vectorizer.fit_transform(texts)
    similarities = cosine_similarity(matrix)

    selected_index = next(
        (
            i for i, book in enumerate(books)
            if book.book_id == selected_book.book_id
        ),
        None
    )

    if selected_index is None:
        return []

    recommendations = []

    for i, book in enumerate(books):
        if i == selected_index:
            continue

        score = similarities[selected_index][i]

        if score > 0:
            recommendations.append((book, float(score)))

    recommendations.sort(
        key=lambda item: item[1],
        reverse=True
    )

    return recommendations[:3]
