(function () {
  "use strict";
  var root = document.documentElement;

  // 1) 다크/라이트 전환 (시스템 설정 기본, 선택 시 localStorage 저장)
  var btn = document.querySelector(".theme-toggle");
  if (btn) {
    btn.addEventListener("click", function () {
      var cur = root.getAttribute("data-theme");
      if (!cur) cur = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
      var next = cur === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("theme", next); } catch (e) {}
    });
  }


  // 1-1) 새 빌드 자동 반영 (iPad 홈 화면 웹앱 등 standalone에서 오래된 화면이 남는 문제)
  //   페이지의 <meta name="site-build"> 와 /version.json(no-store)을 비교해 다르면 다시 불러옴.
  //   무한 새로고침 방지: 같은 목표 버전으로는 5분에 1회만 자동 새로고침 + 최소 30초 간격(sessionStorage 가드).
  //   서비스워커 없음(만들지 않음) — HTTP 캐시만 갱신하면 됨. 규칙: docs/WORKFLOW.md 6장.
  var buildMeta = document.querySelector('meta[name="site-build"]');
  var verMeta = document.querySelector('meta[name="site-version-url"]');
  var curBuild = buildMeta ? buildMeta.getAttribute("content") : "";
  var verUrl = verMeta ? verMeta.getAttribute("content") : "";
  var RK = "dh-reload-guard-v1", lastVerCheck = 0;
  var hardReload = function () {
    // HTML을 HTTP 캐시 무시하고 한 번 받아 캐시를 갱신한 뒤 reload (Pages HTML max-age=600 대응)
    var go = function () { location.reload(); };
    if (!window.fetch) return go();
    fetch(location.href, { cache: "reload", credentials: "same-origin" }).then(go, go);
  };
  var checkVersion = function (force) {
    if (!curBuild || !verUrl || !window.fetch) return;
    var now = Date.now();
    if (!force && now - lastVerCheck < 15000) return; // 너무 잦은 확인 방지
    lastVerCheck = now;
    fetch(verUrl + "?t=" + now, { cache: "no-store" })
      .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
      .then(function (v) {
        var nb = v && String(v.build || "");
        if (!nb || nb === curBuild) return;
        if (Number(nb) && Number(curBuild) && Number(nb) < Number(curBuild)) return; // CDN이 더 옛 버전을 준 경우 무시
        var g = null;
        try { g = JSON.parse(sessionStorage.getItem(RK) || "null"); } catch (e) {}
        if (g && ((g.to === nb && Date.now() - g.t < 300000) || Date.now() - g.t < 30000)) return; // 같은 버전은 5분에 1회, 어떤 경우든 30초 간격 → 루프 방지
        try { sessionStorage.setItem(RK, JSON.stringify({ to: nb, from: curBuild, t: Date.now() })); } catch (e) { return; } // 가드 저장 불가 시 자동 새로고침 안 함
        hardReload();
      })
      .catch(function () { /* 오프라인 등: 조용히 무시 */ });
  };
  checkVersion(true);
  document.addEventListener("visibilitychange", function () { if (document.visibilityState === "visible") checkVersion(false); });
  window.addEventListener("pageshow", function (e) { if (e.persisted) checkVersion(true); });

  // 1-2) 헤더 ↻ 새로고침 버튼 (수동, 항상 표시)
  var rbtn = document.querySelector(".refresh-btn");
  if (rbtn) {
    rbtn.addEventListener("click", function () {
      rbtn.classList.add("is-spinning");
      try { sessionStorage.removeItem("dh-research-open-v1"); } catch (e) {}
      hardReload();
    });
  }

  var prose = document.querySelector(".prose");
  if (!prose) return;

  // 2) 맨 URL(https://…) 텍스트를 링크로 (GitHub 렌더링과 동일하게)
  var urlRe = /(https?:\/\/[^\s<>()"'`]+[^\s<>()"'`.,;:!?·)\]])/g;
  var walker = document.createTreeWalker(prose, NodeFilter.SHOW_TEXT, {
    acceptNode: function (n) {
      if (!n.nodeValue || n.nodeValue.indexOf("http") === -1) return NodeFilter.FILTER_REJECT;
      var p = n.parentNode;
      while (p && p !== prose) {
        if (/^(A|CODE|PRE|SCRIPT|STYLE)$/.test(p.nodeName)) return NodeFilter.FILTER_REJECT;
        p = p.parentNode;
      }
      return NodeFilter.FILTER_ACCEPT;
    }
  });
  var nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);
  nodes.forEach(function (n) {
    var text = n.nodeValue, frag = document.createDocumentFragment(), last = 0, m;
    urlRe.lastIndex = 0;
    while ((m = urlRe.exec(text))) {
      frag.appendChild(document.createTextNode(text.slice(last, m.index)));
      var a = document.createElement("a");
      a.href = m[1]; a.textContent = m[1];
      frag.appendChild(a);
      last = m.index + m[1].length;
    }
    if (last === 0) return;
    frag.appendChild(document.createTextNode(text.slice(last)));
    n.parentNode.replaceChild(frag, n);
  });

  // 3) 외부 링크는 새 탭
  prose.querySelectorAll('a[href^="http"]').forEach(function (a) {
    if (a.hostname !== location.hostname) { a.target = "_blank"; a.rel = "noopener noreferrer"; }
  });

  // 4) 표는 가로 스크롤 래퍼로 감싸기
  prose.querySelectorAll("table").forEach(function (t) {
    if (t.parentNode.classList && t.parentNode.classList.contains("table-wrap")) return;
    var w = document.createElement("div");
    w.className = "table-wrap";
    t.parentNode.insertBefore(w, t);
    w.appendChild(t);
  });

  // 4-1) "### 논조·다른 시각" 섹션 목록에 클래스 부여(스타일용)
  prose.querySelectorAll("h3").forEach(function (h) {
    if (h.textContent.trim().indexOf("논조") !== 0) return;
    h.classList.add("stance-head");
    var n = h.nextElementSibling;
    if (n && n.tagName === "UL") n.classList.add("stance");
  });

  // 4-2) 뉴스 항목(## N. 제목)마다 리서치 버튼 (상태 3가지, 규칙: docs/WORKFLOW.md 8장)
  //   ① 📄 리서치 보기   — 기사 메타에 '**심층 리서치:**' 링크가 있으면(빌드된 마크다운 → API 불필요) 그 페이지로
  //   ② ⏳ 리서치 진행 중 — 열린 research 이슈(작성자 DreamHouseKSH)가 이 기사를 가리키면 그 이슈로 (GitHub REST, 비인증)
  //   ③ 🔍 리서치 요청   — 그 외: 미리 채운 GitHub 이슈 작성 화면(새 탭)
  var newsM = decodeURIComponent(location.pathname).match(/\/news\/(\d{4}-\d{2}-\d{2})\/([^\/]+?)(?:\.html)?\/?$/);
  if (newsM) {
    var REPO = "DreamHouseKSH/dreamhouse-briefings";
    var OWNER = "DreamHouseKSH";
    var ISSUE_NEW = "https://github.com/" + REPO + "/issues/new";
    var rDate = newsM[1], rField = newsM[2];
    var pageUrl = location.origin + location.pathname;
    var normUrl = function (u) {
      if (!u) return "";
      try { u = decodeURIComponent(u); } catch (e) {}
      return u.trim().replace(/^https?:\/\//i, "").replace(/^www\./i, "").replace(/#.*$/, "").replace(/\/+$/, "").toLowerCase();
    };
    var normPage = function (u) {
      // 아카이브 URL → "news/YYYY-MM-DD/분야#앵커" 형태로
      if (!u) return "";
      try { u = decodeURIComponent(u); } catch (e) {}
      var m = u.match(/\/news\/(\d{4}-\d{2}-\d{2})\/([^\/#?]+?)(?:\.html|\.md)?\/?(?:\?[^#]*)?(#.*)?$/);
      return m ? ("news/" + m[1] + "/" + m[2] + (m[3] || "")).toLowerCase() : "";
    };
    var items = [];
    prose.querySelectorAll("h2").forEach(function (h) {
      var raw = h.textContent.replace(/\s+/g, " ").trim();
      var tm = raw.match(/^\d+\.\s*(.+)$/);
      if (!tm) return;
      var title = tm[1];
      var meta = h.nextElementSibling;
      var src = "", doneHref = "";
      if (meta && meta.tagName === "UL") {
        meta.querySelectorAll("li").forEach(function (li) {
          var st = li.querySelector("strong");
          if (!st) return;
          var label = st.textContent.trim();
          if (label.indexOf("원문") === 0 && !src) {
            var a = li.querySelector('a[href^="http"]');
            if (a) src = a.href;
          }
          if (label.indexOf("심층 리서치") === 0) {
            li.classList.add("research-done");
            var ra = li.querySelector("a[href]");
            if (ra && !doneHref) doneHref = ra.href;
          }
        });
      } else {
        meta = null;
      }
      var anchorUrl = pageUrl + (h.id ? "#" + encodeURIComponent(h.id) : "");
      var btn = document.createElement("a");
      btn.className = "research-btn";
      if (doneHref) {
        btn.classList.add("is-done");
        btn.href = doneHref;
        btn.textContent = "📄 리서치 보기";
        btn.title = "이 기사의 심층 리서치 결과 보기";
        btn.setAttribute("data-state", "done");
      } else {
        var body = [
          "## 리서치 요청",
          "",
          "- 날짜: " + rDate,
          "- 분야: " + rField,
          "- 기사 제목: " + title,
          "- 원문: " + (src || "(원문 링크 없음)"),
          "- 아카이브: " + anchorUrl,
          "",
          "궁금한 점(선택): ",
          ""
        ].join("\n");
        btn.href = ISSUE_NEW +
          "?title=" + encodeURIComponent("[research] " + title) +
          "&labels=research" +
          "&body=" + encodeURIComponent(body);
        btn.target = "_blank";
        btn.rel = "noopener noreferrer";
        btn.textContent = "🔍 리서치 요청";
        btn.title = "이 기사 심층 리서치 요청 (GitHub 이슈 작성 화면이 새 탭으로 열립니다)";
        btn.setAttribute("data-state", "request");
        items.push({ btn: btn, src: normUrl(src), page: normPage(anchorUrl), title: title.replace(/\s+/g, " ").trim(),
                     orig: { href: btn.href, text: btn.textContent, title: btn.title } });
      }
      var li2 = document.createElement("li");
      li2.className = "research-req";
      li2.appendChild(btn);
      if (meta) {
        meta.appendChild(li2);
      } else {
        var wrap = document.createElement("p");
        wrap.className = "research-req";
        wrap.appendChild(btn);
        h.parentNode.insertBefore(wrap, h.nextSibling);
      }
    });

    // 진행 중 표시: 열린 research 이슈 조회(비인증 60회/시간 → sessionStorage 5분 캐시, 실패 시 조용히 기본 버튼 유지)
    var markInProgress = function (issues) {
      issues = issues || [];
      items.forEach(function (it) {
        if (it.btn.getAttribute("data-state") === "progress") { // 다시 확인할 때를 위해 기본 상태로 되돌린 뒤 판정
          it.btn.classList.remove("is-progress");
          it.btn.href = it.orig.href; it.btn.textContent = it.orig.text; it.btn.title = it.orig.title;
          it.btn.setAttribute("data-state", "request");
        }
        for (var i = 0; i < issues.length; i++) {
          var is = issues[i];
          var hit = (it.src && is.srcs.indexOf(it.src) !== -1) ||
                    (it.page && is.pages.indexOf(it.page) !== -1) ||
                    (is.date === rDate && is.title && is.title === it.title);
          if (!hit) continue;
          it.btn.classList.add("is-progress");
          it.btn.href = is.url;
          it.btn.textContent = "⏳ 리서치 진행 중";
          it.btn.title = "리서치 진행 중 (요청 이슈 #" + is.number + " 보기)";
          it.btn.setAttribute("data-state", "progress");
          break;
        }
      });
    };
    var parseIssues = function (arr) {
      var out = [];
      (Array.isArray(arr) ? arr : []).forEach(function (x) {
        if (!x || x.pull_request || x.state !== "open") return;
        if (!x.user || x.user.login !== OWNER) return; // 다른 작성자 이슈 무시
        var hasLabel = (x.labels || []).some(function (l) { return (l && (l.name || l)) === "research"; });
        if (!hasLabel) return;
        var b = String(x.body || ""), srcs = [], pages = [], date = "", m;
        var lineRe = /^\s*[-*]?\s*(원문|아카이브|날짜)\s*:\s*(\S+)/gm;
        while ((m = lineRe.exec(b))) {
          if (m[1] === "원문") srcs.push(normUrl(m[2]));
          else if (m[1] === "아카이브") pages.push(normPage(m[2]));
          else date = m[2];
        }
        var t = String(x.title || "").replace(/^\s*\[research\]\s*/i, "").replace(/\s+/g, " ").trim();
        out.push({ number: x.number, url: x.html_url, srcs: srcs, pages: pages, date: date, title: t });
      });
      return out;
    };
    var CK = "dh-research-open-v1", TTL = 5 * 60 * 1000, REVISIT = 60 * 1000, inflight = false;
    var loadResearch = function (maxAge) {
      if (!items.length || !window.fetch || inflight) return;
      var cached = null;
      try {
        var c = JSON.parse(sessionStorage.getItem(CK) || "null");
        if (c && c.t && Date.now() - c.t < maxAge && Array.isArray(c.d)) cached = c.d;
      } catch (e) {}
      if (cached) { markInProgress(cached); return; }
      inflight = true;
      fetch("https://api.github.com/repos/" + REPO + "/issues?labels=research&state=open&per_page=50",
            { headers: { "Accept": "application/vnd.github+json" }, cache: "no-store" })
        .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
        .then(function (j) {
          var d = parseIssues(j);
          try { sessionStorage.setItem(CK, JSON.stringify({ t: Date.now(), d: d })); } catch (e) {}
          markInProgress(d);
        })
        .catch(function () { /* 조용히 현재 버튼 유지 */ })
        .then(function () { inflight = false; });
    };
    loadResearch(TTL);
    // 화면에 돌아올 때(앱 전환·탭 복귀·bfcache 복원) 캐시가 1분 넘었으면 다시 확인
    document.addEventListener("visibilitychange", function () { if (document.visibilityState === "visible") loadResearch(REVISIT); });
    window.addEventListener("pageshow", function (e) { if (e.persisted) loadResearch(REVISIT); });
  }

  // 5) 오른쪽 목차(h2) + 현재 위치 강조
  var toc = document.querySelector(".toc");
  var heads = Array.prototype.slice.call(prose.querySelectorAll("h2"));
  if (toc && heads.length >= 2) {
    var ol = toc.querySelector("ol"), links = [];
    heads.forEach(function (h, i) {
      if (!h.id) h.id = "s-" + (i + 1);
      var li = document.createElement("li"), a = document.createElement("a");
      a.href = "#" + encodeURIComponent(h.id);
      a.textContent = h.textContent.replace(/\s+/g, " ").trim();
      li.appendChild(a); ol.appendChild(li); links.push(a);
    });
    toc.hidden = false;
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            var idx = heads.indexOf(e.target);
            links.forEach(function (l, j) { l.classList.toggle("active", j === idx); });
          }
        });
      }, { rootMargin: "-15% 0px -70% 0px" });
      heads.forEach(function (h) { io.observe(h); });
    }
  }
})();
