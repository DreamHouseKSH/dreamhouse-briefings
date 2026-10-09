---
title: 심층 리서치
permalink: /research/
---
# 🔬 심층 리서치

> 뉴스 항목의 **🔍 리서치 요청** 버튼으로 요청된 기사를 깊게 파고든 정리입니다(최신이 위). 요약·분석이며 기사 전문이 아닙니다 — 사실 확인은 각 문서의 출처 목록을 참고하세요. 작성 규칙: [WORKFLOW 8장](../docs/WORKFLOW.md)

{% assign rs = site.pages | where_exp: "p", "p.path contains 'research/'" | sort: "path" | reverse -%}
{%- assign n = 0 -%}
{%- for p in rs -%}{%- if p.path == "research/index.md" -%}{%- continue -%}{%- endif -%}{%- assign n = n | plus: 1 %}
- [{{ p.title | remove: "심층 리서치 — " }}]({{ p.url | relative_url }}) <span class="rl-meta">{{ p.path | remove: "research/" | slice: 0, 10 }}</span>
{%- endfor %}

{% if n == 0 -%}
아직 완료된 리서치가 없습니다. 뉴스 페이지에서 궁금한 기사의 **🔍 리서치 요청** 버튼을 눌러 보세요.
{%- endif %}
