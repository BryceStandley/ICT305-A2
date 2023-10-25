// Modules to control application life and create native browser window
const { app, BrowserWindow, ipcMain, Notification } = require("electron");
const { spawn, exec } = require("child_process");
psTree = require('ps-tree');
const path = require("path");

const nodeConsole = require("console");
const myConsole = new nodeConsole.Console(process.stdout, process.stderr);
let child;

function printBoth(str) {
  console.log("main.js:    " + str);
  myConsole.log("main.js:    " + str);
}

function startCodeFunction() {
  printBoth("Initiating python");
  child = exec('cmd.exe /c .\\python\\start_app.bat"', (error, stdout, stderr) => {
    printBoth(stdout)
  });

  child.stdout.on("data", (data) => {
    printBoth(
      `Following data has been piped from python program: ${data.toString(
        "utf8"
      )}`
    );
  });
};
startCodeFunction();

// Create the browser window.
function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 1000,
    height: 1000,
    resizable: true,
    webPreferences: {
      nodeIntegration: true,
    },
  });

  // Load the index.html of the app.
  mainWindow.loadURL("http://localhost:5006");
  // Open the DevTools.
  ///mainWindow.webContents.openDevTools();
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  createWindow();
  app.on("activate", function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
    
  });
});



// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on("window-all-closed", function () {
  if (process.platform !== "darwin")
  {
    //process.kill(-child.pid);
    psTree(child.pid, function (err, children) {
    spawn('taskkill', ['/f /pid'].concat(children.map(function (p) { return p.PID })));
    });


    app.quit();
  }
});
