# Clash.Meta 规则聚合生成器

一个基于 Python 的 Clash.Meta 配置文件生成工具，用于自动聚合多个代理提供者并生成完整的 Clash.Meta 配置文件。

## 项目简介

本项目可以根据您的配置自动生成完整的 Clash.Meta 配置文件，支持：

- 多个代理提供者聚合
- 自动地区分组
- 规则提供者管理
- 自定义分组策略

## 环境要求

- Python 3.6+
- PyYAML 库

## 安装依赖

```bash
pip install pyyaml
```

## 使用方法

### 1. 配置代理提供者

编辑 `config/proxy-providers.yaml` 文件，填写您的代理提供者配置：

```yaml
provider1:
  type: http
  url: "https://your-provider-url.com/subscription.yaml"
  interval: 3600
  path: ./providers/provider1.yaml
  health-check:
    enable: true
    url: "https://www.gstatic.com/generate_204"
    interval: 300
  override:
    additional-prefix: "provider1"
```

### 2. 配置分组（可选）

编辑 `config/group-maps.yaml` 文件，通过修改 `use_group` 列表来控制生成哪些分组：

```yaml
use_group:
  - 香港
  - 美国
  - 日本
  - 新加坡
  # 添加或删除您需要的组别
```

### 3. 生成配置文件

运行生成脚本：

```bash
python main.py
```

### 4. 获取配置文件

生成的完整配置文件位于：`output/config.yaml`

将此文件用于 Clash.Meta 客户端即可使用。

## 配置文件说明

### 目录结构

```text
ProxyPy/
├── config/                          # 配置文件目录
│   ├── proxy-providers.yaml         # 代理提供者配置
│   ├── generalRuleProviders.yaml    # 常规规则提供者配置
│   ├── appRuleProviders.yaml        # 应用规则提供者配置
│   ├── group-maps.yaml              # 分组映射配置
│   └── base-config.yaml             # 基础配置
├── output/                          # 输出目录
│   └── config.yaml                  # 生成的完整配置文件
├── main.py                          # 主程序
├── operate_yaml.py                  # YAML 操作工具
├── proxy_group.py                   # 代理分组工具
└── README.md                        # 项目说明文档
```

### 配置文件详解

#### proxy-providers.yaml

存储代理提供者的订阅链接和相关配置。每个提供者包含：

- `type`: 提供者类型（http）
- `url`: 订阅地址
- `interval`: 更新间隔（秒）
- `path`: 本地缓存路径
- `health-check`: 健康检查配置
- `override`: 覆盖配置（如节点前缀）

#### group-maps.yaml

控制分组和节点匹配规则：

- `use_group`: 指定要生成的分组列表
- `group_maps`: 定义每个分组的关键词匹配规则
- `flag_emojis`: 分组对应旗帜的表情符号

#### generalRuleProviders.yaml

常规规则提供者配置，如 GFW、广告拦截、直连等规则。

#### appRuleProviders.yaml

应用专属规则提供者配置，如 Google、OpenAI、Microsoft 等应用的规则。

#### base-config.yaml

Clash.Meta 的基础配置，包括端口、模式、日志级别、GeoIP 等设置。

## 生成的配置特性

生成的 `output/config.yaml` 包含：

1. **独立节点分组** - 包含所有代理提供者的节点
2. **地点分组** - 根据 `use_group` 自动生成分组（使用 url-test 策略）
3. **规则分组** - 为每个规则提供者生成对应的分组
4. **代理选择** - 主选择入口，包含所有分组和默认策略
5. **直连分组** - 用于直连的流量
6. **拦截分组** - 用于拦截的流量
7. **自动规则** - 根据规则提供者自动生成路由规则

## 注意事项

- 请确保所有订阅链接有效且可访问
- 生成配置前请检查各个 YAML 文件的格式正确性
- 建议定期更新规则提供者的 URL
- 生成的配置文件请根据实际需求进行微调

## 许可证

本项目仅供学习和个人使用。

## 作者

Wang-MieMie

## 更新日志

### v1.0.0 (2025-12-20)

- 初始版本发布
- 支持多代理提供者聚合
- 支持自动地点分组
- 支持规则提供者管理
