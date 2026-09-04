import { readFileSync, writeFileSync } from 'node:fs';

const input = process.argv[2];
const output = process.argv[3];

if (!input || !output) {
  console.error('Usage: node scripts/minify-js.mjs <input> <output>');
  process.exit(1);
}

const source = readFileSync(input, 'utf8');
let out = '';
let i = 0;
let last = '';

const isWord = (ch) => /[A-Za-z0-9_$]/.test(ch || '');
const needsSpace = (a, b) => isWord(a) && isWord(b);
const regexCanStartAfter = (ch) => !ch || /[({[=,:;!&|?+\-*~^<>]/.test(ch);

function append(ch) {
  if (ch) {
    out += ch;
    if (!/\s/.test(ch)) last = ch;
  }
}

function readString(quote) {
  append(source[i++]);
  while (i < source.length) {
    const ch = source[i++];
    append(ch);
    if (ch === '\\') {
      append(source[i++]);
    } else if (ch === quote) {
      break;
    }
  }
}

function readTemplate() {
  append(source[i++]);
  while (i < source.length) {
    const ch = source[i++];
    append(ch);
    if (ch === '\\') {
      append(source[i++]);
    } else if (ch === '`') {
      break;
    }
  }
}

function readRegex() {
  append(source[i++]);
  let inClass = false;
  while (i < source.length) {
    const ch = source[i++];
    append(ch);
    if (ch === '\\') {
      append(source[i++]);
    } else if (ch === '[') {
      inClass = true;
    } else if (ch === ']') {
      inClass = false;
    } else if (ch === '/' && !inClass) {
      while (/[A-Za-z]/.test(source[i] || '')) append(source[i++]);
      break;
    }
  }
}

while (i < source.length) {
  const ch = source[i];
  const next = source[i + 1];

  if (ch === '"' || ch === "'") {
    readString(ch);
    continue;
  }
  if (ch === '`') {
    readTemplate();
    continue;
  }
  if (ch === '/' && next === '/') {
    i += 2;
    while (i < source.length && source[i] !== '\n') i++;
    continue;
  }
  if (ch === '/' && next === '*') {
    i += 2;
    while (i < source.length && !(source[i] === '*' && source[i + 1] === '/')) i++;
    i += 2;
    continue;
  }
  if (ch === '/' && regexCanStartAfter(last)) {
    readRegex();
    continue;
  }
  if (/\s/.test(ch)) {
    let j = i + 1;
    while (j < source.length && /\s/.test(source[j])) j++;
    if (needsSpace(last, source[j])) append(' ');
    i = j;
    continue;
  }

  append(ch);
  i++;
}

writeFileSync(output, out.trim() + '\n');
