/* guarda o scroll quando é dado refresh */

if ("scrollRestoration" in history) {
    history.scrollRestoration = "auto";
}

/* efeito de scroll */

const fadeElements = document.querySelectorAll(".fade-in");

const observer = new IntersectionObserver((entries) => {

    entries.forEach(entry => {

        if (entry.isIntersecting) {
            entry.target.classList.add("visible");
        } else {
            entry.target.classList.remove("visible");
        }

    });

}, {
    threshold: 0.01
});


/* marcação de pagina */

fadeElements.forEach(el => observer.observe(el));

const links = document.querySelectorAll(".nav-link");

const currentPage = window.location.pathname.split("/").pop();

links.forEach(link => {

    const linkPage = link.getAttribute("href").split("/").pop();

    if (linkPage === currentPage) {
        link.classList.add("active");
    }

});

/* aparecimento/desaparecimento botao flutuante */

document.addEventListener("DOMContentLoaded", () => {

    const floatingBtn = document.getElementById("floatingReserva");
    const triggers = document.querySelectorAll(".reserva-trigger");

    if (!floatingBtn || triggers.length === 0) return;

    const observer = new IntersectionObserver((entries) => {

        let visible = false;

        entries.forEach(entry => {
            if (entry.isIntersecting) {
                visible = true;
            }
        });

        if (visible) {
            floatingBtn.classList.remove("show");
        } else {
            floatingBtn.classList.add("show");
        }

    }, {
        threshold: 0.2
    });

    triggers.forEach(el => observer.observe(el));

});

/* guarda automaticamente o formulário */

const form = document.querySelector(".reserva-form");

if (form) {

    const inputs = form.querySelectorAll("input, textarea, select");

    inputs.forEach(input => {

        const savedValue = localStorage.getItem(input.name);

        if (savedValue) {
            input.value = savedValue;
        }

        input.addEventListener("input", () => {
            localStorage.setItem(input.name, input.value);
        });

    });

}

/* limpar no botão cancelar */

const cancelBtn = document.getElementById("cancelarReserva");

if (cancelBtn) {

    cancelBtn.addEventListener("click", () => {

        localStorage.clear();
        form.reset();

    });

}

/* Limpar ao submeter */

const reservaForm = document.getElementById("reservaForm");

if (reservaForm) {

    reservaForm.addEventListener("submit", () => {
        localStorage.clear();
    });

}


document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("reservaForm");

    /* se não houver formulário, não executa o resto */
    if (!form) return;


    const steps = document.querySelectorAll(".form-step");
    const nextBtns = document.querySelectorAll(".next-step");
    const prevBtns = document.querySelectorAll(".prev-step");
    const indicators = document.querySelectorAll(".reserva-steps .step");

    let currentStep = 0;


    function showStep(index) {

        steps.forEach(step => step.classList.remove("active"));
        steps[index].classList.add("active");


        indicators.forEach((indicator, i) => {

            indicator.classList.remove("active", "done");

            if (i === index) {
                indicator.classList.add("active");
            }

            if (i < index) {
                indicator.classList.add("done");
            }

        });

    }


    nextBtns.forEach(btn => {

        btn.addEventListener("click", function () {

            if (currentStep < steps.length - 1) {
                currentStep++;
                showStep(currentStep);
            }

            if (currentStep === 2) {
                preencherResumo();
            }

        });

    });


    prevBtns.forEach(btn => {

        btn.addEventListener("click", function () {

            if (currentStep > 0) {
                currentStep--;
                showStep(currentStep);
            }

        });

    });


    function preencherResumo() {

        document.getElementById("resumoServico").textContent =
            document.getElementById("servico").value;

        document.getElementById("resumoBike").textContent =
            document.getElementById("modeloBike").value;

        document.getElementById("resumoData").textContent =
            document.getElementById("data").value;

        document.getElementById("resumoMensagem").textContent =
            document.getElementById("mensagem").value;

        document.getElementById("resumoNome").textContent =
            document.getElementById("nome").value;

        document.getElementById("resumoEmail").textContent =
            document.getElementById("email").value;

        document.getElementById("resumoTelefone").textContent =
            document.getElementById("telefone").value;

    }


    /* bloquear datas anteriores */

    const dataInput = document.getElementById("data");

    if (dataInput) {

        const today = new Date().toISOString().split("T")[0];
        dataInput.setAttribute("min", today);

    }


    /* redirecionar para página de confirmação */

    form.addEventListener("submit", async function (e) {

        e.preventDefault();

        const submitBtn = document.getElementById("submitBtn");

        // 🔒 bloquear botão
        submitBtn.disabled = true;
        submitBtn.textContent = "A enviar...";

        const dados = {
            nome: document.getElementById("nome").value,
            email: document.getElementById("email").value,
            telefone: document.getElementById("telefone").value,
            servico: document.getElementById("servico").value,
            modelo_bike: document.getElementById("modeloBike").value,
            mensagem: document.getElementById("mensagem").value,
            data: document.getElementById("data").value
        };

        try {

            const res = await fetch("https://atxcyclingstore.onrender.com/bookings/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(dados)
            });

            const result = await res.json();

            if (result.success) {
                window.location.href = "confirmacao.html";
            } else {
                throw new Error("Erro backend");
            }

        } catch (err) {

            console.error(err);

            alert("Erro ao enviar");

            // 🔓 voltar ao normal se falhar
            submitBtn.disabled = false;
            submitBtn.textContent = "Enviar Pedido";
        }

    });

});


