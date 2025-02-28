function hideShowPassword(elem){
    let input = elem.querySelector('input');
    let img = elem.querySelector('.toggle');
    if (input.type == "password"){
        input.type = "text"
        img.src = "/static/images/afficher.png"
    }
    else{
        input.type = "password"
        img.src = "/static/images/cacher.png"
    }
}

let password = document.getElementById('pwd')
if (password){
    password.querySelector('.toggle').onclick = () => hideShowPassword(password);
}

let passwordConf = document.getElementById('pwdConf')
if (passwordConf){
    passwordConf.querySelector('.toggle').onclick = () => hideShowPassword(passwordConf);
}

let passwordNew = document.getElementById('pwdNew')
if (passwordNew){
    passwordNew.querySelector('.toggle').onclick = () => hideShowPassword(passwordNew);
}
