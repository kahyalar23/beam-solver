const fs = require('fs');

const file1Path = 'c:/Users/Kahyalar/Desktop/beam-solver/static/index.html';
const file2Path = 'c:/Users/Kahyalar/Desktop/beam-solver/static/index_new.html';

const file1 = fs.readFileSync(file1Path, 'utf-8').split('\n');
const file2 = fs.readFileSync(file2Path, 'utf-8').split('\n');

console.log(`File 1 (index.html): ${file1.length} lines`);
console.log(`File 2 (index_new.html): ${file2.length} lines`);
console.log('\n' + '='.repeat(100));
console.log('UNIFIED DIFF WITH CONTEXT');
console.log('='.repeat(100) + '\n');

// Generate unified diff output
function generateDiff(lines1, lines2) {
  const contextSize = 3;
  let i = 0, j = 0;
  const diffLines = [];
  
  while (i < lines1.length || j < lines2.length) {
    if (i < lines1.length && j < lines2.length && lines1[i] === lines2[j]) {
      i++;
      j++;
    } else {
      // Found a mismatch - collect context and changes
      const hunkStart = i;
      const hunkNewStart = j;
      const changes = [];
      
      while ((i < lines1.length || j < lines2.length) && changes.length < 20) {
        if (i >= lines1.length) {
          changes.push({type: '+', line: lines2[j], num: j + 1});
          j++;
        } else if (j >= lines2.length) {
          changes.push({type: '-', line: lines1[i], num: i + 1});
          i++;
        } else if (lines1[i] === lines2[j]) {
          break;
        } else {
          changes.push({type: '-', line: lines1[i], num: i + 1});
          i++;
          if (j < lines2.length && lines1[i] === lines2[j]) break;
          changes.push({type: '+', line: lines2[j], num: j + 1});
          j++;
        }
      }
      
      for (const change of changes) {
        diffLines.push(`${change.type} L${change.num}: ${change.line}`);
      }
      diffLines.push('');
    }
  }
  
  return diffLines;
}

const diffs = generateDiff(file1, file2);
for (const line of diffs) {
  console.log(line);
}

console.log('\n' + '='.repeat(100));
console.log(`Total diff output lines: ${diffs.length}`);
