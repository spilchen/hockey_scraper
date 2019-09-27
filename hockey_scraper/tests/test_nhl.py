#!/usb/bin/python


def test_teams(nhl_scraper):
    df = nhl_scraper.teams()
    print(df)
    assert(len(df.index) == 31)
    assert(df[df.abbrev == 'TOR'].iloc(0)[0]['name'] == 'Maple Leafs')
    assert(df[df.city == 'San Jose'].iloc(0)[0]['name'] == 'Sharks')
    assert(df[df.city == 'Vegas'].iloc(0)[0]['id'] == 54)
