# ICT305 Assignment 2
## Pink Fluffy Unicorns

<img src="build/icon.png" alt="drawing" width="256"/>

## Setup
Ensure you have **Python** installed and then run the following in a terminal to install any python requirements:
```
cd ICT305-A2
./python/setup_app.bat
```

Once the bat script has installed any requirements, start the application by running in the same terminal:
```
./python/start_app.bat
```

Once the application has started, navigate to **localhost:5006** in a browser to view.

## Electron

The app also has an Electron wrapper to launch and view the application in a native Windows app

In a terminal, run:
```
cd ICT305-A2
./python/setup_app.bat
```

Then launch **ICT305-A2-PinkFluffyUnicorns.exe** from the dist folder

## Build

If you would like to build the Electron app, ensure **NPM** is installed and from a terminal run:

```
cd ICT305-A2
./python/setup_app.bat
npm i
npm run dist
```

The build executable is found in the **/dist** folder