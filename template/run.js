job = function () {
    r = new ActiveXObject("WScript.Shell").Run("~CMD~", 0, false);
    return "[run success]";
}
c = "~JOB_ID~" + "|" + job();
