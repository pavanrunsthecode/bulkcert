from flask import Flask, request, render_template, send_file
import requests
import zipfile
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def show_form():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def submit_form():
    jwtvalue = request.form["jwtvalue"]
    ids_str = request.form["ids"]
    ids = ids_str.split()  # split by whitespace
    ids_str = ','.join(ids)  # join with a comma

    zip_filename = "certificates.zip"
    with zipfile.ZipFile(zip_filename, mode='w') as certificates_zip:
        # Initialize an error message variable
        error_message = None

        for id in ids:
            url = f"https://api.go1.co/exim/enrollment/{id}/pdf?jwt={jwtvalue}"
            response = requests.get(url)
            if response.status_code == 200 and response.headers.get("content-type") == "application/pdf":
                pdf_filename = str(id) + ".pdf"
                with open(pdf_filename, "wb") as pdf_file:
                    pdf_file.write(response.content)
                    print(pdf_filename + " saved successfully")
                certificates_zip.write(pdf_filename)
                os.remove(pdf_filename)
            else:
                error_message = "Error occurred while retrieving the PDF file for ID " + str(id)
                break  # Exit the loop on the first error

        if error_message:
            return (
                f"<script>"
                f"alert('{error_message}');"
                f"window.location.href = '/';"  # Redirect back to the form page
                f"</script>"
            )

        # Return success message and send the ZIP file to the user
        return "<br><br><br><div style='text-align: center !important; color: green; font-size: 1.2em; margin-top: 50px;'>\
        <h2><p>Thank you for submitting the form!</p>\
        <p>Your certificates are ready and have been downloaded as a ZIP file.</p>\
        <p>Please check the root folder of this project to find the file named 'certificates.zip'.</p></h2>\
        </div>"
        # Alternatively, you can use the following statement to send the ZIP file directly to the user:
        #return send_file(zip_filename, mimetype='zip', as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
