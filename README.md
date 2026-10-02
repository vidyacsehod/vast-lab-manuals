# VAST CSE – Lab Manual Download Portal

Streamlit app for downloading the Department of CSE lab manuals (KTU 2019 & 2024 schemes).

## Run locally
    pip install -r requirements.txt
    streamlit run app.py

## Folder layout
    app.py                 main app
    assets/logo.png        college logo (transparent)
    assets/thumbs/*.png    cover-page thumbnails
    manuals/*.pdf          the lab manuals
    .streamlit/config.toml brown theme matching the logo

## Add a new manual
1. Copy the PDF into `manuals/`.
2. Add one entry to the `MANUALS` list in `app.py`.
3. (Optional) cover thumbnail: `pdftoppm -f 1 -l 1 -png -r 40 manuals/X.pdf assets/thumbs/X`
   and rename the output to `X.png`.

## Deploy free
Push this folder to GitHub, then deploy on https://share.streamlit.io (main file: app.py).