/* menu hamburguer mobile */

document.addEventListener("DOMContentLoaded", function () {

    const hamburger = document.getElementById("hamburger");
    const navLinks = document.querySelector(".nav-links");

    hamburger.addEventListener("click", function () {
        navLinks.classList.toggle("active");
    });

});

document.addEventListener("click", function (e) {

    const navLinks = document.querySelector(".nav-links");
    const hamburger = document.getElementById("hamburger");

    if (!navLinks.classList.contains("active")) return;

    const clicouDentroMenu = navLinks.contains(e.target);
    const clicouHamburger = hamburger.contains(e.target);

    if (!clicouDentroMenu && !clicouHamburger) {
        navLinks.classList.remove("active");
    }

});

/* ================= GALERIA ================= */

const galBikes = document.getElementById("gal-bikes");
const galXTR = document.getElementById("gal-xtr");

/* só executa se estivermos na página da galeria */

if (galBikes && galXTR) {

    /* carregar imagens */

    for (let i = 1; i <= 23; i++) {

        const img = document.createElement("img");
        img.src = "../images/gal/gal" + i + ".png";
        img.loading = "lazy";
        img.classList.add("fade-in");

        galBikes.appendChild(img);

        observer.observe(img); /* usa o observer que já tens */

    }

    for (let i = 1; i <= 13; i++) {

        const img = document.createElement("img");
        img.src = "../images/xtr/xtr" + i + ".png";
        img.loading = "lazy";
        img.classList.add("fade-in");

        galXTR.appendChild(img);

        observer.observe(img);

    }

}

/* ================= LIGHTBOX AVANÇADO ================= */

const lightbox = document.getElementById("lightbox");
const lightboxImg = document.getElementById("lightbox-img");
const closeLightbox = document.getElementById("close-lightbox");
const prevBtn = document.querySelector(".prev");
const nextBtn = document.querySelector(".next");

if (lightbox) {

    let images = [];
    let currentIndex = 0;

    /* atualizar lista de imagens sempre que clicar */

    document.addEventListener("click", function (e) {

        if (e.target.tagName === "IMG" && e.target.closest(".grid-galeria")) {

            images = Array.from(document.querySelectorAll(".grid-galeria img"));
            currentIndex = images.indexOf(e.target);

            showImage();

            lightbox.style.display = "flex";
        }

    });


    function showImage() {
        lightboxImg.src = images[currentIndex].src;
    }


    /* navegar */

    function nextImage() {
        currentIndex = (currentIndex + 1) % images.length;
        showImage();
    }

    function prevImage() {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        showImage();
    }

    nextBtn.addEventListener("click", nextImage);
    prevBtn.addEventListener("click", prevImage);


    /* teclado */

    document.addEventListener("keydown", (e) => {

        if (lightbox.style.display === "flex") {

            if (e.key === "ArrowRight") nextImage();
            if (e.key === "ArrowLeft") prevImage();
            if (e.key === "Escape") lightbox.style.display = "none";

        }

    });


    /* fechar */

    closeLightbox.addEventListener("click", () => {
        lightbox.style.display = "none";
    });

    lightbox.addEventListener("click", (e) => {
        if (e.target === lightbox) {
            lightbox.style.display = "none";
        }
    });

}

/* ================= NAVBAR SCROLL MOBILE ================= */

const navbar = document.querySelector(".navbar");

if (navbar) {

    let lastScroll = 0;

    window.addEventListener("scroll", () => {

        if (window.innerWidth > 768) return;

        const currentScroll = window.scrollY;

        if (currentScroll > lastScroll && currentScroll > 100) {
            // descer
            navbar.classList.add("hide");
        } else {
            // subir
            navbar.classList.remove("hide");
        }

        lastScroll = currentScroll;

    });

}






