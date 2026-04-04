/* =====================================================
   SQL Trainer — Client-side Logic
   ===================================================== */

'use strict';

// ── Personalized compliments ──────────────────────────
const COMPLIMENTS = [
  "You're a legend",
  "You're a star",
  "You're a genius",
  "You're a champion",
  "You're a hero",
  "You're a lifesaver",
  "You're a rockstar",
  "You're a superstar",
  "You're a beast",
  "You're a machine",
  "You're a wizard",
  "You're a magician",
  "You're the GOAT",
  "You're so amazing",
  "You're so awesome",
  "You're so brilliant",
  "You're so incredible",
  "You're so fantastic",
  "You're unreal",
  "You're unbelievable",
  "You're on fire",
];

function getCompliment(name) {
  const msg = COMPLIMENTS[Math.floor(Math.random() * COMPLIMENTS.length)];
  return `${msg}, ${name}! 🎉`;
}

// ── Live counter update ───────────────────────────────
function incrementCounter(selector) {
  const el = document.querySelector(selector);
  if (!el) return;
  const n = parseInt(el.textContent.match(/\d+/)?.[0] || '0');
  el.textContent = el.textContent.replace(/\d+/, n + 1);
}

// ── Panel toggle ──────────────────────────────────────
function togglePanel() {
  const panel     = document.getElementById('tablesPanel');
  const btn       = document.getElementById('panelToggle');
  const collapsed = panel.classList.toggle('collapsed');
  btn.textContent = collapsed ? '▼ Tables' : '▲';
}

// ── Hint toggle ───────────────────────────────────────
function toggleHint() {
  const badge  = document.getElementById('hintBadge');
  const btn    = document.getElementById('hintToggle');
  const hidden = badge.classList.toggle('hidden');
  btn.textContent = hidden ? '💡 Show hint' : '💡 Hide hint';
}

// ── Check answer ──────────────────────────────────────
async function checkAnswer() {
  const query = editor.getValue().trim();
  if (!query) { flashEmpty(); return; }

  setLoading(true);
  hideResult();

  try {
    const res  = await fetch('/check', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, exercise_id: EXERCISE_ID }),
    });
    const data = await res.json();
    setLoading(false);
    showResult(data);
  } catch (e) {
    setLoading(false);
    showResult({ correct: false, error: 'Connection error' });
  }
}

function showResult(data) {
  const zone        = document.getElementById('resultZone');
  const success     = document.getElementById('resultSuccess');
  const errBlock    = document.getElementById('resultError');
  const sqlErrBlock = document.getElementById('resultSqlError');

  zone.classList.remove('hidden');
  success.classList.add('hidden');
  errBlock.classList.add('hidden');
  sqlErrBlock.classList.add('hidden');

  if (data.error) {
    document.getElementById('sqlErrorText').textContent = data.error;
    sqlErrBlock.classList.remove('hidden');
    if (data.sql_error) incrementCounter('.score-errors');
    return;
  }

  if (data.correct) {
    document.getElementById('successText').textContent = getCompliment(USER_NAME);
    success.classList.remove('hidden');
    confetti();
    incrementCounter('.score-correct');
    // Disable Check Result and auto-advance after 1 s
    const btnCheck = document.getElementById('btnCheck');
    btnCheck.disabled = true;
    btnCheck.textContent = 'Next in 1s…';
    setTimeout(nextExercise, 1000);
  } else {
    errBlock.classList.remove('hidden');
  }
}

// ── Show / hide answer toggle ─────────────────────────
let _answerLoaded = false;

