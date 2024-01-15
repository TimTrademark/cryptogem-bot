const add_card = document.getElementById("add");

add_card.onclick = () => {
    add_card.style.animation = "pop 0.15s linear 1";
    setTimeout(() => {add_card.style.animation = "none";}, 150);
}