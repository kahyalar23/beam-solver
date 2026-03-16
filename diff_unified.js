#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const file1Path = 'c:/Users/Kahyalar/Desktop/beam-solver/static/index.html';
const file2Path = 'c:/Users/Kahyalar/Desktop/beam-solver/static/index_new.html';

const file1 = fs.readFileSync(file1Path, 'utf-8').split('\n');
const file2 = fs.readFileSync(file2Path, 'utf-8').split('\n');

console.log(`File 1 (index.html): ${file1.length} lines`);
console.log(`File 2 (index_new.html): ${file2.length} lines`);
console.log('\n' + '='.repeat(100));
console.log('UNIFIED DIFF');
console.log('='.repeat(100) + '\n');

// Simple diff output
const output = [];

let i = 0, j = 0;
while (i < file1.length || j < file2.length) {
  if (i < file1.length && j < file2.length && file1[i] === file2[j]) {
    i++;
    j++;
  } else if ((i < file1.length && j >= file2.length) || 
             (i < file1.length && j < file2.length && file1[i] !== file2[j])) {
    // Line only in file1
    output.push(`- ${i+1}: ${file1[i]}`);
    i++;
  } else {
    // Line only in file2
    output.push(`+ ${j+1}: ${file2[j]}`);
    j++;
  }
}

// Group into hunks and display
let diffStart = -1;
const hunks = [];
for (let k = 0; k < output.length; k++) {
  if (output[k].startsWith('+') || output[k].startsWith('-')) {
    if (diffStart === -1) diffStart = k;
  } else if (diffStart !== -1) {
    hunks.push({start: diffStart, end: k});
    diffStart = -1;
  }
}
if (diffStart !== -1) hunks.push({start: diffStart, end: output.length});

// Print hunks with context
for (const hunk of hunks) {
  const contextSize = 3;
  const hunkStart = Math.max(0, hunk.start - contextSize);
  const hunkEnd = Math.min(output.length, hunk.end + contextSize);
  
  console.log(`\n=== HUNK ${hunks.indexOf(hunk) + 1} ===`);
  for (let i = hunkStart; i < hunkEnd; i++) {
    console.log(output[i]);
  }
}

console.log('\n' + '='.repeat(100));
console.log(`Total differences: ${output.filter(l => l.startsWith('+') || l.startsWith('-')).length} lines`);
console.log('='.repeat(100));
