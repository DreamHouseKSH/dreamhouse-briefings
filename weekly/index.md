---
title: 주간 정리·전망
permalink: /weekly/
---

# 📰 주간 정리·전망

> 토요일엔 한 주 브리핑의 흐름·비평 정리, 일요일엔 다음 주 전망을 올립니다(최신이 위). 요약·분석이며 기사 전문이 아닙니다.

{% assign ws = site.pages | where_exp: "p", "p.path contains 'weekly/'" | sort: "path" | reverse -%}
{%- assign n = 0 -%}
{%- for p in ws -%}{%- if p.path == "weekly/index.md" -%}{%- continue -%}{%- endif -%}{%- assign n = n | plus: 1 %}
- [{{ p.title }}]({{ p.url | relative_url }}) <span class="rl-meta">{{ p.path | remove: "weekly/" | slice: 0, 10 }}</span>
{%- endfor %}

{% if n == 0 -%}
아직 주간 정리가 없습니다.
{%- endif %}
