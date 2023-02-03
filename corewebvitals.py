#!/usr/bin/env python
import requests
import json
from databox import Client

def query_psi(url, key, strategy="desktop"):
    # request core web vitals from PageSpeed API
    r = requests.get("https://www.googleapis.com/pagespeedonline/v5/runPagespeed" \
                 + "?strategy=" +strategy \
                 + "&category=PERFORMANCE" \
                 + "&category=ACCESSIBILITY" \
                 + "&category=SEO" \
                 + "&category=BEST_PRACTICES" \
                 + "&url=" +url \
                 + "&key=" +key)

    psi_data = json.loads(r.text)
    print(str(r.status_code) + ' {}-{}'.format(url, strategy))

    return psi_data

plataform = ['desktop', 'mobile']
databox_desktop_token = ""  # Databox key
databox_mobile_token = ""
psi_key = ""  # PageSpeed Insights API key
urls = ['https://databox.com', 'https://app.intercom.com']

#parse over the desktop and mobile strategy options
for x in range(0,2):
    # initilize databox client for either one
    if x == 0:
        client = Client(databox_desktop_token)
    else:
        client = Client(databox_mobile_token)

    #query PageSpeedInsight
    for y in range(0, len(urls)):
        report = query_psi(urls[y], psi_key, plataform[x])

        # defining metrics
        final_url = report['lighthouseResult']['finalUrl']
        fetch_time = report['analysisUTCTimestamp'][0:10]  # date format %Y-$m-$d
        form_factor = report['lighthouseResult']['configSettings']['formFactor']
        seo_score = report["lighthouseResult"]["categories"]["seo"]["score"]
        performance_score = report["lighthouseResult"]["categories"]["performance"]["score"]
        accessibility_score = report["lighthouseResult"]["categories"]["accessibility"]["score"]
        best_practices_score = report["lighthouseResult"]["categories"]["best-practices"]["score"]
        speed_index = report["lighthouseResult"]["audits"]["speed-index"]["score"]
        time_to_interactive = report["lighthouseResult"]["audits"]["interactive"]["score"]
        total_blocking_time = report["lighthouseResult"]["audits"]["total-blocking-time"]["score"]
        # percentile
        largest_contentful_paint = report['loadingExperience']['metrics']['LARGEST_CONTENTFUL_PAINT_MS']['percentile']
        first_contentful_paint = report['loadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['percentile']
        cumulative_layout_shift = report['loadingExperience']['metrics']['CUMULATIVE_LAYOUT_SHIFT_SCORE']['percentile']
        # distributions
        largest_contentful_paint_dist = report['loadingExperience']['metrics']['LARGEST_CONTENTFUL_PAINT_MS']['distributions']
        first_contentful_paint_dist = report['loadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['distributions']
        first_input_delay_dist = report['loadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']['distributions']
        cumulative_layout_shift_dist = report['loadingExperience']['metrics']['CUMULATIVE_LAYOUT_SHIFT_SCORE']['distributions']

        # Send psi data to databox, value key is limited to 6 decimal places
        client.insert_all([
            {'key': 'seo_score', 'value': seo_score, 'date': fetch_time, 'attributes': {'url': urls[y]}},  # seo_score
            {'key': 'speed_index', 'value': speed_index, 'date': fetch_time, 'attributes': {'url': urls[y]}},  # speed_index
            {'key': 'performance_score', 'value': performance_score, 'date': fetch_time, 'attributes': {'url': urls[y]}},  # performance_score
            {'key': 'time_to_interactive', 'value': time_to_interactive, 'date': fetch_time, 'attributes': {'url': urls[y]}},  # time_to_interactive
            {'key': 'total_blocking_time', 'value': total_blocking_time, 'date': fetch_time, 'attributes': {'url': urls[y]}},  # total_blocking_time
            {'key': 'accessibility_score', 'value': accessibility_score, 'date': fetch_time, 'attributes': {'url': urls[y]}},  # accessibility_score
            {'key': 'best_practices_score', 'value': best_practices_score, 'date': fetch_time, 'attributes': {'url': urls[y]}},  # best_practices_score
            # percentile
            {'key': 'largest_contentful_paint', 'value': largest_contentful_paint, 'date': fetch_time, 'attributes': {'url': urls[y]}},
            # largest_contentful_paint
            {'key': 'first_contentful_paint', 'value': first_contentful_paint, 'date': fetch_time, 'attributes': {'url': urls[y]}},  # first_contentful_paint
            {'key': 'cumulative_layout_shift', 'value': total_blocking_time, 'date': fetch_time, 'attributes': {'url': urls[y]}},  # cumulative_layout_shift
            # distributions
            # largest_contentful_paint_dist
            {'key': 'largest_contentful_paint_dist', 'value': round(largest_contentful_paint_dist[0]['proportion'], 4),
             'date': fetch_time,
             'attributes': {'distribution': 'good - {url}'.format(url=urls[y])}},
            {'key': 'largest_contentful_paint_dist', 'value': round(largest_contentful_paint_dist[1]['proportion'], 4),
             'date': fetch_time,
             'attributes': {'distribution': 'need improvement - {url}'.format(url=urls[y])}},
            {'key': 'largest_contentful_paint_dist', 'value': round(largest_contentful_paint_dist[2]['proportion'], 4),
             'date': fetch_time,
             'attributes': {'distribution': 'poor - {url}'.format(url=urls[y])}},
            # first_contentful_paint_dist
            {'key': 'first_contentful_paint_dist', 'value': round(first_contentful_paint_dist[0]['proportion'], 4),
             'date': fetch_time,
             'attributes': {'distribution': 'good - {url}'.format(url=urls[y])}},
            {'key': 'first_contentful_paint_dist', 'value': round(first_contentful_paint_dist[1]['proportion'], 4),
             'date': fetch_time,
             'attributes': {'distribution': 'need improvement - {url}'.format(url=urls[y])}},
            {'key': 'first_contentful_paint_dist', 'value': round(first_contentful_paint_dist[2]['proportion'], 4),
             'date': fetch_time,
             'attributes': {'distribution': 'poor - {url}'.format(url=urls[y])}},
            # first_input_delay_dist
            {'key': 'first_input_delay_dist', 'value': round(first_input_delay_dist[0]['proportion'], 4),
             'date': fetch_time,
             'attributes': {'distribution': 'good - {url}'.format(url=urls[y])}},
            {'key': 'first_input_delay_dist', 'value': round(first_input_delay_dist[1]['proportion'], 4),
             'date': fetch_time,
             'attributes': {'distribution': 'need improvement - {url}'.format(url=urls[y])}},
            {'key': 'first_input_delay_dist', 'value': round(first_input_delay_dist[2]['proportion'], 4),
             'date': fetch_time,
             'attributes': {'distribution': 'poor - {url}'.format(url=urls[y])}},
            # cumulative_layout_shift_dist
            {'key': 'cumulative_layout_shift_dist', 'value': round(cumulative_layout_shift_dist[0]['proportion'], 4),
             'date': fetch_time,
             'attributes': {'distribution': 'good - {url}'.format(url=urls[y])}},
            {'key': 'cumulative_layout_shift_dist', 'value': round(cumulative_layout_shift_dist[1]['proportion'], 4),
             'date': fetch_time,
             'attributes': {'distribution': 'need improvement - {url}'.format(url=urls[y])}},
            {'key': 'cumulative_layout_shift_dist', 'value': round(cumulative_layout_shift_dist[2]['proportion'], 4),
             'date': fetch_time,
             'attributes': {'distribution': 'poor - {url}'.format(url=urls[y])}},
        ])
