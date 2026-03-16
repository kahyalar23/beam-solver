const fs = require('fs');
const path = require('path');
const base = 'c:\\Users\\Kahyalar\\Desktop\\beam-solver';
const files = [
  'static\\index_new.html',
  'README_DIFF.txt',
  'DIFF_INDEX.md',
  'DIFF_SUMMARY.md',
  'DETAILED_DIFF.md',
  'CODE_DIFF_DETAILED.md',
  'DIFF_VISUAL.md',
  'ANALYSIS_COMPLETE.txt',
  'cleanup_temps.bat',
  'compare_files.py',
  'copy_file.js',
  'delete_temps.py',
  'diff_script.py',
  'diff_simple.js',
  'diff_unified.js',
  'execute_diff.js',
  'exec_diff.py',
  'file_operations.py',
  'manage_files.py',
  'run_and_verify.bat',
  'run_and_verify.py',
  'run_delete.bat',
  'run_diff.bat',
  'run_diff.py',
  'run_diff_node.js',
  'run_script.bat',
  'simple_diff.py',
  'verify_copy.py',
  '_diff_output.txt',
  '_diff_temp.py',
  '_gen_diff.js',
  '_run_diff.bat',
  '_temp_diff_run.js',
];
let deleted = 0;
files.forEach(f => {
  const p = path.join(base, f);
  if (fs.existsSync(p)) {
    fs.unlinkSync(p);
    console.log('Deleted: ' + f);
    deleted++;
  }
});
// Self-delete
const self = path.join(base, '_delete_files.js');
if (fs.existsSync(self)) { fs.unlinkSync(self); deleted++; }
console.log(`\nDone: ${deleted} files cleaned up.`);
