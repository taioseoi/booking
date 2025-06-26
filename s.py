import os

folder_path = '/Users/kamontat.s/Desktop/work/routes'  # แก้เป็นโฟลเดอร์จริง
output_file = 'all_code_combined_routes.txt'

with open(output_file, 'w', encoding='utf-8') as outfile:
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    outfile.write(f'\n=== {file_path} ===\n')  # ใส่หัวไฟล์ให้ดูว่าเป็นโค้ดจากไหน
                    outfile.write(f.read())
            except Exception as e:
                print(f"Skip {file_path}: {e}")