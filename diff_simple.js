const fs = require('fs');

// Read files
const file1 = fs.readFileSync('c:/Users/Kahyalar/Desktop/beam-solver/static/index.html', 'utf-8');
const file2 = fs.readFileSync('c:/Users/Kahyalar/Desktop/beam-solver/static/index_new.html', 'utf-8');

const lines1 = file1.split('\n');
const lines2 = file2.split('\n');

console.log(`File 1 (index.html): ${lines1.length} lines`);
console.log(`File 2 (index_new.html): ${lines2.length} lines`);
console.log('\n' + '='.repeat(80));
console.log('LINE-BY-LINE DIFF WITH CONTEXT');
console.log('='.repeat(80) + '\n');

// Simple unified diff implementation
let i = 0, j = 0;
let hunks = [];
let currentHunk = null;
const contextSize = 3;

function createHunk(oldStart, oldCount, newStart, newCount, lines) {
  return {
    oldStart: oldStart + 1,
    oldCount,
    newStart: newStart + 1,
    newCount,
    lines
  };
}

// Find differences
while (i < lines1.length || j < lines2.length) {
  if (i < lines1.length && j < lines2.length && lines1[i] === lines2[j]) {
    i++;
    j++;
  } else {
    // Found a difference
    let oldStart = Math.max(0, i - contextSize);
    let newStart = Math.max(0, j - contextSize);
    let oldLines = [], newLines = [];
    
    // Collect context before
    for (let k = oldStart; k < i; k++) {
      oldLines.push(' ' + lines1[k]);
      newLines.push(' ' + lines2[newStart + (k - oldStart)]);
    }
    
    // Collect the actual difference
    let oldEnd = i, newEnd = j;
    while ((oldEnd < lines1.length || newEnd < lines2.length) &&
           (oldEnd < i + 10 || newEnd < j + 10)) {
      if (oldEnd < lines1.length && (newEnd >= lines2.length || lines1[oldEnd] !== lines2[newEnd])) {
        oldLines.push('-' + lines1[oldEnd]);
        oldEnd++;
      } else if (newEnd < lines2.length && (oldEnd >= lines1.length || lines1[oldEnd] !== lines2[newEnd])) {
        newLines.push('+' + lines2[newEnd]);
        newEnd++;
      } else {
        break;
      }
    }
    
    // Collect context after
    for (let k = 0; k < contextSize && oldEnd < lines1.length && newEnd < lines2.length; k++) {
      oldLines.push(' ' + lines1[oldEnd + k]);
      newLines.push(' ' + lines2[newEnd + k]);
    }
    
    i = oldEnd;
    j = newEnd;
    
    console.log(`@@ -${oldStart + 1},${oldEnd - oldStart} +${newStart + 1},${newEnd - newStart} @@`);
    
    // Print the hunk
    let maxLen = Math.max(oldLines.length, newLines.length);
    for (let k = 0; k < maxLen; k++) {
      if (k < oldLines.length) console.log(oldLines[k]);
      if (k < newLines.length && newLines[k] !== oldLines[k]) console.log(newLines[k]);
    }
    console.log();
  }
}

console.log('='.repeat(80));
console.log('Diff complete!');
