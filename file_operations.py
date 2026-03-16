import os
import shutil

# Paths
source_file = r"c:\Users\Kahyalar\Desktop\beam-solver\static\index_new.html"
dest_file = r"c:\Users\Kahyalar\Desktop\beam-solver\static\index.html"

# Required strings to verify
required_strings = ["TrussCanvas", "TrussTab", "BeamTab", "gaussSolve", "computeBeam", "function App()"]

try:
    # Step 1: Copy contents from index_new.html to index.html (overwrite)
    print("Step 1: Copying index_new.html to index.html...")
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    with open(dest_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK: Successfully copied index_new.html to index.html")
    
    # Step 2: Delete index_new.html
    print("Step 2: Deleting index_new.html...")
    os.remove(source_file)
    print("OK: Successfully deleted index_new.html")
    
    # Step 3: Verify that index.html contains all required strings
    print("Step 3: Verifying required strings in index.html...")
    with open(dest_file, 'r', encoding='utf-8') as f:
        file_content = f.read()
    
    missing_strings = []
    for required_str in required_strings:
        if required_str not in file_content:
            missing_strings.append(required_str)
        else:
            print("  OK: Found: " + required_str)
    
    if missing_strings:
        print("FAILURE: The following strings were NOT found in index.html:")
        for s in missing_strings:
            print("  - " + s)
        exit(1)
    else:
        print("\nSUCCESS: All required strings found in index.html!")
        print("All operations completed successfully")
        exit(0)

except Exception as e:
    print("FAILURE: An error occurred: " + str(e))
    exit(1)
