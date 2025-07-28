import nltk
from nltk.corpus import stopwords, wordnet
import re

nltk.data.path.append("./nltk_data")
stop_words = set(stopwords.words("english"))

def normalize_text(text):
    text = text.encode("ascii", "ignore").decode()  # remove non-ASCII
    text = re.sub(r"[^\w\s.,;:?!-]", "", text)  # keep only words and punctuation
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_context(job_text, persona):
    """
    Extract actions, keywords, boost terms, and avoid terms dynamically.
    """
    full_text = (job_text + " " + persona).lower()
    tokens = nltk.word_tokenize(full_text)
    tags = nltk.pos_tag(tokens)

    # Actions
    actions = []
    for i in range(len(tags) - 1):
        if tags[i][1].startswith("VB"):
            phrase = tags[i][0]
            if tags[i+1][1].startswith("NN"):
                phrase += " " + tags[i+1][0]
            actions.append(phrase)

    # Keywords
    keywords = [w for (w, t) in tags if (t.startswith("NN") or t.startswith("JJ")) and w not in stop_words]

    # Boost terms
    boost_terms = set(actions + keywords)

    # Avoid terms using antonyms
    avoid_terms = set()
    for word in keywords:
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                for antonym in lemma.antonyms():
                    avoid_terms.add(antonym.name().lower())

    return list(set(actions)), list(set(keywords)), list(boost_terms), list(avoid_terms)

def summarize_content(text, boost_terms):
    text = normalize_text(text)``
    if not text.strip():
        return "No relevant content."
    sentences = nltk.sent_tokenize(text)
    scored = []
    for s in sentences:
        score = sum(1 for term in boost_terms if term in s.lower())
        scored.append((score, s.strip()))
    scored.sort(reverse=True)
    top_sentences = [s for _, s in scored[:3]]
    return " ".join(top_sentences) if top_sentences else text
