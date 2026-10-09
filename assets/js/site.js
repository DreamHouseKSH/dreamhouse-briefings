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
  //   페이지의 <meta name="site-build"> 와 /version.json(no-store)을 비교. 열 때·화면 복귀 시 다르면 바로 reload,
  //   화면을 보는 중(3분 주기 확인)에 바뀌면 상단 '새 내용이 있어요 · 새로고침' 배너(닫기 가능).
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
  var dismissedBuild = "";
  var showUpdateBanner = function (nb) {
    if (document.querySelector(".update-banner") || (nb && nb === dismissedBuild)) return; // 닫은 버전은 다시 띄우지 않음
    var bar = document.createElement("div");
    bar.className = "update-banner";
    bar.setAttribute("role", "status");
    var go = document.createElement("button");
    go.type = "button"; go.className = "ub-go"; go.textContent = "새 내용이 있어요 · 새로고침";
    go.addEventListener("click", function () {
      go.disabled = true;
      try { sessionStorage.setItem(RK, JSON.stringify({ to: nb, from: curBuild, t: Date.now() })); } catch (e) {} // 다시 연 HTML이 아직 옛 버전이어도 자동 재시도 루프 방지
      hardReload();
    });
    var x = document.createElement("button");
    x.type = "button"; x.className = "ub-close"; x.setAttribute("aria-label", "닫기"); x.title = "닫기"; x.textContent = "✕";
    x.addEventListener("click", function () { dismissedBuild = nb || ""; bar.remove(); });
    bar.appendChild(go); bar.appendChild(x);
    var hdr = document.querySelector(".site-header");
    if (hdr && hdr.parentNode) hdr.parentNode.insertBefore(bar, hdr.nextSibling); else document.body.insertBefore(bar, document.body.firstChild);
  };
  // mode: "load"(처음 열 때)·"return"(화면 복귀) → 바뀌었으면 바로 reload / "poll"(보는 중 3분 주기) → 배너만
  var checkVersion = function (mode) {
    if (!curBuild || !verUrl || !window.fetch) return;
    var now = Date.now();
    if (mode === "return" && now - lastVerCheck < 15000) return; // 너무 잦은 확인 방지
    lastVerCheck = now;
    fetch(verUrl + "?t=" + now, { cache: "no-store" })
      .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
      .then(function (v) {
        var nb = v && String(v.build || "");
        if (!nb || nb === curBuild) return;
        if (Number(nb) && Number(curBuild) && Number(nb) < Number(curBuild)) return; // CDN이 더 옛 버전을 준 경우 무시
        if (mode === "poll") { showUpdateBanner(nb); return; }
        var g = null;
        try { g = JSON.parse(sessionStorage.getItem(RK) || "null"); } catch (e) {}
        if (g && ((g.to === nb && Date.now() - g.t < 300000) || Date.now() - g.t < 30000)) { showUpdateBanner(nb); return; } // 루프 방지 → 배너로 대신
        try { sessionStorage.setItem(RK, JSON.stringify({ to: nb, from: curBuild, t: Date.now() })); } catch (e) { showUpdateBanner(nb); return; }
        hardReload();
      })
      .catch(function () { /* 오프라인 등: 조용히 무시 */ });
  };
  checkVersion("load");
  document.addEventListener("visibilitychange", function () { if (document.visibilityState === "visible") checkVersion("return"); });
  window.addEventListener("pageshow", function (e) { if (e.persisted) checkVersion("return"); });
  // 보는 중에는 3분마다 확인(숨겨진 동안은 건너뜀). 리서치 상태 API는 이 주기로 돌리지 않음(호출 한도).
  setInterval(function () { if (document.visibilityState === "visible") checkVersion("poll"); }, 3 * 60 * 1000);

  // 1-2) 헤더 ↻ 새로고침 버튼 (수동, 항상 표시)
  var rbtn = document.querySelector(".refresh-btn");
  if (rbtn) {
    rbtn.addEventListener("click", function () {
      rbtn.classList.add("is-spinning");
      try { localStorage.removeItem("dh-research-v2"); } catch (e) {}
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
  //      닫힌 이슈면 📄 리서치 보기(마지막 댓글의 research/ URL, 없으면 이슈) — 새로고침 없이 3분마다 갱신
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

    // 실시간 상태 갱신 (새로고침 없이 버튼만 DOM에서 교체: 🔍 요청 → ⏳ 진행 중 → 📄 리서치 보기)
    //   GET /repos/{REPO}/issues?labels=research&state=all&creator=DreamHouseKSH (비인증, 시간당 60회 한도)
    //   - 화면이 보이는 동안 약 3분마다 + 화면 복귀 시(마지막 확인 2분 경과 시). 숨겨진 동안은 호출 안 함.
    //   - 결과는 localStorage 로 모든 탭이 공유(마지막 확인 170초 이내면 호출 대신 공유 결과 사용, 20초 잠금으로 동시 호출 방지)
    //     → 탭을 여러 개 열어도 이슈 목록은 시간당 약 20회. 'storage' 이벤트로 다른 탭 결과도 즉시 반영.
    //   - 남은 한도 X-RateLimit-Remaining < 10 이면 reset 시각까지 쉼. 실패하면 조용히 현재 버튼 유지.
    //   - 닫힌 이슈(완료) + 페이지에 '심층 리서치' 링크가 아직 없음 → 마지막 댓글에서 research/ URL을 찾아 연결
    //     (https://dreamhouseksh.github.io/dreamhouse-briefings/research/ 로 시작하는 것만 허용, 아니면 이슈 링크).
    //     댓글 조회는 이 페이지에 해당 기사가 있을 때만, 이슈당 1회(결과를 localStorage 에 영구 캐시).
    var LS = "dh-research-v2", LSC = "dh-research-comments-v2", LSL = "dh-research-lock-v2", LSB = "dh-research-backoff-v2";
    var POLL = 3 * 60 * 1000, FRESH = 170 * 1000, REVISIT = 120 * 1000;
    var RESEARCH_PREFIX = "https://dreamhouseksh.github.io/dreamhouse-briefings/research/";
    var lsGet = function (k) { try { return JSON.parse(localStorage.getItem(k) || "null"); } catch (e) { return null; } };
    var lsSet = function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} };
    var apiGet = function (path) {
      return fetch("https://api.github.com/repos/" + REPO + path,
                   { headers: { "Accept": "application/vnd.github+json" }, cache: "no-store" })
        .then(function (r) {
          var rem = Number(r.headers.get("x-ratelimit-remaining")), rst = Number(r.headers.get("x-ratelimit-reset"));
          if (!isNaN(rem) && rem < 10 && rst) lsSet(LSB, { until: rst * 1000 });
          if (r.status === 403 || r.status === 429) lsSet(LSB, { until: rst ? rst * 1000 : Date.now() + 15 * 60 * 1000 });
          if (!r.ok) throw new Error("HTTP " + r.status);
          return r.json();
        });
    };
    var parseIssues = function (arr) {
      var out = [];
      (Array.isArray(arr) ? arr : []).forEach(function (x) {
        if (!x || x.pull_request) return;
        if (!x.user || x.user.login !== OWNER) return; // 다른 작성자 이슈 무시
        if (x.state === "closed" && x.state_reason === "not_planned") return; // 처리 안 하고 닫은 요청은 무시
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
        out.push({ number: x.number, url: x.html_url, state: x.state, closedAt: x.closed_at || "", comments: x.comments || 0,
                   srcs: srcs, pages: pages, date: date, title: t });
      });
      return out;
    };
    var matches = function (it, is) {
      return (it.src && is.srcs.indexOf(it.src) !== -1) ||
             (it.page && is.pages.indexOf(it.page) !== -1) ||
             (is.date === rDate && is.title && is.title === it.title);
    };
    var setBtn = function (it, state, href, text, title, external) {
      var b = it.btn;
      b.classList.toggle("is-progress", state === "progress");
      b.classList.toggle("is-done", state === "done");
      b.href = href; b.textContent = text; b.title = title;
      if (external) { b.target = "_blank"; b.rel = "noopener noreferrer"; } else { b.removeAttribute("target"); b.removeAttribute("rel"); }
      b.setAttribute("data-state", state);
    };
    var findResearchUrl = function (comments) {
      // 마지막 댓글부터 거꾸로, 허용된 접두사로 시작하는 URL만
      for (var i = comments.length - 1; i >= 0; i--) {
        var urls = String(comments[i] && comments[i].body || "").match(/https?:\/\/[^\s<>()"'`\]]+/g) || [];
        for (var j = 0; j < urls.length; j++) {
          var u = urls[j].replace(/[.,;:!?·)]+$/, "");
          if (u.indexOf(RESEARCH_PREFIX) === 0 && u.length > RESEARCH_PREFIX.length && !/[\\]|\.\./.test(u)) return u;
        }
        if (comments[i] && comments[i].user && comments[i].user.login === OWNER) break; // 마지막 내 댓글까지만
      }
      return "";
    };
    var pendingComments = {};
    var resolveClosed = function (is) {
      var cc = lsGet(LSC) || {};
      if (Object.prototype.hasOwnProperty.call(cc, is.number)) return cc[is.number];
      if (pendingComments[is.number] || !is.comments) return is.comments ? null : "";
      var bo = lsGet(LSB); if (bo && bo.until > Date.now()) return null;
      pendingComments[is.number] = true;
      var last = Math.max(1, Math.ceil(is.comments / 100));
      apiGet("/issues/" + is.number + "/comments?per_page=100&page=" + last)
        .then(function (cs) {
          var c2 = lsGet(LSC) || {};
          c2[is.number] = findResearchUrl(Array.isArray(cs) ? cs.filter(function (c) { return c && c.user && c.user.login === OWNER; }) : []);
          lsSet(LSC, c2);
          applyStatus((lsGet(LS) || {}).d || []);
        })
        .catch(function () {})
        .then(function () { delete pendingComments[is.number]; });
      return null; // 아직 모름 → 일단 이슈 링크
    };
    var applyStatus = function (issues) {
      items.forEach(function (it) {
        var open = null, closed = null;
        issues.forEach(function (is) {
          if (!matches(it, is)) return;
          if (is.state === "open") { if (!open) open = is; }
          else if (!closed || is.closedAt > closed.closedAt) closed = is;
        });
        if (open) {
          setBtn(it, "progress", open.url, "⏳ 리서치 진행 중", "리서치 진행 중 (요청 이슈 #" + open.number + " 보기)", true);
        } else if (closed) {
          var ru = resolveClosed(closed);
          if (ru) setBtn(it, "done", ru, "📄 리서치 보기", "이 기사의 심층 리서치 결과 보기", false);
          else setBtn(it, "done", closed.url, "📄 리서치 보기", "리서치 완료 (요청 이슈 #" + closed.number + " 보기)", true);
        } else {
          setBtn(it, "request", it.orig.href, it.orig.text, it.orig.title, true);
        }
      });
    };
    var refreshStatus = function (maxAge) {
      if (!items.length || !window.fetch) return;
      var c = lsGet(LS);
      if (c && Array.isArray(c.d)) applyStatus(c.d);           // 공유 결과 먼저 반영
      if (c && c.t && Date.now() - c.t < maxAge) return;        // 아직 신선 → 호출 안 함
      var bo = lsGet(LSB); if (bo && bo.until > Date.now()) return;
      var lk = lsGet(LSL); if (lk && Date.now() - lk.t < 20000) return; // 다른 탭이 호출 중
      lsSet(LSL, { t: Date.now() });
      apiGet("/issues?labels=research&state=all&creator=" + OWNER + "&per_page=50&sort=updated")
        .then(function (j) {
          var d = parseIssues(j);
          lsSet(LS, { t: Date.now(), d: d });
          applyStatus(d);
        })
        .catch(function () { /* 조용히 현재 버튼 유지 */ })
        .then(function () { try { localStorage.removeItem(LSL); } catch (e) {} });
    };
    refreshStatus(FRESH);
    document.addEventListener("visibilitychange", function () { if (document.visibilityState === "visible") refreshStatus(REVISIT); });
    window.addEventListener("pageshow", function (e) { if (e.persisted) refreshStatus(REVISIT); });
    window.addEventListener("storage", function (e) {
      if ((e.key === LS || e.key === LSC) && items.length) { var c = lsGet(LS); if (c && Array.isArray(c.d)) applyStatus(c.d); }
    });
    if (items.length) setInterval(function () { if (document.visibilityState === "visible") refreshStatus(FRESH); }, POLL);
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
