import requests
import os
from urllib.parse import urlparse
import hashlib


def generate_filename(url):
    """Extracts filename from URL or generates a hash-based filename."""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    if not filename:
        # Generate a unique filename using URL hash
        hash_object = hashlib.md5(url.encode())
        filename = f"image_{hash_object.hexdigest()}.jpg"
    return filename


def download_image(url, directory="Fetched_Images"):
    """Downloads a single image from a URL into the specified directory."""
    try:
        # Ensure the directory exists
        os.makedirs(directory, exist_ok=True)

        # Fetch the image with a timeout
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error for bad HTTP status

        # Optional: check HTTP headers for content type
        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith('image'):
            print(f"✗ URL does not point to an image: {url}")
            return

        # Generate filename and filepath
        filename = generate_filename(url)
        filepath = os.path.join(directory, filename)

        # Prevent duplicate downloads by checking if file exists
        if os.path.exists(filepath):
            print(f"⚠ Image already exists: {filename}")
            return

        # Save image in binary mode
        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}\n")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error for URL {url}: {e}")
    except Exception as e:
        print(f"✗ An error occurred for URL {url}: {e}")


def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Ask user for multiple URLs (comma-separated)
    urls_input = input(
        "Please enter image URL(s), separated by commas if multiple: ")
    urls = [url.strip() for url in urls_input.split(',') if url.strip()]

    for url in urls:
        download_image(url)

    print("Connection strengthened. Community enriched.")


if __name__ == "__main__":
    main()
