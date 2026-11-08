const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const DATA_DIR = path.join(ROOT, 'data');

function walk(dir) {
  let out = [];
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) out = out.concat(walk(p));
    else if (e.isFile() && e.name.endsWith('.json')) out.push(p);
  }
  return out;
}

let ok = 0, fail = 0;
for (const f of walk(DATA_DIR)) {
  try {
    JSON.parse(fs.readFileSync(f, 'utf8'));
    console.log('OK  ', path.relative(ROOT, f));
    ok++;
  } catch (e) {
    console.error('FAIL', path.relative(ROOT, f), '-', e.message);
    fail++;
  }
}
console.log(`\nParsed ${ok + fail} JSON files: ${ok} ok, ${fail} failed.`);
process.exit(fail ? 1 : 0);
