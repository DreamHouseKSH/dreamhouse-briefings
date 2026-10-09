---
# Jekyll 이 _data/glossary.yml 을 JSON 으로 넣어 줌 (front matter 필수)
---
/* 줄임말·전문용어 자동 풀이 — 같은 페이지 어디에 나와도 '용어(원어, 쉬운 뜻)'를 본문에 바로 표시
 * 원본: _data/glossary.yml · 규칙: docs/WORKFLOW.md 2-1 · 용어집 페이지: /glossary/
 * - 대상: 뉴스(news/)·GitHub(github/)·리서치(research/) 페이지의 article.prose 본문
 * - 건드리지 않음: 링크 글자(a), 코드(code/pre/kbd/samp), 제목(h1~h3), 버튼, URL 문자열, .no-gloss 안쪽
 * - 중복 방지: 바로 뒤에 이미 '('가 붙어 있거나(본문의 첫 풀이), 몇 글자 안에 원어가 든 괄호가 있거나,
 *   '강화학습(RL, …)'처럼 이미 괄호 풀이 안의 줄임말이면 새로 달지 않음
 * - '에너지부(DOE)'·'누락(CWE-770)'처럼 괄호 안에 줄임말만 있으면 괄호 안에 이어 붙임 → '(DOE, Department of Energy, 미국 에너지부)'
 * - 'HBM(고대역폭 메모리)'처럼 우리말 뜻만 있고 원어가 빠진 기존 괄호는 괄호 맨 앞에 원어만 끼움
 *   → 'HBM(High Bandwidth Memory, 고대역폭 메모리)' (괄호 안이 한글이고 숫자가 없을 때만)
 * - 단어 경계·대소문자 구분: 'API'는 맞추고 'rapid'·'LightOnOCR'는 안 맞춤(HBM4처럼 세대 숫자는 prefix 항목만)
 * - 툴팁이 아니라 본문 글자(작고 연한 .gl-x)라서 아이패드·모바일에서도 그대로 보임
 */
