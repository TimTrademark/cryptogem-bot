

const baseUrl = "http://localhost:5000/api";

async function getExchangesConfigured() {
    const res = await fetch(baseUrl + "/get-exchanges-configured");
    return await res.json();
}

async function getExchangesNotConfigured() {
    const res = await fetch(baseUrl + "/get-exchanges-not-configured");
    return await res.json();
}

async function addExchangeConfig(name, api_key, api_secret) {
    const res = await fetch(baseUrl + "/add-exchange-config", {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({name, api_key, api_secret})
  });
}

async function deleteExchangeConfig(name) {
    const res = await fetch(baseUrl + "/delete-exchange-config", {
    method: 'DELETE',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({name})
  });
}

async function toggleActiveExchangeConfig(name) {
    const res = await fetch(baseUrl + "/toggle-active-exchange-config", {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({name})
  });
}

async function init() {
    const data = await getExchangesConfigured();
    const exchanges_configured = data["exchanges"];
    const area = document.getElementById("active-exchanges");
    area.innerHTML = `
    <div id="add" class="add-exchange-card" data-bs-toggle="modal" data-bs-target="#add-exchange-modal">
    <img src="images/gridicons_add.png" alt="add-icon"></div>
    `;
    for(let i = 0; i < exchanges_configured.length; i++) {
        const exchange = exchanges_configured[i];
        area.innerHTML = getExchangeCardHTML(exchange["title"], exchange["img"], exchange["active"]) + area.innerHTML;
        const delete_icon = document.getElementById(exchange["title"]).querySelector(`#${exchange["title"]}-delete`);
        delete_icon.onclick = async () => {
            await deleteExchangeConfig(exchange["title"]);
            await init();
        }
        const toggle = document.getElementById(exchange["title"]).querySelector(`#${exchange["title"]}-toggle-active`);
        toggle.onclick = async () => {
        toggle.src = toggle.src.endsWith("pause.png") ? "../images/play.png" : "../images/pause.png";
            const altValue = toggle.src.endsWith("pause.png") ? "play icon" : "pause icon";
            toggle.setAttribute("alt", altValue);
            await toggleActiveExchangeConfig(exchange["title"]);
        }
    }
    const add_card = document.getElementById("add");

    add_card.onclick = () => {
        add_card.style.animation = "pop 0.1s linear 1";
        setTimeout(() => {add_card.style.animation = "none";}, 150);
    }

    const data_not_configured = await getExchangesNotConfigured();
    const exchanges_not_configured = data_not_configured["exchanges"];
    const exchanges_select = document.getElementById("exchanges-select");
    for(let i = 0; i < exchanges_not_configured.length; i++) {
        const exchange = exchanges_not_configured[i];
        exchanges_select.innerHTML += `<option value="${exchange['name']}">${exchange["title"]}</option>`;
    }

}

const add_exchange_btn = document.getElementById("add-exchange-btn");
add_exchange_btn.onclick = async () => {
    const name = document.getElementById("exchanges-select").value;
    if(name.toLowerCase() === "exchange") return;
    const api_key = document.getElementById("floatingInputApiKey").value;
    const api_secret = document.getElementById("floatingInputApiSecret").value;
    await addExchangeConfig(name, api_key, api_secret);
    document.getElementsByClassName("modal-backdrop")[0].remove();
    document.getElementById("add-exchange-modal").classList.remove("show");
    await init();
}

init();


function getExchangeCardHTML(title, img, active) {
    return `
    <div id="${title}" class="active-exchange-card">
            <div class="active-exchange-card-logo-area">
                <div class="active-exchange-card-logo"><img src="images/${img}" alt="exchange logo"></div>
            </div>
            <div class="active-exchange-card-content">
                <div class="active-exchange-card-content-header"><h2>${title}</h2><img class="delete-btn" id="${title}-delete" src="images/delete.png"
                                                                                   alt="delete icon"></div>
                <div class="active-exchange-card-content-actions"><img id="${title}-toggle-active" src="${active ? '../images/pause.png' : '../images/play.png'}"
                                                                       alt="${active ? 'pause' : 'play'} icon"></div>
            </div>
     </div>
    `;
}