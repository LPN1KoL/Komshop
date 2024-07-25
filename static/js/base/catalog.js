function sendData(){

    const XHR = new XMLHttpRequest();
    const form1 = document.getElementById("Form1");
    const form2 = document.getElementById("Form2");
    const FD1 = new FormData(form1);
    const FD2 = new FormData(form2);
    XHR.open("POST", "/catalog");
    XHR.setRequestHeader('Content-type', 'application/json');
    XHR.send({'FD1': FD1, 'FD2': FD2});
    form.addEventListener("submit", function (event) {
    event.preventDefault();
}