(function () {
  "use strict";
  var DATA = {{ site.data.glossary | jsonify }};
  window.DH_GLOSSARY = DATA;
  if (!Array.isArray(DATA) || !DATA.length) return;

  var baseMeta = document.querySelector('meta[name="site-base"]');
  var BASE = baseMeta ? baseMeta.getAttribute("content") : "/";
  var rel = location.pathname.indexOf(BASE) === 0 ? location.pathname.slice(BASE.length) : location.pathname.replace(/^\//, "");
  try { rel = decodeURIComponent(rel); } catch (e) {}
  if (!/^(news|github|research)\//.test(rel)) return;
  var prose = document.querySelector("article.prose");
  if (!prose) return;

  var t0 = (window.performance && performance.now) ? performance.now() : Date.now();
  var map = Object.create(null), alts = [];
  var esc = function (s) { return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); };
  DATA.forEach(function (g) {
    if (!g || !g.term || g.inline === false) return;
    map[g.term] = g;
    alts.push({ t: g.term, re: esc(g.term).replace(/ /g, "\\s") + (g.prefix ? "(?:\\d[A-Za-z0-9]*)?" : "") });
  });
  if (!alts.length) return;
  alts.sort(function (a, b) { return b.t.length - a.t.length; });
  // (앞 경계)(용어[+세대 표기])(-숫자 꼬리: CVE-2026-1234) + 뒤 경계
  var RE = new RegExp("(^|[^A-Za-z0-9_\\-.])(" + alts.map(function (a) { return a.re; }).join("|") + ")((?:-\\d[A-Za-z0-9]*)*)(?![A-Za-z0-9_])", "g");
  var QUICK = new RegExp(alts.map(function (a) { return a.re; }).join("|"));
  var URLRE = /(?:https?:\/\/|www\.)\S+|\b[\w-]+(?:\.[\w-]+)+\/\S*/g;
  var lookup = function (s) { return map[s] || map[s.replace(/\s/g, " ")] || map[s.replace(/\d[A-Za-z0-9]*$/, "")]; };

  var SKIP = { A: 1, CODE: 1, PRE: 1, KBD: 1, SAMP: 1, H1: 1, H2: 1, H3: 1, BUTTON: 1, SCRIPT: 1, STYLE: 1, TEXTAREA: 1, SELECT: 1, OPTION: 1, SVG: 1, TITLE: 1 };
  var skippable = function (el) {
    for (; el && el !== prose; el = el.parentNode) {
      if (el.nodeType !== 1) continue;
      if (SKIP[el.nodeName.toUpperCase()]) return true;
      if (el.classList && (el.classList.contains("gl-x") || el.classList.contains("no-gloss") || el.classList.contains("research-btn"))) return true;
      if (el.getAttribute && el.getAttribute("role") === "button") return true;
    }
    return false;
  };

  // 모든 텍스트 노드(앞뒤 문맥 확인용) + 처리 대상 표시
  var nodes = [], ok = [];
  var w = document.createTreeWalker(prose, 4 /* SHOW_TEXT */, null, false), n;
  while ((n = w.nextNode())) { nodes.push(n); ok.push(QUICK.test(n.nodeValue) && !skippable(n.parentNode)); }

  var afterText = function (i, s) {
    for (var k = i + 1; s.length < 40 && k < nodes.length; k++) s += nodes[k].nodeValue;
    return s;
  };
  var beforeText = function (i, s) {
    for (var k = i - 1; s.length < 2 && k >= 0; k--) s = nodes[k].nodeValue + s;
    return s;
  };
  // 이미 풀이가 붙어 있으면 'skip', 우리말 뜻만 있고 원어가 없으면 'merge'(괄호 안 맨 앞에 원어만 끼움)
  var HANGUL = /[\uac00-\ud7a3]/;
  var explained = function (g, before, after) {
    var full = (g.full || "").toLowerCase().slice(0, 12);
    if (/^[(（]/.test(after)) {                                                       // 'GA(General …)' 본문 첫 풀이
      var c0 = (/^[(（]([^)）]*)/.exec(after) || ["", ""])[1];
      if (full && c0.toLowerCase().indexOf(full) < 0 && HANGUL.test(c0) && !/\d/.test(c0)) return "merge"; // 'HBM(고대역폭 메모리)'
      return "skip";
    }
    if (/\S[(（]$/.test(before) && /^[,，]/.test(after)) return "skip";               // '강화학습(RL, 보상 …)'
    if (/\S[(（]$/.test(before) && /^[)）]/.test(after)) return "inside";             // '에너지부(DOE)' → '(DOE, 원어, 뜻)'
    var m = /^[^()\n]{0,10}[(（]([^)）]*)/.exec(after);                                // 'E2E 테스트(end-to-end, …)'
    if (m && full && m[1].toLowerCase().indexOf(full) >= 0) return "skip";
    return "";
  };
  var span = function (g, text, extra) {
    var sp = document.createElement("span");
    sp.className = "gl-x" + (extra ? " " + extra : "");
    sp.setAttribute("data-term", g.term);
    sp.textContent = text;
    return sp;
  };

  var count = 0, merged = 0, carry = {};                 // carry[i] = 다음 텍스트 노드 맨 앞 '(' 뒤에 끼울 것
  nodes.forEach(function (node, i) {
    var s = node.nodeValue, ins = carry[i] ? carry[i].slice() : [];
    if (ok[i]) {
      var urls = [], u;
      URLRE.lastIndex = 0;
      while ((u = URLRE.exec(s))) urls.push([u.index, u.index + u[0].length]);
      RE.lastIndex = 0;
      var m;
      while ((m = RE.exec(s))) {
        var start = m.index + m[1].length, end = start + m[2].length + m[3].length;
        RE.lastIndex = end;                               // 겹치는 다음 경계 허용
        var g = lookup(m[2]);
        if (!g) continue;
        if (urls.some(function (r) { return start < r[1] && end > r[0]; })) continue;
        var tail = s.slice(end), how = explained(g, beforeText(i, s.slice(0, start)), afterText(i, tail));
        if (how === "skip") continue;
        if (how === "merge") {
          var at = /^[(（]/.test(tail) ? { k: i, pos: end + 1 } : null;
          if (!at && tail === "" && i + 1 < nodes.length && /^[(（]/.test(nodes[i + 1].nodeValue) && !skippable(nodes[i + 1].parentNode)) at = { k: i + 1, pos: 1 };
          if (!at) continue;
          var item = { pos: at.pos, el: span(g, g.full + ", ", "gl-in") };
          if (at.k === i) ins.push(item); else (carry[at.k] = carry[at.k] || []).push(item);
          merged++;
          continue;
        }
        if (how === "inside") ins.push({ pos: end, el: span(g, ", " + (g.full ? g.full + ", " : "") + g.ko, "gl-in") });
        else ins.push({ pos: end, el: span(g, "(" + (g.full ? g.full + ", " : "") + g.ko + ")") });
        count++;
      }
    }
    if (!ins.length) return;
    ins.sort(function (a, b) { return a.pos - b.pos; });
    var frag = document.createDocumentFragment(), last = 0;
    ins.forEach(function (x) { frag.appendChild(document.createTextNode(s.slice(last, x.pos))); frag.appendChild(x.el); last = x.pos; });
    frag.appendChild(document.createTextNode(s.slice(last)));
    node.parentNode.replaceChild(frag, node);
  });
  var t1 = (window.performance && performance.now) ? performance.now() : Date.now();
  window.DH_GLOSSARY_STATS = { terms: alts.length, annotated: count, merged: merged, ms: Math.round((t1 - t0) * 10) / 10 };
})();
