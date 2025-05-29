document.addEventListener('DOMContentLoaded', function(){
    if (loggedIn){
        const login = document.getElementById('loginButton');
        const logout = document.createElement('a');
        logout.href = '/logout';
        logout.id='logoutButton';
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

    }

    page = document.title;

    searchBar = document.getElementById('searchBar');
    searchBar.addEventListener('submit', function(event){
        if(document.getElementById('search').value.trim()===''){
            event.preventDefault();
        }
    });

    if (page == "Search"){
        if(!searchFound){
            const result = document.getElementById('searchResult');
            const message = document.createElement('div');
            message.setAttribute('class', 'flex flex-col text-blue-700 w-full h-full gap-y-10 px-10 py-10 text-center items-center')
            const error = document.createElement('p');
            error.textContent = "Uh Oh, it seems that you have reached a "
            const name = document.createElement('p');
            name.setAttribute('class', 'text-5xl border border-x-transparent border-y-blue-700 border-y-4 p-10 font-bold font-stretch-expanded')
            name.textContent = '404NotFound'
            const solution = document.createElement('p');
            solution.textContent = "Please try again with another name or request to add to our archive."
            const request = document.createElement('form');
            const rbutton = document.createElement('button');
            rbutton.setAttribute('class', 'px-4 py-2 rounded-3xl transition bg-blue-600 text-white hover:bg-blue-500 hover:scale-105');
            rbutton.setAttribute('type', 'submit');
            rbutton.textContent = "Request";
            rbutton.setAttribute('id', 'request');
            rbutton.setAttribute('value', search);
            request.appendChild(rbutton);
            request.setAttribute('action', '/');
            request.setAttribute('method', 'POST');
            message.appendChild(error);
            message.appendChild(name);
            message.appendChild(solution);
            message.appendChild(request);
            message.setAttribute('id', 'searchResult');
            result.replaceWith(message);
        }
    }

});
