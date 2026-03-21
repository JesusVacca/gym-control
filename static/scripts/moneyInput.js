window.addEventListener('DOMContentLoaded',()=>{
    const form = document.querySelector('.form');

    form?.addEventListener('submit',()=>{
        const moneyInputs = document.querySelectorAll('.money-input');
        moneyInputs.forEach(input=>{
            let value = input.value;
            if(!value) return;
            value = value.replace(/\./g, "").replace(/,/g, "");
            input.value = value;
        })
    })

})