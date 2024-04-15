import os

from flask import Flask, render_template, request, redirect, url_for, send_file

# importing thing from get info
from get_info import get_pdf_text, get_word_text, get_gmail, get_phone

# for xml file
import xlsxwriter

app = Flask(__name__)


@app.route('/')
def main():
    return render_template("index.html")

UPLOAD_FOLDER = 'static'
@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist("file")
        pdf_file =[]
        word_file =[]
        row = 1
        workbook = xlsxwriter.Workbook('sample.xls')
        start = ['id', 'name', 'mobile', 'email', 'text']

        worksheet = workbook.add_worksheet()
        worksheet.write_row(0, 0, start)
        for file in files:
            split_tup = os.path.splitext(file.filename)
            file_extension = split_tup[1]
            if file_extension =='.pdf':
                pdf_file.append(file.filename)
                # file.save(f"static/files/{file.filename}")
                file_text = get_pdf_text(file)
            elif file_extension =='.docx':
                word_file.append(file.filename)
                # file.save(f"static/files/{file.filename}")
                file_text = get_word_text(file)
            else:
                return f"<h1>unsupported file format {file_extension}</h1>"


            phone =get_phone(file_text)
            email = get_gmail(file_text)
            phone = ", ".join(phone)
            email = ", ".join(email)
            start = [row, file.filename, phone , email, file_text]
            worksheet.write_row(row, 0, start)
            row+=1
        workbook.close()

        return "<h1>Files Uploaded Successfully.!</h1><br> <a href='/download'>download</a>"
    return redirect(url_for('main'))


@app.route('/download')
def download():

    return send_file(path_or_file='sample.xls', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True) 