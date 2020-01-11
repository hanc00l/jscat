fso1 = new ActiveXObject("Scripting.FileSystemObject");
if (fso1.FileExists("~REMOTE_PATHNAME~")) {
    f = fso1.OpenTextFile("~REMOTE_PATHNAME~", 1);
    d = f.ReadAll();
    f.Close();
    c = "~JOB_ID~" + "|" + d;
}
else{
    c = "~JOB_ID~" + "|" + "[File not exists]";
}
