
const showPasswordToggle = document.querySelector('.showPasswordToggle');
const password = document.querySelector('#password');


const handleToggleInput =(e)=>{

    if(showPasswordToggle.className==='fa fa-eye-slash'){
        showPasswordToggle.className = 'fa fa-eye';
        password.setAttribute('type','text');
    } else {
        showPasswordToggle.className = 'fa fa-eye-slash';
        password.setAttribute('type','password');
    }
}

showPasswordToggle.addEventListener('click',handleToggleInput);
