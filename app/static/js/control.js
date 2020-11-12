
socket = io();

function send_message(e_name,message){
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

    }
});

function loginmodal(){
    var data = {event: 201};
    send_message('newmessage', data);
    return;
};


function closemodal(element){
    $( "#"+element.toString()).remove();
    return;
};


function loginattempt(form){
    console.log(form);
    $('#'+form.toString()).submit();
}