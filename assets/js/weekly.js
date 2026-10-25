/* Weekly magazine enhancement only. Full prose, contents and schedule table work without JS. */
(function () {
  'use strict';
  var magazine = document.querySelector('.weekly-magazine');
  if (!magazine) return;
  magazine.querySelectorAll('.wm-body h3').forEach(function (heading) {
    var title = heading.textContent.trim();
    var fields = [['IT', 'it'], ['AI', 'ai'], ['모델', 'model'], ['엔진', 'engine'], ['GitHub', 'github']];
    fields.forEach(function (field) {
      if (title.indexOf(field[0] + ' —') === 0 || (field[0] === 'GitHub' && title.indexOf('GitHub 트렌드 —') === 0)) heading.dataset.field = field[1];
    });
  });
  // Use the actual schedule rows, including every qualifier and source link.
  magazine.querySelectorAll('table').forEach(function (table) {
    var headers = Array.from(table.querySelectorAll('thead th')).map(function (h) { return h.textContent.trim(); });
    if (headers.join('|') !== '한국시간|공식 일정|발표 뒤 확인할 질문') return;
    var list = document.createElement('ol');
    list.className = 'wm-timeline';
    list.setAttribute('aria-label', '날짜가 확인된 공식 일정 · 한국시간');
    table.querySelectorAll('tbody tr').forEach(function (row) {
      var cells = row.querySelectorAll('td');
      if (cells.length !== 3) return;
      var item = document.createElement('li');
      cells.forEach(function (cell, i) {
        var block = document.createElement(i === 0 ? 'h3' : 'div');
        if (i === 2) {
          var label = document.createElement('strong'); label.textContent = '발표 뒤 확인할 질문';
          block.appendChild(label);
        }
        while (cell.firstChild) block.appendChild(cell.firstChild);
        item.appendChild(block);
      });
      list.appendChild(item);
    });
    table.replaceWith(list);
  });
})();
