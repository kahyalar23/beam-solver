import os

os.chdir(r'c:\Users\Kahyalar\Desktop\beam-solver')
files_to_delete = [
    '_diff_temp.py', '_diff_output.txt', '_gen_diff.js', '_run_diff.bat',
    'run_and_verify.bat', 'run_and_verify.py', 'run_diff.bat', 'run_diff.py',
    'run_diff_node.js', 'execute_diff.js', 'exec_diff.py', 'simple_diff.py'
]

deleted = []
not_found = []

for f in files_to_delete:
    if os.path.exists(f):
        try:
            os.remove(f)
            deleted.append(f)
            print(f'Deleted: {f}')
        except Exception as e:
            print(f'Error deleting {f}: {e}')
    else:
        not_found.append(f)

print(f'\nSummary:')
print(f'Deleted: {len(deleted)} files')
print(f'Not found: {len(not_found)} files')
if deleted:
    print(f'Files deleted: {", ".join(deleted)}')
if not_found:
    print(f'Files not found: {", ".join(not_found)}')
