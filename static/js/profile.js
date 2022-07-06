var profilepic = document.getElementById('profilepic')
var form = document.getElementById('profilepicform')
console.log(form)
form.style.display='none'
console.log('hello')

function openfile(){
    profilepic.click()
}

profilepic.onchange = function(){
    document.getElementById('profilepicform').submit()
}
