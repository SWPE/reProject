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
	$("#registration").submit(function(){
		let email = $("[name='email']").val();
		let nickname = $("[name='nickname']").val();
		let password = $("[name='password']").val().hashCode();
		$.ajaxSetup({                  
			beforeSend: function(xhr, settings) {   
				if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));                                                                  
					}      
				}              
			});  
		$.ajax({
			type:"POST",
			url:"/registration/",
			data:{"email":email, "nickname":nickname, "password":password},
			success:function(){location.href="/registration/"}
			});		
		return false;
		});
	$("#signin").submit(function(){
		let nickname = $("[name='username']").val();
		let password = $("[name='pass']").val().hashCode();
		$.ajaxSetup({                  
			beforeSend: function(xhr, settings) {   
				if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));                                                                  
					}      
				}              
			});  
		$.ajax({
			type:"POST",
			url:"/signin/",
			data:{"nickname":nickname, "password":password},
			succes:function(){location.href=""}
			});
		return false;
		});
});
