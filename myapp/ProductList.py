# core/ProductList.py

import re
import google.generativeai as genai
from PIL import Image
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from dotenv import load_dotenv


# ==========================
# 1. Configure Gemini API
# ==========================
import os
load_dotenv()

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")  # <-- your static API key
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ==========================
# 2. API Endpoint
# ==========================
@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def analyze_product_image(request):
    """
    Upload an image → AI returns description + tags
    """
    if "image" not in request.FILES:
        return Response({"error": "No image uploaded"}, status=400)

    image_file = request.FILES["image"]

    try:
        pil_img = Image.open(image_file).convert("RGB")
    except Exception as e:
        return Response({"error": f"Invalid image: {str(e)}"}, status=400)

    # ==========================
    # 3. Prompt for Gemini
    # ==========================
    prompt = """
You are an AI product image analyst. For the given product image, provide:

1. **Description (40–50 words):** Mention colors, materials, design, shape, and unique features.  
2. **Catchy Name:** Short, brandable product name.  
3. **Categories (10):** Relevant, concise categories.  
4. **Tags (12–15):** Mix of @tags and #hashtags, trendy and descriptive.
"""


    response = model.generate_content([prompt, pil_img])

    description = response.text.strip()
    tags = re.findall(r"(?:[#@]\w+)", description)
    clean_tags = [t.strip("#@").lower() for t in tags]

    return Response({
        "description": description,
        "tags": clean_tags
    })
