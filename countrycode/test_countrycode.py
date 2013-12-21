from countrycode import countrycode

def test_default():
    assert countrycode() == ['Algeria', 'Canada']

def test_cown_iso3c():
    assert countrycode(codes=['666', '31'], origin='cown', target='iso3c') == ['ISR', 'BHS']

def test_cn_iso3c():
    assert countrycode(['United States', 'India', 'Canada', 'Dem. Repu. Congo'],
            'country_name', 'iso3c') == ['USA', 'IND', 'CAN', 'COD']

def test_iso3c_cn_single():
    assert countrycode('DZA', 'iso3c', 'country_name') == 'Algeria'

def test_unicode():
    assert countrycode(u'DZA', 'iso3c', 'country_name') == 'Algeria'

def test_regex():
    assert countrycode('georgia', 'country_name', 'iso3c') == 'GEO'
    assert countrycode('south georgia', 'country_name', 'iso3c') == 'SGS'
    assert countrycode('serbia', 'country_name', 'iso3c') == 'SRB'
    assert countrycode('serbia and montenegro', 'country_name', 'iso3c') == 'SRB'
    assert countrycode('st. kitts and nevis', 'country_name', 'iso3c') == 'KNA'
    assert countrycode('st. christopher and nevis', 'country_name', 'iso3c') == 'KNA'
    assert countrycode('st. maarten', 'country_name', 'iso3c') == 'SXM'
    assert countrycode('sint maarten', 'country_name', 'iso3c') == 'SXM'
    assert countrycode('saint maarten', 'country_name', 'iso3c') == 'SXM'
    assert countrycode('guinea', 'country_name', 'iso3c') == 'GIN'
    assert countrycode('guinea bissau', 'country_name', 'iso3c') == 'GNB'
    assert countrycode('equatorial guinea', 'country_name', 'iso3c') == 'GNQ'
    assert countrycode('niger', 'country_name', 'iso3c') == 'NER'
    assert countrycode('nigeria', 'country_name', 'iso3c') == 'NGA'
    assert countrycode('west bank', 'country_name', 'iso3c') == 'PSE'
    assert countrycode('south korea', 'country_name', 'iso3c') == 'KOR'
    assert countrycode('korea', 'country_name', 'iso3c') == 'KOR'
    assert countrycode('korea, dem. rep.', 'country_name', 'iso3c') == 'PRK'
    assert countrycode('democ. republic of congo', 'country_name', 'iso3c') == 'COD'
    assert countrycode('republic of congo', 'country_name', 'iso3c') == 'COG'
