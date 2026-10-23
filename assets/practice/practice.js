// Each solution owns its timer. A monotonic clock avoids interval drift.
const cards = [...document.querySelectorAll('.question-card')];
const selectedTags = new Set();
const sectionFilter = document.getElementById('section-filter');
const timers = new Map();
const totalTimer = { elapsed: 0, startedAt: null };
const totalOutput = document.getElementById('total-time');

function paintTotal() {
  totalOutput.value = formatTime(elapsedTime(totalTimer));
}

function elapsedTime(timer) {
  return timer.elapsed + (timer.startedAt === null ? 0 : performance.now() - timer.startedAt);
}

function formatTime(milliseconds) {
  const totalSeconds = Math.floor(milliseconds / 1000);
  const minutes = Math.floor(totalSeconds / 60).toString().padStart(2, '0');
  const seconds = (totalSeconds % 60).toString().padStart(2, '0');
  return `${minutes}:${seconds}`;
}

function paintTimer(timer) {
  const running = timer.startedAt !== null;
  timer.output.value = formatTime(elapsedTime(timer));
  timer.toggle.textContent = running ? 'Pause' : 'Resume';
  timer.toggle.setAttribute('aria-label', `${running ? 'Pause' : 'Resume'} timer for ${timer.label}`);
  timer.toggle.disabled = !timer.details.open;
  timer.status.textContent = running ? 'Running' : (timer.hasStarted ? 'Paused' : 'Not started');
  timer.card.classList.toggle('timer-running', running);
}

function pauseTimer(timer) {
  if (timer.startedAt !== null) {
    totalTimer.elapsed = elapsedTime(totalTimer);
    totalTimer.startedAt = null;
  }
  timer.elapsed = elapsedTime(timer);
  timer.startedAt = null;
  paintTimer(timer);
  paintTotal();
}

function startTimer(timer) {
  if (!timer.details.open || timer.card.hidden || document.hidden) return;
  for (const other of timers.values()) {
    if (other === timer) continue;
    other.resumeOnVisible = false;
    if (other.startedAt !== null) pauseTimer(other);
  }
  if (timer.startedAt === null) {
    timer.startedAt = performance.now();
    totalTimer.startedAt = timer.startedAt;
  }
  timer.hasStarted = true;
  paintTimer(timer);
  paintTotal();
}

function handleDisclosure(timer) {
  timer.resumeOnVisible = false;
  if (timer.details.open) startTimer(timer);
  else pauseTimer(timer);
}

function resetTimer(timer) {
  // Reset this part, but retain the time already spent in the session total.
  pauseTimer(timer);
  timer.elapsed = 0;
  timer.startedAt = null;
  timer.resumeOnVisible = false;
  timer.hasStarted = timer.details.open;
  if (timer.details.open) startTimer(timer);
  else paintTimer(timer);
}

function setupTimer(card) {
  const timer = {
    card,
    details: card.querySelector('details'),
    output: card.querySelector('.timer-value'),
    status: card.querySelector('.timer-status'),
    toggle: card.querySelector('.timer-toggle'),
    label: card.querySelector('.question-number a').textContent,
    elapsed: 0,
    startedAt: null,
    hasStarted: false,
    resumeOnVisible: false,
  };
  timers.set(card, timer);
  timer.details.addEventListener('toggle', () => handleDisclosure(timer));
  timer.toggle.addEventListener('click', () => {
    timer.resumeOnVisible = false;
    if (timer.startedAt === null) startTimer(timer);
    else pauseTimer(timer);
  });
  card.querySelector('.timer-reset').addEventListener('click', () => resetTimer(timer));
  card.querySelector('.timer-controls').hidden = false;
  paintTimer(timer);
}

function applyFilters() {
  let visible = 0;
  for (const card of cards) {
    const tags = JSON.parse(card.dataset.tags);
    const matchesTags = selectedTags.size === 0 || tags.some((tag) => selectedTags.has(tag));
    const matchesSection = sectionFilter.value === 'all' || card.dataset.section === sectionFilter.value;
    card.hidden = !(matchesTags && matchesSection);
    if (card.hidden) {
      const timer = timers.get(card);
      timer.resumeOnVisible = false;
      pauseTimer(timer);
      timer.details.open = false;
    } else visible += 1;
  }
  for (const section of document.querySelectorAll('.question-section')) {
    section.hidden = !section.querySelector('.question-card:not([hidden])');
  }
  document.getElementById('result-count').textContent = visible === cards.length
    ? `Showing all ${cards.length} question parts`
    : `Showing ${visible} of ${cards.length} question parts`;
  document.getElementById('empty-state').hidden = visible !== 0;
}

function clearFilters() {
  selectedTags.clear();
  sectionFilter.value = 'all';
  document.querySelectorAll('.tag-filter').forEach((button) => button.setAttribute('aria-pressed', 'false'));
  applyFilters();
}

function revealHashTarget() {
  const target = document.getElementById(location.hash.slice(1));
  const card = target?.closest('.question-card');
  if (!card) return;
  if (card.hidden) clearFilters();
  // Linking to a part does not reveal its answer or start its timer.
  card.scrollIntoView({ block: 'start' });
}

cards.forEach(setupTimer);
document.getElementById('total-time-panel').hidden = false;
document.querySelector('.filter-panel').hidden = false;
document.querySelectorAll('.tag-filter').forEach((button) => {
  button.addEventListener('click', () => {
    const tag = button.dataset.tag;
    if (selectedTags.has(tag)) selectedTags.delete(tag);
    else selectedTags.add(tag);
    button.setAttribute('aria-pressed', String(selectedTags.has(tag)));
    applyFilters();
  });
});
sectionFilter.addEventListener('change', applyFilters);
document.getElementById('clear-filters').addEventListener('click', clearFilters);
document.getElementById('empty-clear').addEventListener('click', clearFilters);
document.addEventListener('visibilitychange', () => {
  for (const timer of timers.values()) {
    if (document.hidden) {
      timer.resumeOnVisible = timer.startedAt !== null;
      pauseTimer(timer);
    } else if (timer.resumeOnVisible) {
      timer.resumeOnVisible = false;
      startTimer(timer);
    }
  }
});
window.addEventListener('pagehide', () => timers.forEach(pauseTimer));
window.addEventListener('hashchange', revealHashTarget);
setInterval(() => {
  for (const timer of timers.values()) {
    if (timer.startedAt !== null) timer.output.value = formatTime(elapsedTime(timer));
  }
  paintTotal();
}, 250);
revealHashTarget();
