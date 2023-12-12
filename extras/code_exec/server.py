import os
import shutil
import logging
from glob import iglob

from flask import Flask, request, abort, send_file

from code_executor import CodeExecutor

app = Flask("code_exec")

if __name__ == "__main__":
    logger = logging.getLogger("waitress")
    logger.setLevel(logging.INFO)
else:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)


IMAGE_PATH = "static/images"
DATA_PATH = "static/files"
CODE_PATH = "static/code"

code_exec = CodeExecutor(DATA_PATH, IMAGE_PATH, CODE_PATH)


@app.route("/", methods=["POST"])
def execute_code():
    """
    Execute provided code in a "safe" manner
    """

    # Load JSON data
    req = request.get_json()

    try:
        code = req["code"]
        logging.debug(f"Received code: {code}")
    except KeyError:
        abort(400, message="Missing required parameter")

    return code_exec.run(code)


@app.route("/image", methods=["GET", "DELETE"])
def list_images():
    """
    List existing images (and delete them)
    """

    image_list = [
        os.path.basename(image) for image in iglob(os.path.join(IMAGE_PATH, "*.png"))
    ]
    deleted = False

    if request.method == "DELETE":
        logging.info("Deleting all images")

        shutil.rmtree(IMAGE_PATH)
        os.mkdir(IMAGE_PATH)

        deleted = True

    return {
        "images": image_list,
        "deleted": deleted,
    }


@app.route("/image/<id>", methods=["GET"])
def serve_image(id: str):
    """
    Serve image file based on the given id
    """

    return send_file(os.path.join(IMAGE_PATH, f"{id}"), mimetype="image/png")


@app.route("/code", methods=["GET", "DELETE"])
def list_codes():
    """
    List existing Python files (and delete them)
    """

    code_list = [
        os.path.basename(code).rstrip(".py")
        for code in iglob(os.path.join(CODE_PATH, "*.py"))
    ]
    deleted = False

    if request.method == "DELETE":
        logging.info("Deleting all codes")

        shutil.rmtree(CODE_PATH)
        os.mkdir(CODE_PATH)

        deleted = True

    return {
        "codes": code_list,
        "deleted": deleted,
    }


@app.route("/code/<id>", methods=["GET"])
def serve_code(id: str):
    """
    Serve previously executed Python file based on the given id
    """

    return send_file(os.path.join(CODE_PATH, f"{id}.py"), mimetype="text/plain")


@app.route("/data", methods=["GET", "DELETE"])
def list_data():
    """
    List existing Python files (and delete them)
    """

    data_list = [os.path.basename(data) for data in iglob(os.path.join(DATA_PATH, "*"))]
    deleted = False

    if request.method == "DELETE":
        logging.info("Deleting all data")

        shutil.rmtree(DATA_PATH)
        os.mkdir(DATA_PATH)

        deleted = True

    return {"data": data_list, "deleted": deleted}


@app.route("/data/<id>", methods=["GET"])
def serve_data(id: str):
    """
    Serve previously uploaded data files based on the given id
    """

    return send_file(os.path.join(DATA_PATH, f"{id}"), mimetype="text/plain")


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=80)
