/* 방문 통계 페이지 (GoatCounter 공개 카운터 JSON만 사용, 외부 라이브러리 없음)
   - 날짜별: counter/TOTAL.json?start=D&end=D+1 (end는 미포함) × 30일, 동시 6개로 묶어서 조회
   - TOP 10: 주요 경로별 counter/{경로}.json?start=30일전 (404 = 기록 없음 = 0)
   - 결과는 localStorage 'dh-stats-v1' 에 1시간 캐시 */
(function () {
  var root = document.querySelector(".stats-page");
  if (!root) return;
  var base = (root.getAttribute("data-gc") || "").replace(/\/+$/, "");
  if (!/^https:\/\/[a-z0-9-]+\.goatcounter\.com$/i.test(base)) { root.querySelector(".stats-chart").innerHTML = '<p class="muted">통계 설정이 꺼져 있어요.</p>'; return; }
  var CK = "dh-stats-v1", TTL = 3600 * 1000, DAYS = 30;
  var kst = function (off) { return new Date(Date.now() + 9 * 3600e3 - (off || 0) * 864e5).toISOString().slice(0, 10); };
  var nextDay = function (d) { var t = new Date(d + "T00:00:00Z"); t.setUTCDate(t.getUTCDate() + 1); return t.toISOString().slice(0, 10); };
  var num = function (j) { var n = j && (j.count != null ? j.count : j.count_unique); n = parseInt(String(n == null ? "" : n).replace(/[^\d]/g, ""), 10); return isNaN(n) ? 0 : n; };
  var get = function (path, q) {
    var url = base + "/counter/" + encodeURIComponent(path) + ".json" + (q ? "?" + q : "");
    return fetch(url, { mode: "cors", credentials: "omit" }).then(function (r) {
      if (r.status === 404) return 0; // 아직 한 번도 기록 안 된 경로
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json().then(num);
    });
  };
  var pool = function (tasks, n) { // 동시 n개씩 묶어서 실행
    var out = new Array(tasks.length), i = 0;
    var run = function () { if (i >= tasks.length) return Promise.resolve(); var k = i++; return tasks[k]().then(function (v) { out[k] = v; }, function () { out[k] = null; }).then(run); };
    var ws = []; for (var w = 0; w < Math.min(n, tasks.length); w++) ws.push(run());
    return Promise.all(ws).then(function () { return out; });
  };
  var enc = function (u) { try { return encodeURI(decodeURI(u)); } catch (e) { return u; } }; // count.js 는 퍼센트 인코딩된 경로로 기록
  var load = function () {
    var days = []; for (var o = DAYS - 1; o >= 0; o--) days.push(kst(o));
    var from = days[0], cut = from;
    var pages = (window.DH_STATS_PAGES || []).filter(function (p) {
      var m = /(\d{4}-\d{2}-\d{2})/.exec(p.u); return !m || m[1] >= cut; // 날짜 페이지는 최근 30일 것만
    }).slice(0, 150);
    var tasks = days.map(function (d) { return function () { return get("TOTAL", "start=" + d + "&end=" + nextDay(d)); }; });
    tasks.push(function () { return get("TOTAL", ""); });
    pages.forEach(function (p) { tasks.push(function () { return get(enc(p.u), "start=" + from); }); });
    return pool(tasks, 6).then(function (r) {
      return {
        at: Date.now(), days: days.map(function (d, k) { return { d: d, n: r[k] }; }), total: r[DAYS],
        pages: pages.map(function (p, k) { return { u: p.u, t: p.t, n: r[DAYS + 1 + k] }; })
      };
    });
  };
  var fmt = function (n) { return n == null ? "—" : n.toLocaleString("ko-KR"); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var render = function (s) {
    var sum = function (a) { var t = 0, ok = false; a.forEach(function (x) { if (x.n != null) { t += x.n; ok = true; } }); return ok ? t : null; };
    var today = s.days[s.days.length - 1].n;
    var set = function (k, v) { root.querySelector('[data-k="' + k + '"]').textContent = v; };
    set("total", fmt(s.total)); set("week", fmt(sum(s.days.slice(-7)))); set("month", fmt(sum(s.days)));
    set("today", today ? fmt(today) : "—");
    var max = 1; s.days.forEach(function (x) { if (x.n > max) max = x.n; });
    var W = 30 * 12, H = 120, bw = 8, svg = '<svg viewBox="0 0 ' + W + ' ' + (H + 22) + '" preserveAspectRatio="none" aria-hidden="true">';
    s.days.forEach(function (x, i) {
      var h = x.n ? Math.max(2, Math.round(x.n / max * H)) : 0, X = i * 12 + 2;
      svg += '<rect class="bar' + (i === s.days.length - 1 ? ' today' : '') + '" x="' + X + '" y="' + (H - h) + '" width="' + bw + '" height="' + h + '" rx="2"><title>' + x.d + ' · ' + (x.n == null ? '실패' : x.n + '명') + '</title></rect>';
      if (x.n) svg += '<text x="' + (X + bw / 2) + '" y="' + (H - h - 3) + '" text-anchor="middle">' + x.n + '</text>';
      if (i % 7 === 0 || i === s.days.length - 1) svg += '<text class="ax" x="' + (X + bw / 2) + '" y="' + (H + 15) + '" text-anchor="middle">' + x.d.slice(5).replace("-", "/") + '</text>';
    });
    svg += '<line class="base" x1="0" x2="' + W + '" y1="' + H + '" y2="' + H + '"/></svg>';
    root.querySelector(".stats-chart").innerHTML = svg;
    var top = s.pages.filter(function (p) { return p.n > 0; }).sort(function (a, b) { return b.n - a.n; }).slice(0, 10);
    var tmax = top.length ? top[0].n : 1;
    root.querySelector(".stats-top").innerHTML = top.length ? top.map(function (p) {
      return '<li><a href="' + esc(p.u) + '">' + esc(p.t) + '</a><span class="tb"><i style="width:' + Math.round(p.n / tmax * 100) + '%"></i></span><b>' + p.n + '</b></li>';
    }).join("") : '<li class="muted">아직 기록된 페이지가 없어요.</li>';
    var t = new Date(s.at + 9 * 3600e3).toISOString().slice(0, 16).replace("T", " ");
    root.querySelector(".stats-updated").textContent = "숫자를 가져온 시각: " + t + " KST (1시간 동안 다시 쓰고, 그 뒤 새로 가져와요)";
  };
  var c = null; try { c = JSON.parse(localStorage.getItem(CK) || "null"); } catch (e) {}
  if (c && c.at && Date.now() - c.at < TTL && c.days && c.days.length === DAYS && c.days[DAYS - 1].d === kst(0)) { render(c); return; }
  if (!window.fetch) return;
  load().then(function (s) { try { localStorage.setItem(CK, JSON.stringify(s)); } catch (e) {} render(s); })
    .catch(function () { root.querySelector(".stats-chart").innerHTML = '<p class="muted">통계를 불러오지 못했어요. 잠시 뒤 다시 열어 주세요.</p>'; });
})();
