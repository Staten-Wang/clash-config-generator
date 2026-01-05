#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@FileName  : proxy_provider.py
@FilePath  : proxy_provider.py
@Time      : 2026/01/05 18:02
@Author    : Wang-MieMie
"""


from typing import Any, Dict


def organize_proxy_providers(d: Dict[str, Any]) -> Dict:
    for k in list(d.keys()):
        if k.startswith('_'):
            d.pop(k)
    return d
