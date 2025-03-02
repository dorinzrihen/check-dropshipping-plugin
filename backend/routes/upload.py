from flask import Blueprint, request, jsonify
from PIL import Image
import io
import os

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image = request.files["image"]
    image_bytes = io.BytesIO(image.read())

    try:
        img = Image.open(image_bytes)
    except Exception as e:
        return jsonify({"error": "Invalid image format", "details": str(e)}), 400

    # Get original size
    original_width, original_height = img.size

    # Resize while maintaining aspect ratio
    img.thumbnail((800, 800))  # Resize but keep aspect ratio

    # Save processed image in memory
    processed_image_bytes = io.BytesIO()
    img.save(processed_image_bytes, format="PNG")
    processed_image_bytes.seek(0)  # Reset file pointer

    # Save the image to the upload folder
    save_path = os.path.join(os.getcwd(), image.filename)
    img.save(save_path, format="PNG")

    return jsonify({
        "message": "Image processed and saved",
        "original_size": f"{original_width}x{original_height}",
        "new_size": f"{img.width}x{img.height}",
        "saved_path": save_path
    }), 200
