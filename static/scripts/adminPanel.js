window.addEventListener('DOMContentLoaded',()=>{
    const focusDynamicLinks =()=>{
        const linkFocus = localStorage.getItem('linkFocus');
        const links = document.querySelectorAll('a.menu__link');

        if (linkFocus) {
            const link = document.querySelector(`a.menu__link[href="${linkFocus}"]`);
            if (link) {
                links.forEach(link=>link.classList.remove('menu__link--active'))
                link.classList.add('menu__link--active');
            }
        }

        links.forEach(a=>{
            a.addEventListener('click',()=>{
                localStorage.setItem('linkFocus', new URL(a.href).pathname);
            })
        })
    }

    const actionLogout = () => {
        const logout = document.querySelector('#logout');
        logout?.addEventListener('click',()=>{
            const url = logout.getAttribute('data-url');
            if(!url) return;
            Swal.fire({
                title: "¿Está seguro que desea cerrar sesión?",
                icon: "info",
                confirmButtonText: "Si, estoy seguro",
                denyButtonText: "No",
                showDenyButton:true
            })
            .then(result=>{
                if(result.isConfirmed){
                    localStorage.clear();
                    window.location.href = url;
                }
            })
        })
    }

    const toggleProfileOptions =()=>{
        const profileName = document.querySelector('.profile__name');
        const profileOptions = document.querySelector('.profile__options');
        profileName?.addEventListener('click',()=>profileOptions.classList.toggle('toggle'))
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.profile')) profileOptions?.classList.remove('toggle');
        });
    }


    const deleteMember =()=>{
        const buttons =  document.querySelectorAll('.button--delete');
        buttons.forEach(button=>{
            button.addEventListener('click',()=>{
                const dataUrl = button.getAttribute('data-url');
                const title = button.title?button.title:'Eliminar este elemento';
                const csrfToken = document
                    .querySelector('meta[name="csrf-token"]')
                    .getAttribute('content');


                if(!dataUrl || !csrfToken)return;
                Swal.fire({
                    title: `¿${title}?`,
                    icon: "info",
                    confirmButtonText: "Si, estoy seguro",
                    denyButtonText: "No",
                    showDenyButton:true
                })
                .then(result=>{
                    if(result.isConfirmed) {
                        const form = document.createElement("form");
                        const csrf = document.createElement("input");
                        form.method = "POST";
                        form.action = dataUrl;
                        csrf.type = "hidden";
                        csrf.name = "csrfmiddlewaretoken";
                        csrf.value = csrfToken;
                        form.appendChild(csrf);
                        document.body.appendChild(form);
                        form.submit();
                    }
                })
            })
        })
    }

    const toggleDropdown =()=>{
        const openActiveDropdown =()=>{
            const currentPath = window.location.pathname;
            document.querySelectorAll('.menu__link').forEach(link=>{
                const href = link.getAttribute('href');
                if (!href || href === '#') return;
                const linkPath = new URL(link.href).pathname;
                if(currentPath === linkPath){
                    link.classList.add('menu__link--active');
                    const dropdown = link.closest('.menu__dropdown');
                    const menu = dropdown?.querySelector('.menu');
                    if(menu){
                        menu.classList.add('menu--visible');
                        menu.style.height = menu.scrollHeight + 'px';
                    }
                }
            })
        }
        document.querySelectorAll('.menu__dropdown__header').forEach(button=>{
            button.addEventListener('click',()=>{
                const dropdown = button.closest('.menu__dropdown');
                const menu = dropdown.querySelector('.menu');
                const isOpen = menu.classList.contains('menu--visible');
                 document.querySelectorAll('.menu__dropdown .menu').forEach(m => {
                    m.style.height = "0px";
                    m.classList.remove('menu--visible');
                 });
                 if(!isOpen) {
                     menu.classList.add('menu--visible');
                     menu.style.height = menu.scrollHeight + "px";
                 }
            })
        })

        openActiveDropdown();
    }

    const datalistSelect =()=>{
        document.addEventListener('input',(e)=>{
            if(!e.target.matches('input[list]'))return;
            const input = e.target;
            const list = document.getElementById(input.getAttribute('list'));
            const hidden = input.parentElement.querySelector('input[type=hidden]');
            hidden.value = '';

            list.querySelectorAll('option').forEach(option=>{
                if(option.value === input.value){
                    hidden.value = option.dataset.id;
                }
            })


        })
    }

    datalistSelect();
    toggleProfileOptions();
    actionLogout();
    focusDynamicLinks();
    deleteMember();
    toggleDropdown();


})