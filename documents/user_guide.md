# User guide

## Server

There is few ways to lauch a server where the app is then accessible. 

### Panel

Launch a Panel server with

    panel serve app.py

which then launches a local server where the app is hosted.

### PyScript

To make a Panel app suitable for GitHub Pages it has to be converted to WebAssembly. For this we use PyScript.

Convert the  app.py to PyScript based application with

    panel convert app.py --to pyscript --out app --skip-embed

where

    --to pyscript

defines that we use PyScript,

    --out app

the output folder and

    --skip-embed

flag skips embedding contents to app.html.

<strong>Important:</strong> Converting might not work if PyScript does not find all required requirements. The process might be successful but the app.html might have importing issues. This is why it is suggested to use, for example, virtual environment with requirements in requirement.txt.

PyScript based application can also be served (and therefore tested) locally with

    python3 -m http.server

and navigating to app/app.html.

More about [Running Panel in the Browser with WASM](https://panel.holoviz.org/how_to/wasm/index.html).

### GitHub Pages

When the repository is updated, GitHub Actions automatically sets up a server where the PyScript based application app/app.html is hosted.

https://music-recommender.github.io/music-recommender/app/app.html



