String.prototype.hashCode = function() {
	  var hash = 0, i, chr;
	  if (this.length === 0) return hash;
	  for (i = 0; i < this.length; i++) {
		      chr   = this.charCodeAt(i);
		      hash  = ((hash << 5) - hash) + chr;
		      hash |= 0; // Convert to 32bit integer
		    }
	  return hash;
	};
function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
				}
			}
		}
	return cookieValue;
	}
function csrfSafeMethod(method) {
	//these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
			}
		}
	});
$(document).ready(function(){
	$("#registration").submit(function(){ //This function controls registration form
		let email = $("[name='email']").val();
		let nickname = $("[name='nickname']").val();
		let password = $("[name='password']").val().hashCode(); //Get password and hash it
		let password2 = $("[name='passwordT']").val().hashCode();
		$.ajaxSetup({                  
			beforeSend: function(xhr, settings) {//Setup crossdomain methods to ajax   
				if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));                                                                  
					}      
				}              
			});
		if(password === password2){
			$.ajax({//Send the response to the server
				type:"POST",
				url:"/registration/",
				data:{"email":email, "nickname":nickname, "password":password},
				success:function(){location.href="/"},
				statusCode:{
					500:function(){alert("Such user is already exists");}
					}
				});
			}else{alert("Passwords are not the same");}		
		return false;
		});
	$("#signin").submit(function(){
		let nickname = $("[name='username']").val();
		let password = $("[name='pass']").val().hashCode();//Make hash of password
		$.ajaxSetup({//The same setup                  
			beforeSend: function(xhr, settings) {   
				if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));                                                                  
					}      
				}              
			});  
		$.ajax({
			type:"POST",
			url:"/signin/",
			data:{"nickname":nickname, "password":password},//Send data to the server
			success:function(){location.href="/"}//If successful login redirect to main page
			});
		return false;
		});
});
