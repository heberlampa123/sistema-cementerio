// Paginacion de tabla
document.addEventListener("DOMContentLoaded", function () {
    const table = document.getElementById("AllTable");
    const rows = table.querySelectorAll("tbody tr");
    const rowsPerPage = 8; // Número de filas por página
    const pagination = document.getElementById("pagination");
    const pageCount = Math.ceil(rows.length / rowsPerPage);
    let currentPage = 1;

    function showPage(page) {
        rows.forEach((row, index) => {
            row.style.display = (index >= (page - 1) * rowsPerPage && index < page * rowsPerPage)
                ? ""
                : "none";
        });
    }

    function createPagination() {
        pagination.innerHTML = "";

        // Botón "Anterior"
        const prevLi = document.createElement("li");
        prevLi.classList.add("page-item");
        if (currentPage === 1) prevLi.classList.add("disabled");

        const prevLink = document.createElement("a");
        prevLink.classList.add("page-link");
        prevLink.href = "#";
        prevLink.textContent = "« Anterior";
        prevLink.addEventListener("click", function (e) {
            e.preventDefault();
            if (currentPage > 1) {
                currentPage--;
                showPage(currentPage);
                createPagination();
            }
        });

        prevLi.appendChild(prevLink);
        pagination.appendChild(prevLi);

        // Números de página
        for (let i = 1; i <= pageCount; i++) {
            const li = document.createElement("li");
            li.classList.add("page-item");
            if (i === currentPage) li.classList.add("active");

            const a = document.createElement("a");
            a.classList.add("page-link");
            a.href = "#";
            a.textContent = i;
            a.addEventListener("click", function (e) {
                e.preventDefault();
                currentPage = i;
                showPage(currentPage);
                createPagination();
            });

            li.appendChild(a);
            pagination.appendChild(li);
        }

        // Botón "Siguiente"
        const nextLi = document.createElement("li");
        nextLi.classList.add("page-item");
        if (currentPage === pageCount) nextLi.classList.add("disabled");

        const nextLink = document.createElement("a");
        nextLink.classList.add("page-link");
        nextLink.href = "#";
        nextLink.textContent = "Siguiente »";
        nextLink.addEventListener("click", function (e) {
            e.preventDefault();
            if (currentPage < pageCount) {
                currentPage++;
                showPage(currentPage);
                createPagination();
            }
        });

        nextLi.appendChild(nextLink);
        pagination.appendChild(nextLi);
    }

    showPage(currentPage);
    createPagination();
});

document.addEventListener("DOMContentLoaded", function () {
    const table = document.getElementById("DefTable");
    const rows = table.querySelectorAll("tbody tr");
    const rowsPerPage = 5; // Número de filas por página
    const pagination = document.getElementById("pagination");
    const pageCount = Math.ceil(rows.length / rowsPerPage);
    let currentPage = 1;

    function showPage(page) {
        rows.forEach((row, index) => {
            row.style.display = (index >= (page - 1) * rowsPerPage && index < page * rowsPerPage)
                ? ""
                : "none";
        });
    }

    function createPagination() {
        pagination.innerHTML = "";

        // Botón "Anterior"
        const prevLi = document.createElement("li");
        prevLi.classList.add("page-item");
        if (currentPage === 1) prevLi.classList.add("disabled");

        const prevLink = document.createElement("a");
        prevLink.classList.add("page-link");
        prevLink.href = "#";
        prevLink.textContent = "« Anterior";
        prevLink.addEventListener("click", function (e) {
            e.preventDefault();
            if (currentPage > 1) {
                currentPage--;
                showPage(currentPage);
                createPagination();
            }
        });

        prevLi.appendChild(prevLink);
        pagination.appendChild(prevLi);

        // Números de página
        for (let i = 1; i <= pageCount; i++) {
            const li = document.createElement("li");
            li.classList.add("page-item");
            if (i === currentPage) li.classList.add("active");

            const a = document.createElement("a");
            a.classList.add("page-link");
            a.href = "#";
            a.textContent = i;
            a.addEventListener("click", function (e) {
                e.preventDefault();
                currentPage = i;
                showPage(currentPage);
                createPagination();
            });

            li.appendChild(a);
            pagination.appendChild(li);
        }

        // Botón "Siguiente"
        const nextLi = document.createElement("li");
        nextLi.classList.add("page-item");
        if (currentPage === pageCount) nextLi.classList.add("disabled");

        const nextLink = document.createElement("a");
        nextLink.classList.add("page-link");
        nextLink.href = "#";
        nextLink.textContent = "Siguiente »";
        nextLink.addEventListener("click", function (e) {
            e.preventDefault();
            if (currentPage < pageCount) {
                currentPage++;
                showPage(currentPage);
                createPagination();
            }
        });

        nextLi.appendChild(nextLink);
        pagination.appendChild(nextLi);
    }

    showPage(currentPage);
    createPagination();
});

// Mostrar / Ocultar contraseña
const togglePassword = document.getElementById('togglePassword');
const passwordInput = document.getElementById('exampleInputPassword1');
const iconoPassword = document.getElementById('iconoPassword');

togglePassword.addEventListener('click', () => {
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);
    iconoPassword.classList.toggle('bi-eye');
    iconoPassword.classList.toggle('bi-eye-slash');
});



document.addEventListener("DOMContentLoaded", () => {
    // Buscar elementos; si alguno no existe, salimos silenciosamente.
    const tipoServicioSelect = document.getElementById("tipo_servicio");
    const asignacionSelect = document.getElementById("asignacion");
    const totalInput = document.getElementById("total");

    // Si la página no tiene estos elementos, no hacemos nada.
    if (!tipoServicioSelect && !asignacionSelect && !totalInput) return;

    function getOptionData(option, key) {
        if (!option) return 0;
        const v = option.dataset ? option.dataset[key] : undefined;
        return v !== undefined ? parseFloat(v) || 0 : 0;
    }

    function calcularTotal() {
        try {
            let total = 0;

            // Precio del tipo de servicio
            const tsOption = tipoServicioSelect ? tipoServicioSelect.options[tipoServicioSelect.selectedIndex] : null;
            const precioTS = getOptionData(tsOption, "precio");

            // Precio de la asignación
            const asigOption = asignacionSelect ? asignacionSelect.options[asignacionSelect.selectedIndex] : null;
            const precioAsig = getOptionData(asigOption, "precio");

            // Verificar si la asignación ya está usada (dataset.usado === "1")
            const asignacionUsada = asigOption ? (asigOption.dataset && asigOption.dataset.usado === "1") : false;

            total = precioTS + (asignacionUsada ? 0 : precioAsig);

            if (totalInput) totalInput.value = total.toFixed(2);
        } catch (err) {
            console.error("Error al calcular total:", err);
        }
    }

    // Conectar eventos si existen los selects
    if (tipoServicioSelect) tipoServicioSelect.addEventListener("change", calcularTotal);
    if (asignacionSelect) asignacionSelect.addEventListener("change", calcularTotal);

    // Calculo inicial (útil en la página de edit para mostrar el total existente)
    calcularTotal();
});


setTimeout(() => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        alert.classList.remove('show');
        alert.classList.add('fade');
    });
}, 3500);