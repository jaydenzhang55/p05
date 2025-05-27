document.addEventListener('DOMContentLoaded', function(){
    if (loggedIn){
        const login = document.getElementById('loginButton');
        const logout = document.createElement('a');
        logout.href = '/logout';
        logout.id='logout_button';
        logout.setAttribute('class', 'px-4 py-2 rounded-3xl transition bg-blue-600 text-white hover:bg-blue-500 hover:scale-105" id="login_button');
        logout.textContent = "Log Out";

        login.replaceWith(logout);
       
        const lmessage = document.getElementById('lmessage');
        const welcome =  "Welcome " + user + "!";
        lmessage.textContent = welcome;
    }
    else{
        const profile = document.getElementById('sbutton');
        const login = document.createElement('a');
        login.href = '/login';
        login.textContent = "Saved";  

        profile.replaceWith(login)  

        console.log('wwww')
    }

     

    page = document.title;

});
