document.addEventListener('DOMContentLoaded', function(){
    if (loggedIn){
        // const login = document.getElementById('loginButton');
        // const logout = document.createElement('a');
        // logout.href = '/logout';
        // logout.id='logoutButton';
        // logout.setAttribute('class', 'px-4 py-2 rounded-3xl transition bg-blue-600 text-white hover:bg-blue-500 hover:scale-105" id="login_button');
        // logout.textContent = "Log Out";

        // login.replaceWith(logout);
       
        // const lmessage = document.getElementById('lmessage');
        // const welcome =  "Welcome " + user + "!";
        // lmessage.textContent = welcome;
    }

    page = document.title;

    searchBar = document.getElementById('searchBar');
    searchBar.addEventListener('submit', function(event){
        if(document.getElementById('search').value.trim()===''){
            event.preventDefault();
        }
    });
    
    const searchOptions = document.getElementById('searchOptions')
    const options = searchOptions.getElementsByTagName('li');
    const searchInput = document.getElementById('search')

    searchOptions.style.width = "${searchInput.offsetWidth}px";

    Array.from(options).forEach(option => {
        option.addEventListener('click', function(){
            searchInput.value = option.textContent.trim();
        })
    });

    let filterSearch = function(){
        const searchTerm = searchInput.value.toLowerCase();
        let found = false;

        if (searchTerm.trim() === "") {
        searchOptions.style.display = "none";
        return;
    }
        Array.from(options).forEach(option => {
            const optionName = option.textContent.toLowerCase();
            option.style.width = "${searchInput.offsetWidth}px";

            if (optionName.includes(searchTerm)) {
                option.style.display = '';
                found = true;
            } else {
                option.style.display = 'none';
            }
         });

         if(found){
            searchOptions.style.display='';
         }
         else{
            searchOptions.style.display='none';
         }
    }

    searchInput.addEventListener('input', filterSearch);

    if (page == "Search"){
        if(!searchFound && !showAll){
            const result = document.getElementById('searchResult');
            const message = document.createElement('div');
            message.setAttribute('class', 'flex flex-col text-blue-700 w-full h-full gap-y-10 px-10 py-10 text-center items-center')
            const error = document.createElement('p');
            error.textContent = "Uh Oh, it seems that you have reached a "
            const name = document.createElement('p');
            name.setAttribute('class', 'text-5xl border border-x-transparent border-y-blue-700 border-y-4 p-10 font-bold font-stretch-expanded')
            name.textContent = '404NotFound'
            const solution = document.createElement('p');
            solution.textContent = "Please try a different search, view all current pdfs, or upload your own to add to the archive."
            const request = document.createElement('form');

            const hiddenInput = document.createElement('input');
            hiddenInput.setAttribute('type', 'hidden');
            hiddenInput.setAttribute('name', 'request'); 
            hiddenInput.setAttribute('value', search);
            request.appendChild(hiddenInput);


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
