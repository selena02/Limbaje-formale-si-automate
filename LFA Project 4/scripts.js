
var filters;
function init() {
    button.addEventListener("click", show);
    fetch("result.json")
    .then(response => response.json())
    .then(data =>{
        let list = document.getElementById("list");
        filters = Object.values(data);
        console.log(data);
    })
}
function show(){
    let filtersArray = Array(9);
    for(let i = 0; i < 9; i++){
        filtersArray[i] = document.getElementById("cb"+i).checked;
    }
        let list = document.getElementById("list");
        let count = 0;
        let i = 0;
        list.innerHTML = '';
        filters.forEach(element => {
            if(filtersArray[i]){
                count += Object.values(element).length;
                element.forEach(details => {
                    list.innerHTML += `
                    <li>
                        <a href=${details.link}>
                            <h3>${details.title.slice(0, 45)}</h3>
                            <img src=${details.image}>
                            <h2>${details.price}</h2>
                        </a>
                    </li>
                    `
                })
            }
            i++;
        })
            document.getElementById("count").textContent = `Am găsit ${count} rezultate pentru tine`;
        }
    const button = document.getElementById("btn");
    window.onload = init;