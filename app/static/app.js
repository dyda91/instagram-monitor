// app/static/app.js

console.log("Instagram Monitor iniciado");

// =========================================================
// AUTO REFRESH DASHBOARD
// =========================================================
setInterval(() => {

    const currentPath = window.location.pathname;

    // Atualiza apenas dashboard
    if (currentPath === "/") {

        window.location.reload();

    }

}, 60000);

// =========================================================
// ANIMAÇÃO SIMPLES CARDS
// =========================================================
window.addEventListener("DOMContentLoaded", () => {

    const cards = document.querySelectorAll(".card");

    cards.forEach((card, index) => {

        card.style.opacity = "0";
        card.style.transform = "translateY(15px)";

        setTimeout(() => {

            card.style.transition = "0.3s";

            card.style.opacity = "1";
            card.style.transform = "translateY(0px)";

        }, index * 80);

    });

});