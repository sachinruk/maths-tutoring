// Compile original solution text to accessible, static KaTeX HTML + MathML.
const fs = require('node:fs');
const katex = require('../assets/vendor/katex/katex.min.js');

function escapeHtml(text) {
  return text.replace(/[&<>"']/g, (character) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  })[character]);
}

function renderText(text) {
  const expression = /\\\[([\s\S]*?)\\\]|\\\(([\s\S]*?)\\\)/g;
  let output = '';
  let cursor = 0;
  for (const match of text.matchAll(expression)) {
    output += escapeHtml(text.slice(cursor, match.index));
    output += katex.renderToString(match[1] ?? match[2], {
      displayMode: match[1] !== undefined,
      throwOnError: true,
      strict: 'error',
      trust: false,
      output: 'htmlAndMathml',
    });
    cursor = match.index + match[0].length;
  }
  return output + escapeHtml(text.slice(cursor));
}

const texts = JSON.parse(fs.readFileSync(0, 'utf8'));
process.stdout.write(JSON.stringify(texts.map(renderText)));
