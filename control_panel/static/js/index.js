

const baseUrl = "http://localhost:5000/api";

async function getExchangesConfigured() {
    const res = await fetch(baseUrl + "/get-exchanges-configured");
    return await res.json();
}

async function getExchangesNotConfigured() {
    const res = await fetch(baseUrl + "/get-exchanges-not-configured");
    return await res.json();
}

async function addExchangeConfig(name, api_key, api_secret, funds, extra_args) {
    const res = await fetch(baseUrl + "/add-exchange-config", {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({name, api_key, api_secret, funds, extra_args})
  });
  return await res.json();
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
    }
    for(let i = 0; i < exchanges_configured.length; i++) {
    const exchange = exchanges_configured[i];
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
    let exchanges_select = document.getElementById("exchanges-select");
    exchanges_select.innerHTML = "<option disabled selected>Exchange</option>";
    for(let i = 0; i < exchanges_not_configured.length; i++) {
        const exchange = exchanges_not_configured[i];
        exchanges_select.innerHTML += `<option id="option-${exchange['name']}" data-min-funds="${exchange['min_funds']}" value="${exchange['name']}">${exchange["title"]}</option>`;
        exchanges_select = document.getElementById("exchanges-select");
    }
    exchanges_select.onchange = (e) => {
        const picked = e.target.value;
        document.getElementById('min-funds-hint').innerText = `Minimum trade funds for ${e.target.value} is ${e.target.options[e.target.selectedIndex].dataset.minFunds} USDT`;
        for(let i = 0; i < exchanges_not_configured.length; i++) {
        const exchange = exchanges_not_configured[i];
        if(exchange["name"].toLowerCase() !== picked.toLowerCase()) continue;
        const extra_args_keys = exchange["extra_args"];
         const modal_extra_args = document.getElementById("form-extra-args");
        if(extra_args_keys === null) {
            modal_extra_args.style = "display: none;";
        } else if(extra_args_keys.length > 0) {
            modal_extra_args.style = "display: block;";
            modal_extra_args.innerHTML = "";
            for(let j = 0; j < extra_args_keys.length; j++) {
                const extra_arg = extra_args_keys[j]
                modal_extra_args.innerHTML += `
                <div class="form-floating mb-3">
                    <input type="text" class="form-control floatingInputExtraArgs" id="floatingInputExtraArgs" data-arg="${extra_arg}" placeholder="${extra_arg.charAt(0).toUpperCase() + extra_arg.slice(1)}">
                    <label for="floatingInputExtraArgs">${extra_arg.charAt(0).toUpperCase() + extra_arg.slice(1)}</label>
                    </div>
                </div>
            `;
            }

        }
    }
    }
}

const add_exchange_btn = document.getElementById("add-exchange-btn");
add_exchange_btn.onclick = async () => {
    const name = document.getElementById("exchanges-select").value;
    if(name.toLowerCase() === "exchange") return;
    const api_key = document.getElementById("floatingInputApiKey").value;
    const api_secret = document.getElementById("floatingInputApiSecret").value;
    const funds = document.getElementById("floatingInputFunds").value;
    const extra_args_dict = {};
    if(document.getElementById("form-extra-args").style.display != "none") {
        const extra_args = document.getElementsByClassName("floatingInputExtraArgs");
        for(let i = 0; i < extra_args.length;i++) {
            extra_args_dict[extra_args[i].dataset.arg] = extra_args[i].value;
        }
    }
    const res = await addExchangeConfig(name, api_key, api_secret, funds, extra_args_dict);
    if(res.success == 'false') {
        const mainElement = document.getElementById('main');
        mainElement.innerHTML = `<div class="alert alert-warning alert-dismissible fade show" role="alert">
          ${res.message}
          <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>${mainElement.innerHTML}`;
    } else {
        await init();
    }
    document.getElementById("dismiss-modal").click();

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