async function showAnswer() {
  const btn  = document.getElementById('btnReveal');
  const zone = document.getElementById('answerZone');

  // If already visible — hide it
  if (!zone.classList.contains('hidden')) {
    zone.classList.add('hidden');
    btn.textContent = '👁 Reveal Answer';
    return;
  }

  // If already fetched — just show again
  if (_answerLoaded) {
    zone.classList.remove('hidden');
    setTimeout(() => {
      answerEditor.refresh();
      zone.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 30);
    btn.textContent = '🙈 Hide Answer';
    return;
  }

  btn.disabled = true;
  btn.textContent = '👁 Loading...';

  try {
    const res  = await fetch('/show-answer', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ exercise_id: EXERCISE_ID }),
    });
    const data = await res.json();
    if (data.solution) {
      answerEditor.setValue(data.solution);
      zone.classList.remove('hidden');
      // CodeMirror needs a tick after element becomes visible to render correctly
      setTimeout(() => {
        answerEditor.refresh();
        zone.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }, 30);
      _answerLoaded = true;
      incrementCounter('.score-revealed');
      btn.textContent = '🙈 Hide Answer';
    }
  } catch (e) {
    console.error('show answer error', e);
    btn.textContent = '👁 Reveal Answer';
  } finally {
    btn.disabled = false;
  }
}

// ── Next exercise ─────────────────────────────────────
async function nextExercise(skipped = false) {
  try {
    await fetch('/next', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ skipped }),
    });
  } catch (_) {}
  window.location.href = '/trainer';
}

// ── Skip ──────────────────────────────────────────────
function skipExercise() {
  nextExercise(true);
}

// ── Clear editor ──────────────────────────────────────
function clearEditor() {
  editor.setValue('');
  editor.focus();
  hideResult();
}

function hideResult() {
  document.getElementById('resultZone').classList.add('hidden');
  document.getElementById('answerZone').classList.add('hidden');
}

// ── Reset DB ──────────────────────────────────────────
async function resetDb() {
  const btn  = document.querySelector('.btn-reset-db');
  const orig = btn.textContent;
  btn.textContent = '↺ Resetting...';
  btn.disabled    = true;
  try {
    await fetch('/reset-db', { method: 'POST' });
    window.location.reload();
  } catch (e) {
    btn.textContent = orig;
    btn.disabled    = false;
  }
}

// ── Loading state ─────────────────────────────────────
function setLoading(on) {
  const btn = document.getElementById('btnCheck');
  if (on) {
    btn.textContent = 'Checking...';
    btn.disabled    = true;
  } else {
    btn.textContent = 'Check Result';
    btn.disabled    = false;
  }
}

function flashEmpty() {
  const cm = document.querySelector('.editor-wrap .CodeMirror');
  if (!cm) return;
  cm.style.borderColor = 'var(--error)';
  setTimeout(() => { cm.style.borderColor = ''; }, 800);
}

// ── Shutdown server ───────────────────────────────────
async function shutdownServer() {
  if (!confirm('Stop the server?')) return;
  try {
    await fetch('/shutdown', { method: 'POST' });
  } catch (_) {}
  document.body.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100vh;font-family:monospace;font-size:1.2rem;color:#8888aa;">Server stopped. You can close this tab.</div>';
}

// ── Mini confetti ─────────────────────────────────────
function confetti() {
  const colors = ['#4fc3f7', '#7c6af7', '#4caf80', '#ffa726', '#ef5350'];
  for (let i = 0; i < 40; i++) {
    const el = document.createElement('div');
    const rot = (Math.random() > 0.5 ? '' : '-') + Math.round(Math.random() * 360) + 'deg';
    el.style.cssText = `
      position:fixed;
      top:${Math.random() * 50}%;
      left:${Math.random() * 100}%;
      width:${6 + Math.round(Math.random() * 6)}px;
      height:${6 + Math.round(Math.random() * 6)}px;
      border-radius:${Math.random() > 0.5 ? '50%' : '2px'};
      background:${colors[Math.floor(Math.random() * colors.length)]};
      pointer-events:none;
      z-index:9999;
      animation: confettiFall ${0.7 + Math.random() * 1.2}s ease forwards;
      --rot: ${rot};
    `;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 2200);
  }
}

const _style = document.createElement('style');
_style.textContent = `
  @keyframes confettiFall {
    0%   { transform: translateY(0) rotate(0deg); opacity: 1; }
    100% { transform: translateY(130px) rotate(var(--rot, 360deg)); opacity: 0; }
  }
`;
document.head.appendChild(_style);
