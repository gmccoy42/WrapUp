// <![CDATA[
	
	$('#login').click(function(){ openFunction(); return false; });

	function login(showhide)
	{
	  if(showhide == "show")
	  {
		  document.getElementById('container').style.visibility="visible";
	  }
	  else if(showhide == "hide")
	  {
	      document.getElementById('container').style.visibility="hidden"; 
	      //document.getElementById('regbox').style.visibility="hidden"; 
	  }
	}

	function closeFunction()
	{
		document.getElementById('problem').style.visibility="hidden";
		login("hide");
	}

	function openFunction()
	{
		login("show");
	}

	function logout()
	{
		delete_cookie("login");
		delete_cookie("user");
		delete_cookie("u_id");
		delete_cookie("pass");
		location.reload(); 
	}

	function regShow()
	{
		document.getElementById('regbox').style.visibility="visible";
	}

	function regHide()
	{
		document.getElementById('regbox').style.visibility="hidden";
	}

	function passCheck()
    {
    	var pass1 = document.getElementById('p1').value;
    	var pass2 = document.getElementById('p2').value;
    	if(pass1.localeCompare(pass2) == 0)
    	{
    		document.getElementById('problem').style.visibility="hidden";
    		var form = document.getElementById('reg');
    		form.submit();
    	}
    	else
    	{
    		document.getElementById('problem').style.visibility="visible";
    	}
    }

    function delete_cookie(name) 
    {
    	//Doesn't seem to work
    	document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
	}

	function checkPass() {
		var valid = true;
	    var confirmPassword = $("#confirm-password").val();
	    var password = $("#userpassword").val();
	    var user = $("#username").val();
	    var email = $("#email").val();
	    var msg = ""

	    if (password == confirmPassword)
	    {
	    	
	    }
	    else
	    {
	    	msg += "Passwords do not match<br>";
	    	valid = false;
	    }

	    if(user != "")
	    {

	    }
	    else
	    {
	    	msg += "Must Enter Username<br>";
	    	valid = false;
	    }

	    if(email != "")
	    {

	    }
	    else
	    {
	    	msg += "Must Enter Email<br>";
	    	valid = false;
	    }
	    $("#divCheckPasswordMatch").html(msg);
	    return valid;
	}

	function regSub()
	{
		if(checkPass())
		{
			$( "#register-form" ).submit();
		}
		else
		{

		}
	}


	$(function() {
	    $('#login-form-link').click(function(e) {
			$("#login-form").delay(100).fadeIn(100);
	 		$("#register-form").fadeOut(100);
			$('#register-form-link').removeClass('active');
			$(this).addClass('active');
			e.preventDefault();
		});
		$('#register-form-link').click(function(e) {
			$("#register-form").delay(100).fadeIn(100);
	 		$("#login-form").fadeOut(100);
			$('#login-form-link').removeClass('active');
			$(this).addClass('active');
			e.preventDefault();
		});

	});

	function debug()
	{
		alert($("#confirm-password").val());
		alert($("#userPassword").val());
	}

	function deleteItem(id)
	{
		var form = document.getElementById(id)
	}

	 
	// ]]>