from sklearn.metrics.pairwise import cosine_similarity


def get_similarity(
    user_vector,
    locality_vector,
):
    return float(
        cosine_similarity(
            [user_vector],
            [locality_vector],
        )[0][0]
    )
