# Server instructions

There are few ways to lauch a server where the app is then accessible. 

## Panel

Launch a Panel server with

    panel serve app.ipynb

which then launches a local server where the app is hosted.
Additionally, you can add

    --autoreload

flag which automatically reloads the server if there are changes.

## PyScript

Convert the <em>app.ipynb</em> to PyScript based application with

    panel convert app.ipynb --to pyscript --out app --skip-embed

where

    --to pyscript

defines that we use PyScript,

    --out app

the output folder and

    --skip-embed

flag skips embedding contents to <em>app.html</em>.

<strong>Important:</strong>

1. Converting might not work if PyScript does not find all required requirements. The process might be successful but the <em>app.html</em> might have importing issues. This is why it is suggested to use, for example, virtual environment with requirements defined in <em>requirement.txt</em>.
2. Also, if <em>json</em>-package is imported and included in requirements, it needs to be removed from packages inside <em>py-config</em>-tags in <em>app.html</em>

PyScript based application can also be served (and therefore tested) locally with

    python3 -m http.server

and navigating to <em>app/app.html</em>.

More about [Running Panel in the Browser with WASM](https://panel.holoviz.org/how_to/wasm/index.html).

## GitHub Pages

When the repository is updated, GitHub Actions automatically sets up a server where the PyScript based application <em>app/app.html</em> is hosted.

https://music-recommender.github.io/music-recommender/app/app.html

