import shutil
import os

# 1. Copy index_new.html to index.html (overwrite)
src = r'c:\Users\Kahyalar\Desktop\beam-solver\static\index_new.html'
dst = r'c:\Users\Kahyalar\Desktop\beam-solver\static\index.html'
shutil.copy2(src, dst)
print(f"✓ Copied {src} to {dst}")

# 2. Delete index_new.html
os.remove(src)
print(f"✓ Deleted {src}")

# 3. Delete generated diff files if they exist
files_to_delete = [
    r'c:\Users\Kahyalar\Desktop\beam-solver\README_DIFF.txt',
    r'c:\Users\Kahyalar\Desktop\beam-solver\DIFF_INDEX.md',
    r'c:\Users\Kahyalar\Desktop\beam-solver\DIFF_SUMMARY.md',
    r'c:\Users\Kahyalar\Desktop\beam-solver\DETAILED_DIFF.md',
    r'c:\Users\Kahyalar\Desktop\beam-solver\CODE_DIFF_DETAILED.md',
    r'c:\Users\Kahyalar\Desktop\beam-solver\DIFF_VISUAL.md'
]

for file in files_to_delete:
    if os.path.exists(file):
        os.remove(file)
        print(f"✓ Deleted {file}")
    else:
        print(f"  Skipped (not found): {file}")

# 4. Print line count of the new index.html
with open(dst, 'r', encoding='utf-8') as f:
    line_count = len(f.readlines())
print(f"\n✓ Line count of {dst}: {line_count} lines")
