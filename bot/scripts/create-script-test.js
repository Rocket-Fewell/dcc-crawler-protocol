#!/usr/bin/env node
/** Runs the spec's 10-item /create test script against fresh sandbox beta sessions and prints a report. */
import { runScript } from '../test/helpers/create-script.js';
const { results, realAlphaUnchanged, dir } = await runScript();
for (const r of results) console.log(`${r.pass ? 'PASS' : 'FAIL'}  ${String(r.n).padStart(2)}. ${r.name}\n        ${r.detail}`);
console.log(`\nreal alpha sessions/state.json unchanged: ${realAlphaUnchanged}; main sandbox: ${dir}`);
process.exit(results.every((r) => r.pass) && realAlphaUnchanged ? 0 : 1);
