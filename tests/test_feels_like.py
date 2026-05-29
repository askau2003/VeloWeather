import numpy as np
from velo_weather.backend.weather import feels_like


def test_mere_vind_føles_koldere():
    assert feels_like(-5.0, 40.0) < feels_like(-5.0, 10.0)