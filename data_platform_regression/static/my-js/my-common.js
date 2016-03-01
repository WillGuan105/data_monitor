// <script type="text/javascript">

// function formSubmit()
// {
// 	var ckIds= new Array();
// 	ckIds=getAllChecked();
// 	var ckIdsString = ckIds.join(",");
// 	document.getElementById("returnckIds").value=ckIdsString;
// 	document.getElementById("runjob").submit();
// }


function selectAll()
{

    var allCheckBoxs = document.getElementsByName("box");
    var desc = document.getElementById("selectall");
    if(desc.value == "全选")
    {
        desc.value = "清除";
        for(var i = 0; i < allCheckBoxs.length; i ++ )
        {
            allCheckBoxs[i].checked = true;
        }
    }
    else
    {
        desc.value = "全选";
        for(var i = 0; i < allCheckBoxs.length; i ++ )
        {
        allCheckBoxs[i].checked = false;
        }
    }
}


function getAllChecked()
{
	var ckBox = new Array();
	var allCheckBoxs = document.getElementsByName("box");
	for(var i=0; i < allCheckBoxs.length; i++)
	{
		if(allCheckBoxs[i].checked==true)
		{
			ckBox.push(allCheckBoxs[i].id);
		}
	}
	// {% for m in data %}
	// 	if(document.getElementById('{{m.g_id}}').checked==true)
	// 	{
	// 		ckBox.push({{m.g_id}})
	// 	}
   
	// {% endfor %}
	return ckBox;
}

function getAllDataId()
{
	var dataIds = new Array();
	var allCheckBoxs = document.getElementsByName("box");
	for(var i=0; i < allCheckBoxs.length; i++)
	{
		dataIds.push(allCheckBoxs[i].id);
	}
	// {% for m in data %}
	// 	dataIds.push({{m.g_id}})
	// {% endfor %}
	return dataIds;
}

// function getRunHistory()
// {
// 	var his_arr = new Array()
// 	{% for r in run_history %}
// 		his_arr.push({{r.result_id}})
// 	{% endfor %}
// 	return his_arr[0]
// }

function statistics(){
    document.getElementById('suc-count').innerHTML = 0;
    document.getElementById('fail-count').innerHTML = 0;

	var Status= document.getElementsByName("m.status");
	for(var k = 0; k < Status.length; k ++ )
        {
		if(Status[k].innerText == "success")
		{
			document.getElementById('suc-count').innerHTML ++;
		}
		else if (Status[k].innerText == "error")
			{document.getElementById('fail-count').innerHTML ++;}
	}

}

function setCookie(key,value,expiredays)
{
	var exdate = new Date();
	exdate.setDate(exdate.getDate()+expiredays);
	document.cookie=key+"="+escape(value)+((expiredays==null)?"":";expires="+exdate.toUTCString());
}

function getCookie(key)
{
	if(document.cookie.length>0)
	{
		c_start=document.cookie.indexOf(key + "=")
		if(c_start!=-1)
		{
			c_start=c_start + key.length + 1;
			c_end=document.cookie.indexOf(";",c_start);
			if(c_end == -1)
				c_end=document.cookie.length;
			return unescape(document.cookie.substring(c_start,c_end))
		}
	}
	return ""
}

// </script>