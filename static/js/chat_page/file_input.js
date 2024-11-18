const text_input = document.getElementById("text_input");
const file_input = document.getElementById("file_input");

text_input.addEventListener('dragenter', function(){
    text_input.className="hidden";
    file_input.className="";
});

['drop', 'dragleave'].forEach(eventName => file_input.addEventListener(eventName, function(){
    text_input.className="";
    file_input.className="hidden";
}));