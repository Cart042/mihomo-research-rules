# Mihomo Research Direct Rules / 科研网站直连规则集

> 为 `3x-ui` 生成的 Clash/Mihomo 订阅与 FlClash 等 mihomo 客户端准备的 **科研网站路由规则**。这是路由清单，不是 VPN 服务，也不能赋予付费论文访问权限。

## 内容

- `rules/Research.yaml`：综合科研直连候选规则，**431** 个去重域名，`behavior: classical`、`format: yaml`。
- `rules/Research-Institutions-Optional.yaml`：**63** 个可选大学、科研机构与公共机构域名，默认不启用（匹配整个学校域名可能涉及其他流量）。
- `3xui-global-routing-INLINE.yaml`：**现在就可用**。将整个文件复制至 3x-ui → 面板设置 → 订阅设置 → Clash/Mihomo → 全局路由规则，保存后刷新 FlClash 订阅。保留原 Loyalsoldier 13 组及 `proxy: DIRECT`。
- `3xui-global-routing-REMOTE.yaml`：等此项目按**公开仓库**发布至 `Cart042/mihomo-research-rules` 后使用；含单独的 `Research` 规则提供者、更新周期 86400、`proxy: DIRECT`。
- `scripts/validate.py`：标准库验证重复、格式及引用（额外检查 YAML 推荐安装 PyYAML）。

## 仓库发布状态

仓库已发布至 `Cart042/mihomo-research-rules`，主分支为 `main`。规则集下载地址：

`https://raw.githubusercontent.com/Cart042/mihomo-research-rules/main/rules/Research.yaml`

如果修改 `rules/Research.yaml`，mihomo 会按配置的 `interval: 86400` 重新拉取更新。

## 单独添加到已有配置（推荐）

在 `rule-providers:` 末尾增加：

```yaml
  Research:
    type: http
    behavior: classical
    format: yaml
    url: "https://raw.githubusercontent.com/Cart042/mihomo-research-rules/main/rules/Research.yaml"
    path: ./ruleset/Research.yaml
    interval: 86400
    proxy: DIRECT
```

再在 `rules:` 中，将 `- RULE-SET,Research,DIRECT` **放在** `- RULE-SET,proxy,PROXY` 和 `- RULE-SET,google,PROXY` 之前，但不要放在 `- RULE-SET,reject,REJECT` 之前，以免覆盖原先的广告拒绝规则。

```yaml
rules:
  - RULE-SET,private,DIRECT
  - RULE-SET,reject,REJECT
  - DOMAIN-SUFFIX,google.com,PROXY
  - DOMAIN-SUFFIX,github.com,PROXY
  - DOMAIN-SUFFIX,researchgate.net,PROXY
  - RULE-SET,Research,DIRECT
  - RULE-SET,google,PROXY
  - RULE-SET,proxy,PROXY
  # ...保留其他原规则
  - MATCH,PROXY
```

## 不纳入科研直连的服务

- **Google Scholar**：不强制直连，Google 域名交给 `PROXY`。
- **Google Colab / Google Drive / GitHub / GitHub Pages**：不强制直连，显式使用 `PROXY`。
- **ResearchGate、Academia.edu、Semantic Scholar、Connected Papers、Litmaps、Dimensions、Scite、OpenReview、Kaggle**：从科研直连核心及可选列表排除，并在完整 3x-ui 配置中优先配置 `PROXY`。
- **非法/不稳定镜像站**：未纳入核心规则，避免误匹配被冒用或更换运营方的域名。
- **科研数据库/期刊认证**：直连仅控制网络路径，机构订阅仍可能要求校园网、学校 VPN、图书馆代理或 SSO 登录。
- **CDN 与跨站资源**：单个网站的页面可能加载其他域名上的字体、文件、登录脚本或 PDF，不能保证访问该站相关的每个请求都走直连。
- `proxy: DIRECT` **仅控制规则文件的下载出口**。如果 `cdn.jsdelivr.net` / `raw.githubusercontent.com` 被 DNS 错误映射至 `127.0.0.1`，仍会失败。

## 策略说明

- 这里的“直连”是用户期望的政策，不表示每个域名已从中国大陆网络逐一验证可达。
- `proxy: DIRECT` 只控制规则集下载；`PROXY` 排除规则控制对网站的访问，两者互不冲突。
- 核心文件主要匹配正规学术服务。为了追求覆盖，部分历史域名、重定向域名也被保留；访问失败请测试后改单条域名的路由。
- 该规则集**不会自行从上游抓取新增域名**。`interval: 86400` 只是让客户端下载仓库里维护后的新版本。
- 项目按域名后缀匹配，故含目标域名的所有子域名；不使用会误伤海量网站的 `.edu`、`.ac.uk` 或任意含 `science` 关键词规则。

## 参考与致谢

- mihomo rule provider 文档：https://wiki.metacubex.one/en/config/rule-providers/
- mihomo provider 文件格式：https://wiki.metacubex.one/en/config/rule-providers/content/
- blackmatrix7 Scholar（检索范围参考；没有直接复制整份规则，且主动排除了 Google Scholar 和不稳定镜像站）：https://github.com/blackmatrix7/ios_rule_script/tree/master/rule/Clash/Scholar
- Loyalsoldier 规则：https://github.com/Loyalsoldier/clash-rules

整理日期：2026-11-16。规则只按公开域名信息整理，包含可能迁移或停用的站点，不能替代实时网络可达性验证。