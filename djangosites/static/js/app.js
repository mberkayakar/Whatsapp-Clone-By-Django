const roomName = JSON.parse(document.getElementById('room-name').textContent)
const chatSocket = new WebSocket('ws://'+window.location.host+"/ws/chat/"+roomName+"/")
const conversation = document.getElementById('conversation')
const sendbutton = document.getElementById('send')
const inputfield = document.getElementById('ali')

const user = JSON.parse(document.getElementById('user').textContent)
document.getElementById('hiddeninput').addEventListener('change',handleFileSelect)
function handleFileSelect() {
  let file = document.getElementById('hiddeninput').files[0];
  getBase64(file,file.type)
}
function getBase64(file, filetype) {
  let type = filetype.split('/')[0]
  let reader = new FileReader()
  reader.readAsDataURL(file)
  reader.onload=function () {
    chatSocket.send(JSON.stringify({
      'what_is_it':type,
      'message':reader.result,
  }))
  }
  conversation.scrollTop=conversation.scrollHeight
}
conversation.scrollTop=conversation.scrollHeight

chatSocket.onopen = () => chatSocket.send(JSON.stringify({
  'what_is_it':"text",
  'message':"görüldümesajı10203040",
}));

function okundumu(){
  let form = $("#aliform");																
  let form_serialize = form.serialize();
  $.ajax({
    method : "POST",									
    type:'json',										
    url: `/chat/okundu/${roomName}`,
    data: form_serialize,														
    success:function (data) {
      if (data.data=="True")
      document.querySelectorAll('span .messagex').forEach(element => element.innerText = 'okundu');
    }
  })
}
setInterval(okundumu,4000)

chatSocket.onmessage=function (e) {
  const data = JSON.parse(e.data)
  const message_type = data.what_is_it
  if(data.message=="görüldümesajı10203040"){
    console.log("okundurkardeşim")
    if (user!=data.user){
      document.querySelectorAll('span .messagex').forEach(element => element.innerText = 'okundu');
    }}
  else{
    if(message_type==="text")
    {
      let messages = data.message
    }
    else if(message_type==="image")
    {
      let messages=`<img style="width:400px;height=400px;" src="${data.message}"alt="hataaaa">`
    }
    if (user===data.user){
        if(message_type==="image")
        {
          let message = `
    <div class="row message-body">
          <div class="col-sm-12 message-main-sender">
            <div class="sender">
              <div class="message-text">
              <img style="width:400px;height=400px;" src="${data.message}"alt="hataaaa">
              </div>
              <span class="message-time pull-right">
                ${data.created_date} - <span class= "messagex">okunmadı</span> 
              </span>
            </div>
          </div>
        </div>`
        conversation.innerHTML +=message;
        }
        else{
          let message = `
    <div class="row message-body">
          <div class="col-sm-12 message-main-sender">
            <div class="sender">
              <div class="message-text">
                x
              </div>
              <span class="message-time pull-right">
                x - <span class= "messagex">okunmadı</span> 
              </span>
            </div>
          </div>
        </div>`
        conversation.innerHTML +=message;
        let allSelects = document.getElementsByClassName("message-text");
        let lastSelect = allSelects[allSelects.length-1];
        lastSelect.innerText= data.message;
        let allSelectss = document.getElementsByClassName("message-time pull-right");
        let lastSelects = allSelectss[allSelectss.length-1];
        lastSelects.innerText= data.created_date+" - ";
        lastSelects.innerHTML +="<span class= 'messagex'>okunmadı</span> ";
        conversation.scrollTop=conversation.scrollHeight
        }
        let form = $("#aliform");																
        let form_serialize = form.serialize();
        $.ajax({
          method : "POST",									
          type:'json',										
          url: `/chat/goruldu/${roomName}`,
          data: form_serialize,														
          success:function (data) {
            document.getElementById("removefield").remove();
            document.getElementById("addfield").innerHTML= data["data"];
          }
        })

    }
    else{if(message_type==="image")
    {
      let message = `
<div class="row message-body">
      <div class="col-sm-12 message-main-receiver">
        <div class="receiver">
          <div class="message-text">
          <img style="width:400px;height=400px;" src="${data.message}"alt="hataaaa">
          </div>
          <span class="message-time pull-right">
            ${data.created_date}
          </span>
        </div>
      </div>
    </div>`
    conversation.innerHTML +=message;
    }
    else{
      let message = `
<div class="row message-body">
      <div class="col-sm-12 message-main-receiver">
        <div class="receiver">
          <div class="message-text">
            x
          </div>
          <span class="message-time pull-right">
            x  
          </span>
        </div>
      </div>
    </div>`
    conversation.innerHTML +=message;
    let allSelects = document.getElementsByClassName("message-text");
    let lastSelect = allSelects[allSelects.length-1];
    lastSelect.innerText= data.message;
    let allSelectss = document.getElementsByClassName("message-time pull-right");
    let lastSelects = allSelectss[allSelectss.length-1];
    lastSelects.innerText= data.created_date+" - ";
    conversation.scrollTop=conversation.scrollHeight
    }

        let form = $("#aliform");																
        let form_serialize = form.serialize();
        $.ajax({
          method : "POST",									
          type:'json',										
          url: "/chat/roomcontrol",
          data: form_serialize,														
          success:function (data) {
            document.getElementById("removefield").remove();
            document.getElementById("addfield").innerHTML= data["data"];
            document.querySelectorAll('span .messagex').forEach(element => element.innerText = 'okundu')
          }
        }
      )
    }
  }
}
chatSocket.onclose=function(e){
    console.error("kapatttınknk")
}
inputfield.focus();
inputfield.onkeyup=function (e) {
  if(e.keycode===13){
      sendbutton.click()
  }
}
sendbutton.onclick=function (e) {
  const message = inputfield.value
  ///chat/goruldu/roomName
  
  if (message==="")
  {
  inputfield.value= ""
  inputfield.focus()
  }
  else{
  chatSocket.send(JSON.stringify({
    'message':message,
    'what_is_it':'text'
  }))
  inputfield.focus()
  inputfield.value= ""}
  conversation.scrollTop=conversation.scrollHeight
}