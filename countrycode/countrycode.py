import re
import os
import csv
import pandas as pd
from copy import copy

pkg_dir, pkg_filename = os.path.split(__file__)
data_path = os.path.join(pkg_dir, "data", "countrycode_data.csv")
f = csv.reader(open(data_path, 'r'))
data = zip(*f)
data = [(x[0], x[1:]) for x in data]
data = dict(data)

data_path = os.path.join(pkg_dir, "data", "cown2014.csv")
cown = pd.read_csv(data_path)
data_path = os.path.join(pkg_dir, "data", "cowc2014.csv")
cowc = pd.read_csv(data_path)

#data_path = os.path.join(pkg_dir, "data", "states2014.csv")
#states = pd.read_csv(data_path)
#f = lambda x: xrange(x['styear'], x['endyear'] + 1)
#g = lambda x: reduce(lambda z, y: z + y, x)
#def make_frame(years, code='AFG', codename='cowc'):
    #years = list(set(sum(years, [])))
    #out = pd.DataFrame(years, columns=['year'])
    #out[codename] = code
    #return out
#cowc = []
#cown = []
#for c in states.stateabb.unique():
    #tmp = states[states.stateabb==c]
    #tmp = tmp.apply(f, axis=1).tolist()
    #tmp = [list(x) for x in tmp]
    #tmp = make_frame(tmp, code=c, codename='cowc')
    #cowc.append(tmp)
#for c in states.ccode.unique():
    #tmp = states[states.ccode==c]
    #tmp = tmp.apply(f, axis=1).tolist()
    #tmp = [list(x) for x in tmp]
    #tmp = make_frame(tmp, code=c, codename='cown')
    #cown.append(tmp)
#cowc = pd.concat(cowc, ignore_index=True)
#cown = pd.concat(cown, ignore_index=False)


def countryyear(code='iso3c', years=range(1990,2013)):
    if not years:
        if code == 'cown':
            out = cown
        else:
            out = cowc
    else:
        codes = data[code]
        out = pd.DataFrame(zip(range(len(codes)), codes), columns=['idx', code])
        out[code][out[code]==''] = None
        out = out.dropna()
        out = [out.copy() for x in years]
        for i,v in enumerate(years):
            out[i]['year'] = v
        out = reduce(lambda x,y: pd.concat([x,y]), out)
    return out

def countrycode(codes=['DZA', 'CAN'], origin='iso3c', target='country_name', dictionary=False):
    '''Convert to and from 11 country code schemes. Use regular expressions to
    detect country names and standardize them. Assign region/continent
    descriptors.

    Parameters
    ----------

    codes : string or list of strings
        country names or country codes to convert
    origin : string
        name of the coding scheme of origin
    target : string
        name of the coding scheme you wish to obtain

    Notes
    -----

    Valid origin codes:

        * country_name
        * iso2c : ISO 2 character
        * iso3c : ISO 3 character
        * iso3n : ISO 3 numeric
        * cown : Correlates of War numeric
        * cowc : Correlates of War character
        * un : United Nations
        * wb : World Bank
        * imf : International Monetary Fund
        * fips104 : FIPS 10-4 U.S. government geographic data
        * fao : Food & Agriculture Organization of the U.N.

    Valid target codes:

        * Any valid origin code
        * region : World Bank geographic region descriptor
        * continent : Name of continent
    '''

    if dictionary:
        in_codes = pd.Series(codes).unique()
        out_codes = _convert(in_codes, origin, target)
        out = pd.DataFrame(zip(in_codes, out_codes), columns=[origin, target])
        out = out.dropna()
    else:
        out = _convert(codes, origin, target)
    return out

def _convert(codes, origin, target):
    '''Internal conversion function'''

    # Codes to be converted (cleanup)
    if type(codes) in [str, unicode, int]:
        codes = [codes]
        loner = True
    else:
        loner = False

    try:
        codes = ["%.0f" % x for x in codes]
    except:
        codes = [str(x).strip() for x in codes]

    # Dictionary
    target_codes = data[target]

    if origin == 'country_name':
        origin_codes = ['(?i)' + x for x in data['regex']]
    else:
        origin_codes = data[origin]

    #idx = [True if (v not in ['NA','']) and (origin_codes[i] not in ['NA','']) else False
    idx = [True if (v != '') and (origin_codes[i] != '') else False
           for i,v in enumerate(target_codes)]

    origin_codes = [v for i,v in enumerate(origin_codes) if idx[i]]
    target_codes = [v for i,v in enumerate(target_codes) if idx[i]]

    dictionary = dict(zip(origin_codes, target_codes))

    if origin != 'country_name':
        codes_new = ["None" if x not in origin_codes else x for x in codes]
    else:
        codes_new = copy(codes)

    for k in dictionary.keys():
        codes_new = [dictionary[k] if re.match('^'+k+'$', x) != None else x
                     for x in codes_new]

    # Output
    codes_new = [None if x=='None' else x for x in codes_new]

    if loner:
        codes_new = codes_new[0]

    return codes_new
