#!/usr/bin/env python3
import difflib

# Read the files
with open(r'c:\Users\Kahyalar\Desktop\beam-solver\static\index.html', 'r', encoding='utf-8') as f:
    file1_lines = f.readlines()

with open(r'c:\Users\Kahyalar\Desktop\beam-solver\static\index_new.html', 'r', encoding='utf-8') as f:
    file2_lines = f.readlines()

print(f"File 1 (index.html): {len(file1_lines)} lines")
print(f"File 2 (index_new.html): {len(file2_lines)} lines")
print("\n" + "="*80)
print("UNIFIED DIFF OUTPUT:")
print("="*80 + "\n")

# Generate unified diff with context lines
diff = difflib.unified_diff(
    file1_lines, 
    file2_lines,
    fromfile='index.html',
    tofile='index_new.html',
    lineterm='',
    n=3  # 3 lines of context
)

# Print all diff output
diff_lines = list(diff)
print(f"Total diff lines: {len(diff_lines)}\n")
for line in diff_lines:
    print(line)
