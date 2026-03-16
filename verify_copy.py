import shutil

shutil.copy2(r'c:\Users\Kahyalar\Desktop\beam-solver\static\index_new.html', r'c:\Users\Kahyalar\Desktop\beam-solver\static\index.html')
print('Copy done')

f = open(r'c:\Users\Kahyalar\Desktop\beam-solver\static\index.html', 'r', encoding='utf-8')
lines = f.readlines()
f.close()

print(f'Line count: {len(lines)}')
print(f'Last line: {lines[-1].strip()}')
