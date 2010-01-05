$(document).ready(intialize);

function intialize() {
    if ( $("#fposttopic").length > 0 ) {
        $('#fposttopic').clearForm();
        $('#fposttopic').ajaxForm( {
            // dataType identifies the expected content type of the server response 
            dataType:  'json',       
            // success identifies the function to invoke when the server response 
            // has been received 
            success: formsubmission }
        );
    }
    
    if ( $("#fpostreply").length > 0 ) {
        $('#fpostreply').clearForm();
        $('#fpostreply').ajaxForm({
            // dataType identifies the expected content type of the server response 
            dataType:  'json',              
            // success identifies the function to invoke when the server response 
            // has been received 
            success: formsubmission }
        );
    } 
}

function check_errors_in_form() {
    farry =  $('#fposttopic *').fieldValue()
  
    if ($.trim(farry[0]).length  <= 0) {
        window.alert("Subject field should not be empty"+farry[0]);
        return false;
    }
     
    if ($.trim(farry[1]).length <= 0) {
        window.alert("Message field should not be empty"+farry[1]);
        return false;
    }
            
    //hide the form
    
    $("#errorbox span").html(" <img src='/site_media/dinette/images/ajaximage.gif' alt='ajax image'/> &nbsp; posting...........  ")
    
     return true;
}


function check_errors_in_Replyform() {
    farry =  $('#fpostreply *').fieldValue();
    if ($.trim(farry[0]).length  <= 0) {
        window.alert("MEssage should not be empty"+farry[0]);
        return false;
    }
   
    $("#errorbox span").html(" <img src='/site_media/dinette/images/images/ajaximage.gif' alt='ajax image'/> &nbsp; posting the reply...........  ");
     
    return true;    
}


function formsubmission(data) {
    if ( $("#fposttopic").length > 0 ) {
        if(data["is_valid"] == "true") {
            $("#topicslist").prepend(data["response_html"]);
            show_hide_error_box();
            $("#errorbox span").html("Sucessfully posted the topic");
            $("#errorbox span").css({ padding : 6 })
            $("#formbox").css("display","none");
        }
        else if(data["is_valid"] == "false") {
            $("tr:lt(3)","#formbox").remove();
            $("#formbox  table tbody").prepend(data["response_html"]);
            show_hide_error_box();
            $("#errorbox span").html("There is an error in the form.Please repost the form");
            $("#errorbox span").css({ padding : 6 })
        }        
        else if(data["is_valid"] == "flood") {
            $("#formbox").css("display","none");
            show_hide_error_box();
            $("#errorbox span").html(data["errormessage"]);
            $("#errorbox span").css({ padding : 6 })
        }
    }
    
    if ( $("#fpostreply").length > 0 ) {
        if(data["is_valid"] == "true") {
            $("#replylist").append(data["response_html"]);
            show_hide_error_box();
            $("#errorbox span").html("Sucessfully Replied to the topic");
            $("#errorbox span").css({ padding : 6 })
            $("#formbox").css("display","none");
        }
        else if(data["is_valid"] == "false") {
            $("tr:lt(2)","#formbox").remove();
            $("#formbox  table tbody").prepend(data["response_html"]);
            show_hide_error_box();
            $("#errorbox span").html("There is an error in the form.Please repost the form");
            $("#errorbox span").css({ padding : 6 })
        }
        else if(data["is_valid"] == "flood") {
            $("#formbox").css("display","none");
            show_hide_error_box();
            $("#errorbox span").html(data["errormessage"]);
            $("#errorbox span").css({ padding : 6 })
        }
   }
}


function isUserAuthenticated( k )
{
    farry =  $('[name=authenticated]').val()     
    
    if(farry == "True") {
        if($("#formbox").css("display") == "block") {
            $("#formbox").css("display","none");
            return false;
        }
         
        if( $("#fposttopic").length > 0 ) {
            $("#errorbox span").html(" ");
            $("#errorbox span").css({ padding : 0 })
            $("#formbox").css("display","block");
         }
         
        if( $("#fpostreply").length > 0 ) {
            if(k == 2) {
                content =   $("#formbox").html();
                $("#formbox").remove();    
                $("#belowpostreplybox").after("<div id='formbox'>"+content+"</div>");
                $("#formbox").css("display","block");
                $("#errorbox span").html(" ");
                $("#errorbox span").css({ padding : 0 });
                $('#fpostreply').ajaxForm({dataType: 'json', success: formsubmission });
            }
            else{
                content =   $("#formbox").html();
                $("#formbox").remove();    
                $("#errorbox").after("<div id='formbox'>"+content+"</div>");
                $("#formbox").css("display","block");
                $("#errorbox span").html(" ");
                $("#errorbox span").css({ padding : 0 });
                $('#fpostreply').ajaxForm({dataType:  'json', success: formsubmission });
            }
         }
         
        if ( $("#fposttopic").length > 0 ){
            $('#fposttopic').clearForm();        
            $(':input:visible:enabled:first','#fposttopic').focus();
            return false;
        }
           
        if( $("#fpostreply").length > 0 )  {
            $('#fpostreply').clearForm();
            $(':input:visible:enabled:first','#fpostreply').focus();
            return false;
        }
    }
    document.location = "/forum/login/?next=/forum/";    
    return false; 
}


function hideForm()
{
    $("#formbox").css("display","none");
   return false;
}

function update_message(data){
   $("#errorbox span").html(data["message"]);
   $("#errorbox span").css({ padding : 6 })
   show_hide_error_box();
   
}

function show_hide_error_box(){
   $("#errorbox span").show();
   setTimeout(function (){$("#errorbox span").hide('normal');}, 3000);
}

$('.moderate-post').click(function(){
   url = $(this).attr('href');
   $.post(url, {}, update_message, 'json');
   return false;
   })

