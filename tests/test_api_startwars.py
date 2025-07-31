from helpers import get_with_ssl

BASE_API = "https://swapi.dev/api/films/"

def test_movies_count():
    resp = get_with_ssl(BASE_API)
    assert resp.status_code == 200
    assert len(resp.json()['results']) == 6

def test_director_of_third_movie():
    resp = get_with_ssl(BASE_API)
    third = resp.json()['results'][2]
    assert third['director'] == "Richard Marquand"

def test_producer_of_fifth_movie_not_certain_names():
    resp = get_with_ssl(BASE_API)
    fifth = resp.json()['results'][4]
    assert fifth['producer'] != "Gary Kurtz, George Lucas"
