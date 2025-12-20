#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@FileName  : operate_yaml.py
@FilePath  : operate_yaml.py
@Time      : 2025/12/19 16:54
@Author    : Wang-MieMie
"""

from pathlib import Path

import yaml


def load_yaml(p: Path):
    with open(p, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data


def save_yaml(p: Path, data):
    with open(p, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)
