
const myButton = document.getElementById("reply_btn");


myButton.addEventListener("click", function(){

    const replies = document.getElementById("all_replies");

    if (replies.classList.contains('d-none')){
        replies.classList.remove('d-none');
        myButton.textContent = "Comment";

    }
    else{
        replies.classList.add('d-none');
        myButton.textContent = "Reply";
        

 
    }


})




