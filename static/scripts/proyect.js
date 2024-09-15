const contenedor = document.getElementById("proj-container");
const panel1 = document.getElementById("cifrar");
const panel2 = document.getElementById("descifrar");
const boton1 = document.getElementById("boton_panel_cifrar");
const boton2 = document.getElementById("boton_panel_descifrar");

panel1.style.display = "block";
panel2.style.display = "none";

boton1.addEventListener("click", () => {
    panel1.style.display = "block";
    panel2.style.display = "none";
});

boton2.addEventListener("click", () => {
    panel1.style.display = "none";
    panel2.style.display = "block";
});