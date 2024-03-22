def test_get_top_artists_valid(quizzify_test_app):
    # Test case for successful response
    response = quizzify_test_app.post(
        url="/artists/top",
        json={"time_range": "short_term", "limit": 5},
        headers={"user-id": "example_user_id"},
    )
    print(response.json())
    assert response.json() == 200
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 5


def test_get_top_artists_invalid_limit(quizzify_test_app):
    # Test case for invalid limit exceeding 50
    response = quizzify_test_app.post(
        url="/artists/top",
        json={"time_range": "short_term", "limit": 51},
        headers={"user_id": "example_user_id"},
    )
    # Unprocessable Entity
    assert response.status_code == 422


# def test_get_random_artist(quizzify_test_app):
#     # Test case for successful response
#     response = quizzify_test_app.get("/artists/random")
#     assert response.status_code == 200
#     # Assuming service returns a single artist
#     assert isinstance(response.json(), dict)
