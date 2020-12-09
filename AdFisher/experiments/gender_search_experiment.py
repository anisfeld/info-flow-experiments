import os
import sys

sys.path.append("../core")  # nopep8

import adfisher                     # adfisher wrapper function
import web.google_ads               # collecting ads

log_file = 'school_b.gender.search.log.txt'
search_terms = ["what major should i study", "degree programs"]


def make_browser(unit_id, treatment_id):
    b = web.google_ads.GoogleAdsUnit(log_file=log_file, unit_id=unit_id,
                                     treatment_id=treatment_id, headless=True, browser="firefox")
    return b

# Control Group treatment (blank)

# Control Group treatment


def control_treatment(unit):
    unit.search_and_click('site_files/mens_search.txt')

# Experimental Group treatment


def exp_treatment(unit):
    unit.search_and_click('site_files/womens_search.txt')

# Measurement - Collects ads
# checks all the sites that adfisher could previously collect on
# (~10 minutes for src and href)


def measurement(unit):
    sites = ['google']
    for site in sites:
        unit.collect_ads(site=site, reloads=2, delay=5,
                         search_terms=search_terms)

# Shuts down the browser once we are done with it.


def cleanup_browser(unit):
    unit.quit()


def load_results():
    pass

# Blank analysis


def test_stat(observed_values, unit_assignments):
    pass


adfisher.do_experiment(make_unit=make_browser, treatments=[control_treatment, exp_treatment],
                       measurement=measurement, end_unit=cleanup_browser,
                       load_results=load_results, test_stat=test_stat, ml_analysis=False,
                       num_blocks=10, num_units=4, timeout=1400,
                       log_file=log_file, exp_flag=True, analysis_flag=False,
                       treatment_names=["A (men's search)", "B (women's search)"])
