#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@FileName  : proxy_group.py
@FilePath  : proxy_group.py
@Time      : 2025/12/19 16:57
@Author    : Wang-MieMie
"""


def create_select_pg(name,
                     proxy_name_list=None,
                     provider_name_list=None,
                     filter_=None,
                     interval=30,
                     tolerance=100,
                     timeout=1000,
                     lazy=True,
                     url='https://www.gstatic.com/generate_204',
                     max_failed_times: int = 5):
    return create_proxy_group(name, 'select', proxy_name_list, provider_name_list,
                              filter_, interval, tolerance, timeout, lazy, url, max_failed_times)


def create_url_test_pg(name,
                       proxy_name_list=None,
                       provider_name_list=None,
                       filter_=None,
                       interval=30,
                       tolerance=100,
                       timeout=1000,
                       lazy=True,
                       url='https://www.gstatic.com/generate_204',
                       max_failed_times: int = 2):
    return create_proxy_group(name, 'url-test', proxy_name_list, provider_name_list,
                              filter_, interval, tolerance, timeout, lazy, url, max_failed_times)


#

def create_proxy_group(name,
                       type: str,
                       proxy_name_list=None,
                       provider_name_list=None,
                       filter_=None,
                       interval=30,
                       tolerance=100,
                       timeout=1000,
                       lazy=True,
                       url='https://www.gstatic.com/generate_204',
                       max_failed_times: int = 5):
    cfg = {
        'name': name,
        'type': type,
        'url': url,
        'interval': interval,
        'tolerance': tolerance,
        'lazy': lazy,
        'timeout': timeout,
        'max-failed-times': max_failed_times,
    }
    if proxy_name_list is None and provider_name_list is None:
        raise
    if proxy_name_list is not None:
        cfg['proxies'] = proxy_name_list
    if provider_name_list is not None:
        cfg['use'] = provider_name_list

    if filter_:
        cfg['filter'] = filter_

    return cfg
