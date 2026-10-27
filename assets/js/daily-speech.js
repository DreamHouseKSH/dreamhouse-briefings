/* Browser-provided, local Korean voices only. No text leaves this page via a TTS service. */
(function () {
  'use strict';
  window.createDailySpeech = function (options) {
    const synth = window.speechSynthesis;
    const supported = !!(synth && window.SpeechSynthesisUtterance);
    let voices = [], voice = null, token = 0, cursor = 0, currentSlide = null;
    let preferenceSet = false;
    let enabled = false, state = 'off', message = '', utterance = null, watchdog = null;
    const change = () => options.change();
    function cancel(keepPosition) {
      token++; clearTimeout(watchdog); watchdog = null; utterance = null;
      if (supported) { try { synth.cancel(); } catch (_) {} }
      if (!keepPosition) { cursor = 0; currentSlide = null; }
      state = enabled ? 'ready' : 'off';
    }
    function fail(text) {
      cancel(true); state = 'error'; message = text;
      options.error(); change();
    }
    function refresh() {
      const previous = voice && voice.voiceURI;
      try { voices = supported ? synth.getVoices().filter(v => /^ko(?:-|$)/i.test(v.lang) && v.localService === true) : []; } catch (_) { voices = []; }
      voices = voices.filter((v, i, all) => all.findIndex(other => other.voiceURI === v.voiceURI) === i);
      voice = voices.find(v => v.voiceURI === previous) || voices.find(v => v.default) || voices[0] || null;
      if (!voice) {
        if (enabled) { enabled = false; cancel(false); options.error(); }
        message = supported ? '기기 내장 한국어 음성이 아직 없거나 제공되지 않습니다. 대본으로 읽어 주세요.' : '이 브라우저는 음성 읽기를 지원하지 않습니다. 대본으로 읽어 주세요.';
      } else if (!preferenceSet) {
        enabled = true; preferenceSet = true; state = 'ready'; message = '기기 내장 한국어 음성 준비됨 · 재생을 눌러 시작합니다.';
        options.modechange();
      } else if (state !== 'error') message = '기기 내장 음성 · 음색은 기기마다 다릅니다. 음성 켜기 후 재생을 눌러 주세요.';
      options.voices(voices, voice); change();
    }
    function start(slide, rate, resume) {
      if (!enabled || !voice || document.hidden) return false;
      const preserve = resume && currentSlide === slide;
      cancel(preserve);
      currentSlide = slide;
      const sentences = Array.from(slide.querySelectorAll('.day-script li')).map(li => li.textContent.trim()).filter(Boolean);
      if (!sentences.length) { fail('이 장의 대본이 없습니다. 음성을 멈췄습니다.'); return false; }
      if (cursor >= sentences.length) cursor = 0;
      const session = token;
      function read() {
        if (session !== token || !enabled || document.hidden) return;
        state = 'starting'; message = '음성 시작 확인 중'; change();
        utterance = new SpeechSynthesisUtterance(sentences[cursor]);
        utterance.voice = voice; utterance.lang = 'ko-KR'; utterance.rate = rate;
        utterance.onstart = () => {
          if (session !== token) return;
          clearTimeout(watchdog); state = 'speaking'; message = `${cursor + 1} / ${sentences.length}문장 읽는 중`;
          options.chunk(cursor + 1, sentences.length); change();
          watchdog = setTimeout(() => { if (session === token) fail('음성 응답이 오래 멈춰 재생을 중단했습니다. 대본을 읽거나 다시 재생해 주세요.'); }, 60000);
        };
        utterance.onend = () => {
          if (session !== token) return;
          clearTimeout(watchdog); utterance = null; cursor++;
          if (cursor < sentences.length) read();
          else { state = 'ready'; message = '이 장의 음성 읽기 완료'; cursor = 0; change(); options.complete(); }
        };
        utterance.onerror = event => {
          if (session === token) fail('음성 재생이 중단됐습니다' + (event.error ? ' (' + event.error + ')' : '') + '. 대본을 읽거나 재생을 다시 눌러 주세요.');
        };
        watchdog = setTimeout(() => { if (session === token) fail('음성이 시작되지 않았습니다. 기기 음성과 소리 설정을 확인하거나 대본으로 읽어 주세요.'); }, 8000);
        try { synth.speak(utterance); } catch (_) { fail('음성 재생을 시작할 수 없습니다. 대본으로 읽어 주세요.'); }
      }
      read(); return true;
    }
    const api = {
      get available() { return !!voice; }, get enabled() { return enabled; }, get state() { return state; }, get message() { return message; },
      setEnabled(value) { preferenceSet = true; enabled = !!(value && voice); cancel(false); message = enabled ? '음성 켜짐 · 재생을 눌러 시작합니다.' : '음성 꺼짐 · 대본과 무음 발표를 사용할 수 있습니다.'; change(); return enabled; },
      choose(uri) { voice = voices.find(v => v.voiceURI === uri) || voice; },
      start, cancel,
      pause() { const active = state === 'starting' || state === 'speaking'; cancel(true); state = enabled && active ? 'paused' : state; if (active) message = '일시정지 · 다시 재생하면 현재 문장 처음부터 읽습니다.'; change(); },
      refresh
    };
    if (supported && synth.addEventListener) synth.addEventListener('voiceschanged', refresh);
    // Defer the first callback until the caller has stored the controller.
    setTimeout(refresh, 0); setTimeout(refresh, 500); setTimeout(refresh, 2000); setTimeout(refresh, 5000);
    return api;
  };
})();
