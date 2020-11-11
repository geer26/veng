
socket = io();

function send_message(e_name,message){
    socket.emit(e_name,message);
};



//event dispatcher
socket.on('newmessage', function(data){
    switch (data['event']){

        //incoming login modal!
        case 101:{
            $('#pagecontent').append(data['htm']);
            }
            break;

    }
});

function loginmodal(){
    var data = {event: 201};
    send_message('newmessage', data);
};
