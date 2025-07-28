from sklearn.metrics.pairwise import cosine_similarity

def rank_items(items, item_embeddings, query_embeddings, boost_terms, avoid_terms, job_text, model, top_k=5):
    scores = []
    boost_terms = [term.lower() for term in boost_terms]
    avoid_terms = [term.lower() for term in avoid_terms]

    # Encode job_text once for efficiency
    job_embedding = model.encode([job_text], normalize_embeddings=True)[0]

    for idx, item in enumerate(items):
        section_text = (item["title"] + " " + item["content"]).lower()
        title_text = item["title"].lower()

        # 1. Semantic similarity with extracted queries (existing)
        sim_scores_query = [cosine_similarity([q], [item_embeddings[idx]])[0][0] for q in query_embeddings]
        semantic_sim_query = max(sim_scores_query)

        # 2. Job text relevance (new)
        job_sim = cosine_similarity([job_embedding], [item_embeddings[idx]])[0][0]

        # 3. Title relevance
        title_embedding = model.encode([item["title"]], normalize_embeddings=True)[0]
        title_sim_scores = [cosine_similarity([q], [title_embedding])[0][0] for q in query_embeddings]
        title_relevance = max(title_sim_scores)

        # 4. Keyword match score
        keyword_match_score = sum(1 for term in boost_terms if term in section_text) / max(len(boost_terms), 1)

        # 5. Avoid term penalty
        penalty = 0.5 if any(term in section_text for term in avoid_terms) else 0

        # Combine all
        if keyword_match_score == 0:
            final_score = 0
        else:
            final_score = (
                (0.3 * semantic_sim_query) +
                (0.3 * job_sim) +
                (0.2 * title_relevance) +
                (0.2 * keyword_match_score) -
                penalty
            )

        scores.append((item, final_score))

    # Sort by final score
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]
