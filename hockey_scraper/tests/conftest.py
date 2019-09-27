#!/usr/bin/python

import pytest
from hockey_scraper import nhl
import mock_nhl


@pytest.fixture
def nhl_scraper():
    s = nhl.Scraper()
    # Put the mock adapter in so we don't make calls out
    s.set_endpoint_adapter(mock_nhl.EndpointAdapter())
    yield s
