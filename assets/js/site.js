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

  // 4-2) 뉴스 항목(## N. 제목)마다 '🔍 리서치 요청' 버튼 → 미리 채운 GitHub 이슈 작성 화면(새 탭)
  //      처리 규칙: docs/WORKFLOW.md 9장 (research 라벨 + 작성자 DreamHouseKSH 만 처리)
  var newsM = decodeURIComponent(location.pathname).match(/\/news\/(\d{4}-\d{2}-\d{2})\/([^\/]+?)(?:\.html)?\/?$/);
  if (newsM) {
    var ISSUE_NEW = "https://github.com/DreamHouseKSH/dreamhouse-briefings/issues/new";
    var rDate = newsM[1], rField = newsM[2];
    var pageUrl = location.origin + location.pathname;
    prose.querySelectorAll("h2").forEach(function (h) {
      var raw = h.textContent.replace(/\s+/g, " ").trim();
      var tm = raw.match(/^\d+\.\s*(.+)$/);
      if (!tm) return;
      var title = tm[1];
      var meta = h.nextElementSibling;
      var src = "";
      if (meta && meta.tagName === "UL") {
        meta.querySelectorAll("li").forEach(function (li) {
          var st = li.querySelector("strong");
          if (!st) return;
          var label = st.textContent.trim();
          if (label.indexOf("원문") === 0 && !src) {
            var a = li.querySelector('a[href^="http"]');
            if (a) src = a.href;
          }
          if (label.indexOf("심층 리서치") === 0) li.classList.add("research-done");
        });
      } else {
        meta = null;
      }
      var anchorUrl = pageUrl + (h.id ? "#" + encodeURIComponent(h.id) : "");
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
      var href = ISSUE_NEW +
        "?title=" + encodeURIComponent("[research] " + title) +
        "&labels=research" +
        "&body=" + encodeURIComponent(body);
      var btn = document.createElement("a");
      btn.className = "research-btn";
      btn.href = href;
      btn.target = "_blank";
      btn.rel = "noopener noreferrer";
      btn.textContent = "🔍 리서치 요청";
      btn.title = "이 기사 심층 리서치 요청 (GitHub 이슈 작성 화면이 새 탭으로 열립니다)";
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
