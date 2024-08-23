# Image Metadata Viewer/Editor

A web application for viewing and removing EXIF metadata from images.

## Features

- View EXIF metadata of uploaded images
- Remove EXIF data from images
- Browser-based interface

## Usage

1. Start the application
2. Upload an image using the "Choose Image" button
3. View the metadata displayed on the page
4. Click "Remove EXIF" to create a copy of the image without metadata

## Setup

1. Ensure Python and Flask are installed
2. Clone the repository
3. Run `python app.py`
4. Access the app at `http://localhost:5000` in your web browser

## Requirements

- Python 3.x
- Flask
- Pillow (PIL)

## Note

The application processes images locally in your browser. No data is stored on external servers.