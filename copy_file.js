const fs = require('fs');
const path = require('path');

const sourceFile = 'c:\\Users\\Kahyalar\\Desktop\\beam-solver\\static\\index_new.html';
const destFile = 'c:\\Users\\Kahyalar\\Desktop\\beam-solver\\static\\index.html';

const requiredStrings = [
  'TrussCanvas',
  'TrussTab',
  'BeamTab',
  'gaussSolve',
  'computeBeam',
  'function App()'
];

try {
  // Step 1: Copy contents from index_new.html to index.html
  console.log('Step 1: Copying index_new.html to index.html...');
  const content = fs.readFileSync(sourceFile, 'utf-8');
  fs.writeFileSync(destFile, content, 'utf-8');
  console.log('OK: Successfully copied index_new.html to index.html');
  
  // Step 2: Delete index_new.html
  console.log('Step 2: Deleting index_new.html...');
  fs.unlinkSync(sourceFile);
  console.log('OK: Successfully deleted index_new.html');
  
  // Step 3: Verify that index.html contains all required strings
  console.log('Step 3: Verifying required strings in index.html...');
  const fileContent = fs.readFileSync(destFile, 'utf-8');
  
  const missingStrings = [];
  for (const requiredStr of requiredStrings) {
    if (!fileContent.includes(requiredStr)) {
      missingStrings.push(requiredStr);
    } else {
      console.log('  OK: Found: ' + requiredStr);
    }
  }
  
  if (missingStrings.length > 0) {
    console.log('\nFAILURE: The following strings were NOT found in index.html:');
    for (const s of missingStrings) {
      console.log('  - ' + s);
    }
    process.exit(1);
  } else {
    console.log('\nSUCCESS: All required strings found in index.html!');
    console.log('All operations completed successfully');
    process.exit(0);
  }
} catch (e) {
  console.log('FAILURE: An error occurred: ' + e.message);
  console.log(e);
  process.exit(1);
}
