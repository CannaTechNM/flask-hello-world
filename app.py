import os
from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from flask_wtf.file import FileField
from pdfrw import PdfReader, PdfWriter
from flask.helpers import send_file

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
csrf = CSRFProtect(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class SignatureForm(FlaskForm):
    signature = FileField('Signature', validators=[FileRequired()])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SignatureForm()

    if form.validate_on_submit():
        signature = form.signature.data
        pdf_file = 'sample.pdf'  # Path to the existing PDF file

        # Save the uploaded signature
        signature_path = os.path.join(app.config['UPLOAD_FOLDER'], 'signature.png')
        signature.save(signature_path)

        # Add signature to the PDF
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.pdf')
        add_signature_to_pdf(pdf_file, signature_path, output_path)

        return send_file(output_path, as_attachment=True)

    return render_template('index.html', form=form)


def add_signature_to_pdf(pdf_file, signature_file, output_file):
    # Read the existing PDF file
    template_pdf = PdfReader(pdf_file)
    page = template_pdf.pages[0]  # Assuming the signature will be added to the first page

    # Load the signature image
    signature_pdf = PdfReader(signature_file)
    signature_page = signature_pdf.pages[0]

    # Add the signature as an annotation to the page
    page.Annots.append(signature_page)

    # Write the modified PDF to a new file
    writer = PdfWriter()
    writer.add_page(page)
    writer.write(output_file)


if __name__ == '__main__':
    app.run(debug=True)

