
socket = io();

function send_message(message, e_name = 'newmessage'){
    socket.emit(e_name,message);
};


//------------------- event dispatcher ------------------

socket.on('newmessage', function(data){
    switch (data['event']){

        //--------------------- dev ops ---------------------------

        case 301:{
            $('#mainpage').append(data['htm']);
            }
            break;

        //---------------------------------------------------------

        //incoming login modal!
        case 101:{
            $('#mainpage').append(data['htm']);
            }
            break;


        //error message!
        case 109:{
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


function register(){
    var message = {event: 209, message: 'Ez a funkció nem elérhető!'};
    send_message(message);
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

        if (edit_user != 0){
            $('#details_'+edit_user.toString()).hide();
            $( '#icon_'+ edit_user.toString() ).removeClass('rotate90');
            $( '#icon_'+ edit_user.toString() ).addClass('rotate180');
        };

        $('#details_'+ id.toString()).show();
        $( '#icon_'+ id.toString() ).removeClass('rotate180');
        $( '#icon_'+ id.toString() ).addClass('rotate90');
        $('#'+id.toString()).data('opened', true);
        edit_user = id;
    }else{
        edit_user = 0;
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


function req_for_addumodal(){
};


//------------------- dev ops ------------------------
var edit_user = 0

function req_for_aselector(){
    var data = {event: 401};
    send_message(data);
    return;
};


function showuri(img){
    var newsrc = $(img).attr('src').toString();
    $('#useravatar_'+edit_user.toString()).attr( 'src', newsrc );
    closemodal('avatarmodal');
};