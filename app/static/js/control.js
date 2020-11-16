
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
            };
            break;


        //adduser modal!
        case 302:{
            $('#mainpage').append(data['htm']);
            };

            break;


        //---------------------------------------------------------

        //incoming login modal!
        case 101:{
            $('#mainpage').append(data['htm']);
            };
            break;


        //error message!
        case 109:{
            $('#mainpage').append(data['htm']);
            };
            break;


        //login data are OK, submit the form
        case 121:{
            $('#loginform').submit();
            };
            break;

        //user deleted, remove from list
        case 122:{
            $('#'+data['id'].toString()).remove();
            };
            break;


        //Registration OK, close the modal
        case 131:{
            $('#adduser_modal').remove();
            var message = {event: 251};
            send_message(message);
            };
            break;


        //incoming usertable refreshment
        case 151:{
            $('#utable').remove();
            $('#table_users').append(data['htm']);
            };
            break;


        //incoming QR table
        case 161:{
            $('#mainpage').append(data['htm']);
            };
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
    var message = {event: 402};
    send_message(message);
};


function deluser(id){
    var message = {event: 222, id: id};
    send_message(message);
};


function register_u(){
    var fullname = $('#fullname').val();
    var mmn = $('#mmn').val();
    var pob = $('#pob').val();
    var email = $('#email').val();
    var phone = $('#phone').val();
    var address = $('#address').val();
    var associaton = $('#associaton').val();
    var lic_no = $('#lic_no').val();
    var ph_pa = $('#adduser_img').attr('src');
    var gender = $('#u_gender').is(':checked')
    if (!fullname || !mmn || !email || !phone || !address || !associaton || !lic_no || !ph_pa || !pob){
        var message = {event: 209, message: 'Minden mező kitöltése kötelező!'};
        send_message(message);
        return;
        }
    var message = {
        event: 231,
        fullname: fullname,
        mmn: mmn,
        pob: pob,
        email: email,
        phone: phone,
        address: address,
        associaton: associaton,
        lic_no: lic_no,
        photo_path: ph_pa,
        gender: gender
        };
    send_message(message);
    return;
};


function req_qr(uuid){
    var domain = location.hostname;
    var message = {event: 261, uuid: uuid, domain: domain};
    send_message(message);
    return
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

    if( $('#adduser_modal').length ){
        $('#adduser_img').attr( 'src', newsrc );
    }
    else{
        $('#useravatar_'+edit_user.toString()).attr( 'src', newsrc );
    }

    closemodal('avatarmodal');
};

function showdatasheet(uuid){
    console.log(uuid);
};