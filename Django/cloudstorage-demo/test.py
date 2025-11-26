from urllib.parse import urljoin

out = urljoin(
    "https://localhost:8000/media/gradpro/logo.webp",
    "https://localhost:8000/media/gradpro/logo.webp1",
)


print(out)
