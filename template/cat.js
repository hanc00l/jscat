job = function () {
    fso1 = new ActiveXObject("Scripting.FileSystemObject");
    if (fso1.FileExists("~REMOTE_PATHNAME~")) {
        f = fso1.OpenTextFile("~REMOTE_PATHNAME~", 1);
        d = f.ReadAll();
        f.Close();
        return d;
    }
    else {
        return "[File not exists]";
    }
}
c = "~JOB_ID~" + "|" + job();
