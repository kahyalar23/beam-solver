import difflib

with open(r'c:\Users\Kahyalar\Desktop\beam-solver\static\index.html', 'r', encoding='utf-8') as f:
    file1_lines = f.readlines()

with open(r'c:\Users\Kahyalar\Desktop\beam-solver\static\index_new.html', 'r', encoding='utf-8') as f:
    file2_lines = f.readlines()

print(f'File 1 (index.html): {len(file1_lines)} lines')
print(f'File 2 (index_new.html): {len(file2_lines)} lines')
print()
print('='*80)
print('UNIFIED DIFF OUTPUT:')
print('='*80)
print()

diff = list(difflib.unified_diff(
    file1_lines, 
    file2_lines,
    fromfile='index.html',
    tofile='index_new.html',
    lineterm='',
    n=3
))

print(f'Total diff lines: {len(diff)}')
print()
for line in diff:
    print(line)
