import os
import pandas as pd
import zipfile


zip_file = r'C:\Users\PavanRongali\Downloads\Python projects\Testpython\certificates.zip'


extracted_directory = r'C:\Users\PavanRongali\Downloads\Python projects\Testpython\extracted_pdfs'


csv_file = r'C:\Users\PavanRongali\Downloads\Python projects\Testpython\enrollment_data.csv'


new_zip_file = r'C:\Users\PavanRongali\Downloads\Python projects\Testpython\certificates_named.zip'

data = pd.read_csv(csv_file)

with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    for index, row in data.iterrows():
        enrollment_id = row['EnrollmentID']
        username = row['username']

        
        old_pdf_filename = f'{enrollment_id}.pdf'
        new_pdf_filename = f'{username}.pdf'

        if old_pdf_filename in zip_ref.namelist():
            
            zip_ref.extract(old_pdf_filename, extracted_directory)

            
            os.rename(os.path.join(extracted_directory, old_pdf_filename), os.path.join(extracted_directory, new_pdf_filename))

            print(f'Renamed {old_pdf_filename} to {new_pdf_filename}')


with zipfile.ZipFile(new_zip_file, 'w', zipfile.ZIP_DEFLATED) as new_zip:
    for root, _, files in os.walk(extracted_directory):
        for file in files:
            file_path = os.path.join(root, file)
            new_zip.write(file_path, os.path.relpath(file_path, extracted_directory))


for file in os.listdir(extracted_directory):
    file_path = os.path.join(extracted_directory, file)
    os.remove(file_path)


os.rmdir(extracted_directory)

print(f'Renamed PDFs have been archived in {new_zip_file}')
