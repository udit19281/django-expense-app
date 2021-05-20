window.onload=function() {
    const emailfield=document.getElementById("emailf");
    const emailfeed=document.getElementById("emailfeedbackarea");
    const showps=document.getElementById("show");
    const ps=document.getElementById("passwordf");
    show.addEventListener("click",()=>{
        if(showps.textContent==="Show"){
            showps.textContent="Hide";
            ps.setAttribute("type","text");
        }
        else{
            showps.textContent="Show";
            ps.setAttribute("type","password");
        }
    });
    emailfield.addEventListener("keyup",(e)=>{
        const val=e.target.value;
        emailfeed.classList.remove("is-valid");
        emailfeed.style.display="none";
        if(val.length>0){
            fetch('/auth/valid-email/',{
            method: 'POST',
            body:JSON.stringify({email:val}),})
            .then((res)=>res.json()).then((data)=>{
                console.log(data);
                if(data.email_error){
                    emailfeed.classList.add("is-valid");
                    emailfeed.style.display="block";
                    emailfeed.innerHTML=`<p>${data.email_error}</p>`;
                }
            })
    }
        })
}
