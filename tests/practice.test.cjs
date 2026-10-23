const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const content = JSON.parse(fs.readFileSync(path.join(root, 'content/2025-maths-advanced.json'), 'utf8'));
const code = fs.readFileSync(path.join(root, 'assets/practice/practice.js'), 'utf8');

// Small DOM boundary fake: exercise the actual page script without browser dependencies.
class Element {
  constructor() {
    this.listeners = new Map();
    this.attributes = {};
    this.children = {};
    this.dataset = {};
    this.hidden = false;
    this.value = '';
    this.textContent = '';
    this.classList = { toggle() {} };
    this._open = false;
  }
  addEventListener(event, callback) {
    const callbacks = this.listeners.get(event) ?? [];
    callbacks.push(callback);
    this.listeners.set(event, callbacks);
  }
  emit(event) { for (const callback of this.listeners.get(event) ?? []) callback(); }
  setAttribute(name, value) { this.attributes[name] = value; }
  querySelector(selector) { return this.children[selector]; }
  get open() { return this._open; }
  set open(value) {
    if (this._open === value) return;
    this._open = value;
    this.emit('toggle');
  }
  closest() { return this; }
  scrollIntoView() {}
}

function createCard(part) {
  const card = new Element();
  card.id = `q${part.number}${part.part}`;
  card.dataset = { tags: JSON.stringify(part.tags), section: part.number <= 10 ? 'I' : 'II' };
  for (const selector of ['details', '.timer-value', '.timer-status', '.timer-toggle', '.timer-reset', '.question-number a', '.timer-controls']) {
    card.children[selector] = new Element();
  }
  card.children['.question-number a'].textContent = card.id;
  return card;
}

function setup() {
  let now = 0;
  let tick;
  const cards = content.map(createCard);
  const tags = [...new Set(content.flatMap((part) => part.tags))].map((tag) => {
    const button = new Element();
    button.dataset.tag = tag;
    return button;
  });
  const ids = Object.fromEntries(['section-filter', 'result-count', 'empty-state', 'clear-filters', 'empty-clear', 'total-time', 'total-time-panel'].map((id) => [id, new Element()]));
  ids['section-filter'].value = 'all';
  const sections = ['I', 'II'].map((name) => {
    const section = new Element();
    section.querySelector = () => cards.find((card) => card.dataset.section === name && !card.hidden);
    return section;
  });
  const document = new Element();
  document.querySelectorAll = (selector) => ({ '.question-card': cards, '.tag-filter': tags, '.question-section': sections })[selector];
  document.querySelector = () => new Element();
  document.getElementById = (id) => ids[id] ?? cards.find((card) => card.id === id);
  const window = new Element();
  const location = { hash: '' };
  vm.runInNewContext(code, { document, window, location, performance: { now: () => now }, setInterval: (callback) => { tick = callback; } });
  return { cards, tags, ids, document, window, location, sections, advance(milliseconds) { now += milliseconds; tick(); } };
}

function cardById(state, id) { return state.cards.find((card) => card.id === id); }
function output(card) { return card.querySelector('.timer-value').value; }
function clickTag(state, tag) { state.tags.find((button) => button.dataset.tag === tag).emit('click'); }

test('all paper parts are present with tags and short explanations, totalling 100 marks', () => {
  const expected = Array.from({ length: 10 }, (_, i) => `${i + 1}`);
  const suffixes = { 11: 'ab', 14: 'abcd', 15: 'abc', 16: 'ab', 17: 'abc', 21: 'ab', 23: 'ab', 25: 'abc', 26: 'ab', 27: 'abc', 28: 'ab', 29: 'abc' };
  for (let n = 11; n <= 31; n += 1) {
    for (const part of suffixes[n] ?? ['']) expected.push(`${n}${part}`);
  }
  assert.deepEqual(content.map((part) => `${part.number}${part.part}`), expected);
  assert.equal(content.reduce((sum, part) => sum + part.marks, 0), 100);
  assert.equal(content.slice(0, 10).map((part) => part.answer[0]).join(''), 'BADCB CADBC'.replaceAll(' ', ''));
  for (const part of content) {
    assert.ok(part.tags.length > 0 && part.steps.length > 0 && part.answer.length > 0);
    assert.ok(part.page >= 2 && part.page <= 37);
    assert.ok(part.steps.join(' ').split(/\s+/).length < 150, `${part.number}${part.part} should stay concise`);
  }
});

test('opening another solution pauses the previous timer and totals time once', () => {
  const state = setup();
  const first = cardById(state, 'q1');
  const second = cardById(state, 'q2');
  first.querySelector('details').open = true;
  state.advance(6100);
  assert.equal(output(first), '00:06');
  second.querySelector('details').open = true;
  state.advance(4000);
  assert.equal(output(first), '00:06');
  assert.equal(first.querySelector('details').open, true);
  assert.equal(first.querySelector('.timer-status').textContent, 'Paused');
  assert.equal(output(second), '00:04');
  assert.equal(state.ids['total-time'].value, '00:10');
  first.querySelector('.timer-toggle').emit('click');
  state.advance(2000);
  assert.equal(output(first), '00:08');
  assert.equal(output(second), '00:04');
  assert.equal(state.ids['total-time'].value, '00:12');
});

