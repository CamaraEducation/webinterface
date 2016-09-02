# Welcome to the Camara Resource Compendium Development Repository.

The two main parts to concern yourself with are the webapp - basically everything in app, and the updater, which can be found in app/resources.

In terms of what needs to be put on an end-user's computer, just /dist will do. It contains the compiled and minimized version of the web app, with the updater gui living in the resource folder. Launchers for the web app and updater gui will need to be created to be user friendly.

The web app can be served simply by running "python -m SimpleHTTPServer" in /dist and going to http://127.0.0.1:8000/ in firefox/the browser of your choice.

The updater gui is run simply as a python script - run "python ./updater.py" in /dist/resources.

The web app was developed using Yeoman, so if you're working on it, you'll want to install that.

I've ensured that all libraries/packages imported for the updater gui come pre-installed. For the purpose of portability I strongly recommend anyone in the future who works on it keeps it that way.

I am not a designer. I did my best to make things looks decent in the web app and usable in the updater, but someone with more UI/UX experience could make things a lot nicer.

[From here on is the default README that yeoman generates. I've left it in becuase it's useful enough info]
# interface

This project is generated with [yo angular generator](https://github.com/yeoman/generator-angular)
version 0.15.1.

## Build & development

Run `grunt` for building and `grunt serve` for preview.

## Testing

Running `grunt test` will run the unit tests with karma.
