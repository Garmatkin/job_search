import PyPDF2

# Open the PDF file
pdf_file = '/home/ubuntu/upload/Ivan_Dobrovolskyi_VP_PT.pdf'
pdf_reader = PyPDF2.PdfReader(pdf_file)

# Extract text from all pages
text = ""
for page in pdf_reader.pages:
    text += page.extract_text()

# Save the extracted text to a file
with open('/home/ubuntu/resume_analysis/resume_text.txt', 'w', encoding='utf-8') as f:
    f.write(text)

print("PDF extraction completed successfully")
