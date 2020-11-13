
socket = io();

function send_message(message, e_name = 'newmessage'){
    socket.emit(e_name,message);
};


//event dispatcher
socket.on('newmessage', function(data){
    switch (data['event']){

        //incoming login modal!
        case 101:{
            $('#mainpage').append(data['htm']);
            }
            break;


        //login data are OK, submit the form
        case 121:{
            $('#loginform').submit();
            }
            break;

    }
});


//--------------------- common ops -----------------------

function loginmodal(){
    var data = {event: 201};
    send_message(data);
    return;
};


function closemodal(element){
    $( "#"+element.toString()).remove();
    return;
};


function try_login(){
    var uname = $('#login_username').val();
    var password= $('#login_password').val();
    var message = {event: 221, username: uname, password:password};
    send_message(message);
};


function loginattempt(form){
    $('#'+form.toString()).submit();
};


function opendetail(id){
    if ( !$('#'+id.toString()).data('opened') ){
        $('#details_'+ id.toString()).show();
        $( '#icon_'+ id.toString() ).removeClass('rotate180');
        $( '#icon_'+ id.toString() ).addClass('rotate90');
        $('#'+id.toString()).data('opened', true);
    }else{
        $('#details_'+id.toString()).hide();
        $( '#icon_'+ id.toString() ).removeClass('rotate90');
        $( '#icon_'+ id.toString() ).addClass('rotate180');
        $('#'+id.toString()).data('opened', false);
    }
};


function uc_next(){
    $('#admincarousel').carousel('next');
};


function uc_prev(){
    $('#admincarousel').carousel('prev');
};


// ------------------ admin ops ----------------------

function admin_proba(){
    console.log('HI THERE!');
};