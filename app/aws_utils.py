import os
from uuid import uuid4

MEDIA_DIR = "./media"
os.makedirs(MEDIA_DIR, exist_ok=True)


def save_file(file) -> str:
    # Зберігає файл локально та повертає URL для доступу через FastAPI static
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid4()}{ext}"
    file_path = os.path.join(MEDIA_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return f"/media/{filename}"