test('pause, close and reset retain the correct cumulative session total', () => {
  const state = setup();
  const card = state.cards[0];
  card.querySelector('details').open = true;
  state.advance(5000);
  card.querySelector('.timer-toggle').emit('click');
  state.advance(9000);
  assert.equal(output(card), '00:05');
  assert.equal(state.ids['total-time'].value, '00:05');
  card.querySelector('.timer-toggle').emit('click');
  state.advance(3000);
  card.querySelector('.timer-reset').emit('click');
  assert.equal(output(card), '00:00');
  assert.equal(state.ids['total-time'].value, '00:08');
  state.advance(2000);
  card.querySelector('details').open = false;
  state.advance(5000);
  assert.equal(output(card), '00:02');
  assert.equal(state.ids['total-time'].value, '00:10');
  card.querySelector('.timer-reset').emit('click');
  assert.equal(output(card), '00:00');
  assert.equal(state.ids['total-time'].value, '00:10');
});

test('hidden tabs pause time; only the previously running timer resumes', () => {
  const state = setup();
  state.cards[0].querySelector('details').open = true;
  state.advance(3000);
  state.cards[1].querySelector('details').open = true;
  state.advance(2000);
  state.document.hidden = true;
  state.document.emit('visibilitychange');
  state.advance(60000);
  assert.equal(state.ids['total-time'].value, '00:05');
  state.document.hidden = false;
  state.document.emit('visibilitychange');
  state.advance(1000);
  assert.equal(output(state.cards[0]), '00:03');
  assert.equal(output(state.cards[1]), '00:03');
  assert.equal(state.ids['total-time'].value, '00:06');
  state.cards[1].querySelector('.timer-toggle').emit('click');
  state.document.hidden = true;
  state.document.emit('visibilitychange');
  state.document.hidden = false;
  state.document.emit('visibilitychange');
  state.advance(3000);
  assert.equal(state.ids['total-time'].value, '00:06');
});

test('topic union, section intersections, empty results and clearing work', () => {
  const state = setup();
  clickTag(state, 'Conditional probability');
  assert.deepEqual(state.cards.filter((card) => !card.hidden).map((card) => card.id), ['q19']);
  clickTag(state, 'Financial maths');
  assert.deepEqual(state.cards.filter((card) => !card.hidden).map((card) => card.id), ['q17a', 'q17b', 'q17c', 'q19', 'q20']);
  state.ids['section-filter'].value = 'I';
  state.ids['section-filter'].emit('change');
  assert.equal(state.ids['empty-state'].hidden, false);
  assert.ok(state.sections.every((section) => section.hidden));
  state.ids['empty-clear'].emit('click');
  assert.equal(state.cards.filter((card) => !card.hidden).length, 50);
  assert.ok(state.sections.every((section) => !section.hidden));
  assert.ok(state.tags.every((tag) => tag.attributes['aria-pressed'] === 'false'));
});

test('filtering an active solution stops its timer and does not reveal answers on clear', () => {
  const state = setup();
  state.cards[0].querySelector('details').open = true;
  state.advance(3000);
  clickTag(state, 'Integration');
  state.advance(5000);
  assert.equal(state.ids['total-time'].value, '00:03');
  assert.equal(state.cards[0].querySelector('details').open, false);
  state.ids['clear-filters'].emit('click');
  state.advance(3000);
  assert.equal(state.ids['total-time'].value, '00:03');
});

test('a question deep link clears incompatible filters without starting time', () => {
  const state = setup();
  clickTag(state, 'Integration');
  state.location.hash = '#q1';
  state.window.emit('hashchange');
  assert.equal(state.cards[0].hidden, false);
  assert.equal(state.cards[0].querySelector('details').open, false);
  state.advance(3000);
  assert.equal(state.ids['total-time'].value, '00:00');
});

test('published papers include every marked section and link to their own official PDF', () => {
  const papers = [
    { slug: '2025-maths-extension-1', parts: 34, marks: 70, questions: 14, written: [15, 14, 16, 15], key: 'ABBCDDAABC' },
    { slug: '2026-maths-advanced', parts: 52, marks: 100, questions: 33, written: [2, 4, 4, 2, 2, 4, 3, 4, 3, 3, 5, 3, 4, 4, 2, 5, 4, 4, 6, 7, 4, 3, 8], key: 'CDBDAABCAD' },
    { slug: '2026-maths-extension-2', parts: 48, marks: 100, questions: 16, written: [15, 15, 14, 15, 15, 16], key: 'ABDDBCCBAC' },
  ];
  for (const paper of papers) {
    const parts = JSON.parse(fs.readFileSync(path.join(root, `content/${paper.slug}.json`), 'utf8'));
    const page = fs.readFileSync(path.join(root, `practice/${paper.slug}/index.html`), 'utf8');
    assert.equal(parts.length, paper.parts, paper.slug);
    assert.equal(parts.reduce((sum, part) => sum + part.marks, 0), paper.marks);
    assert.equal(new Set(parts.map((part) => `q${part.number}${part.part}`)).size, parts.length);
    assert.deepEqual([...new Set(parts.map((part) => part.number))], Array.from({ length: paper.questions }, (_, index) => index + 1));
    assert.deepEqual(Array.from({ length: paper.questions - 10 }, (_, index) => parts.filter((part) => part.number === index + 11).reduce((sum, part) => sum + part.marks, 0)), paper.written);
    assert.equal(parts.filter((part) => part.number <= 10).map((part) => part.answer[0]).join(''), paper.key);
    assert.equal((page.match(/class="question-card"/g) ?? []).length, parts.length);
    assert.ok(page.includes(`${paper.slug.replace('maths-', 'hsc-maths-')}.pdf#page=`));
    assert.ok(page.includes('id="total-time"'));
    assert.ok(parts.every((part) => part.steps.length > 0 && part.tags.length > 0 && part.page > 0 && part.answer));
  }
});
