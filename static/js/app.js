
let cent = document.getElementById('Cent');
function showCon(){
    console.log("clicked add")
    let C = document.getElementById('cont');
    
    if (C.style.scale == 0){
        C.classList.toggle('show');
        C.style.position = "";
        cent.style.display = "none";
    }
}
function hideCon(){
    console.log("clicked del")
    let C = document.getElementById('cont');
    
    if (C.style.scale == 0){
        //C.style.display = 'none'
        C.classList.toggle('show');
        C.style.position = "";
        cent.style.display = "block";
    }
}
function more(){
    console.log('M pressed')
    let moreL = document.getElementById('moreL');
    if (moreL.style.display == 'none'){
        moreL.style.display = 'block';
    }else{
        moreL.style.display = 'none';
    }
}
function logout(){
    window.location.assign("/logout");
}

function goto(site){
    window.location.assign(site);
}

function addZero(i) {
    if (i < 10) {
      i = "0" + i;
    }
    return i;
  }
function currentTime() {
  var d = new Date();
  var h = addZero(d.getHours());
  var m = addZero(d.getMinutes());
  var s = addZero(d.getSeconds());
   return `${h} : ${m}`;
}


document.getElementById('message-form').addEventListener('submit', (event) => {
event.preventDefault();
let message = document.getElementById('userInput').value;
console.log(message);

//Add the users message to the screen....
var chatwin = document.getElementById('chatWindow');
var userQ = document.createElement('li');
var mbox = document.createElement('div');
mbox.textContent = message;
var img1 = document.createElement('img');
var nTime = document.createElement('div');
nTime.innerText = currentTime();
nTime.classList.add('sT');
mbox.appendChild(nTime); 
img1.classList.add('im1');
img1.src = "../static/img/profile.png";
mbox.appendChild(img1);
mbox.classList.add('umess');
userQ.appendChild(mbox);
chatwin.appendChild(userQ);

//clear form input to show that message has been sent.....
document.getElementById('userInput').value = '';

//asynchronus request sent to backend...
fetch('/send_message', {method: 'POST', 
headers:{'Content-Type':'application/x-www-form-urlencoded'}, 

body: 'message=' + encodeURIComponent(message)
}).then(response => response.json()).then(data =>{

    var chatwin = document.getElementById('chatWindow');
    var userQ = document.createElement('li');
    var mbox = document.createElement('div');
    // mbox.textContent = message;
    // var img1 = document.createElement('img');
    // var nTime = document.createElement('div');
    // nTime.innerText = currentTime();
    // nTime.classList.add('sT');
    // mbox.appendChild(nTime); 
    // img1.classList.add('im1');
    // img1.src = "../static/img/profile.png";
    // mbox.appendChild(img1);
    // mbox.classList.add('umess');
    // userQ.appendChild(mbox);
    // chatwin.appendChild(userQ);

    var resposeM = document.createElement('li');
    var bBox = document.createElement('div');
    var img = document.createElement('img');
    img.classList.add('im');
    
    img.src = "../static/img/prop.png";
    bBox.classList.add('bmess')
    bBox.innerHTML = data.answer;
    var Time = document.createElement('div');
    Time.innerText = currentTime();
    Time.classList.add('mT');
    bBox.appendChild(Time);
    bBox.appendChild(img);
    resposeM.appendChild(bBox);
    //<!-- console.log(data.response) -->
    chatwin.appendChild(resposeM);
    chatwin.scrollTop = chatwin.scrollHeight;
    console.log(chatwin.scrollTop)
    console.log(data, 12344);
    

});

});
