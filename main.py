#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@FileName  : main.py
@FilePath  : main.py
@Time      : 2025/12/19 17:18
@Author    : Wang-MieMie
"""


from pathlib import Path
from typing import Dict, List, Sequence

from operate_yaml import load_yaml, save_yaml
from proxy_group import create_select_pg, create_url_test_pg

base_config_path = Path('config/base-config.yaml')
proxy_providers_path = Path('config/proxy-providers.yaml')
app_rule_providers_path = Path('config/appRuleProviders.yaml')
general_rule_providers_path = Path('config/generalRuleProviders.yaml')

group_maps_path = Path('config/group-maps.yaml')


def build_proxy_select_pg(name: str, proxy_name_list):
    return create_select_pg(name, proxy_name_list=proxy_name_list)


def build_independent_node_pg(provider_name_list):
    return create_select_pg('独立节点', provider_name_list=provider_name_list)


def build_location_pg(name: str, map_name: Sequence[str], flag: str, provider_name_list):
    filter_ = f'''(?i)({'|'.join(map_name)})'''
    return create_url_test_pg(f'{flag}|-最优路线-|{name}', provider_name_list=provider_name_list, filter_=filter_)


def main():
    cfg = {}

    base_config = load_yaml(base_config_path)
    proxy_providers = load_yaml(proxy_providers_path)
    app_rule_providers = load_yaml(app_rule_providers_path)
    general_rule_providers = load_yaml(general_rule_providers_path)

    cfg.update(base_config)
    cfg['proxy-providers'] = proxy_providers

    all_rule_providers: Dict = app_rule_providers | general_rule_providers
    cfg['rule-providers'] = all_rule_providers

    # proxy-groups make
    proxy_provider_names = [k for k in proxy_providers.keys()]
    independent_node_pg = build_independent_node_pg(proxy_provider_names)

    location_pg = []
    group_data: Dict = load_yaml(group_maps_path)

    use_group: List[str] = group_data['use_group']
    group_maps: Dict = group_data['group_maps']
    group_flags: Dict = group_data['flag_emojis']

    for name in use_group:
        map_name = group_maps[name]
        flag = group_flags[name]
        pg = build_location_pg(name, map_name, flag, proxy_provider_names)
        location_pg.append(pg)

    location_pg_names = [v['name'] for v in location_pg]

    proxy_select_proxy_name = [independent_node_pg['name']] + location_pg_names + ['DIRECT', 'REJECT']

    proxy_select_gp = build_proxy_select_pg('代理选择', proxy_select_proxy_name)

    for_rule_gp = ['代理选择'] + proxy_select_proxy_name
    rule_providers_gp = [build_proxy_select_pg(name, for_rule_gp) for name in app_rule_providers.keys()]

    all_gp = [proxy_select_gp, independent_node_pg]
    all_gp = all_gp + location_pg + rule_providers_gp
    cfg['proxy-groups'] = all_gp

    # rule make
    rule_providers_gp_rule = [f'RULE-SET,{gp['name']},{gp['name']}' for gp in rule_providers_gp]

    general_rule_providers_rules = [
        'RULE-SET,reject,REJECT',
        'RULE-SET,private,DIRECT',
        'RULE-SET,direct,DIRECT',
        'RULE-SET,lancidr,DIRECT',
        'RULE-SET,cncidr,DIRECT',
    ]

    rules = rule_providers_gp_rule + general_rule_providers_rules + ['GEOIP,CN,DIRECT,no-resolve', 'MATCH,代理选择']
    cfg['rules'] = rules
    cfg['converted'] = True

    save_yaml('./output/config.yaml', cfg)


if __name__ == '__main__':
    main()
