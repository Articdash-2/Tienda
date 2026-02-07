let productos = []; // Ahora empieza vacío
let carrito = [];

window.onload = async () => {
  // 1. CARGAR DATOS DESDE EL JSON
  try {
    const respuesta = await fetch("productos.json");
    productos = await respuesta.json();
  } catch (error) {
    console.error("Error cargando productos:", error);
  }

  // 2. MANEJO DEL PRELOADER (código original)
  setTimeout(() => {
    const preloader = document.getElementById("preloader");
    if (preloader) {
      preloader.style.opacity = "0";
      setTimeout(() => (preloader.style.display = "none"), 600);
    }
  }, 1500);

  // 3. MODO VENDEDOR O USUARIO
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get("p")) {
    try {
      mostrarModoVendedor(atob(urlParams.get("p")));
    } catch (e) {
      render(productos);
    }
  } else {
    iniciarEfectoEscritura();
    render(productos);
  }
};
// --- EFECTO DE ESCRITURA PROFESIONAL ---
function iniciarEfectoEscritura() {
  const frases = [
    { texto: "TODO EL TIEMPO FIEL ES DIOS", emoji: " 💖" },
    { texto: "POR SIEMPRE AMEN", emoji: " 🙏" },
  ];

  let index = 0;
  let charIndex = 0;
  let esBorrando = false;
  const cont = document.getElementById("titulo-escrito");

  function type() {
    const current = frases[index];
    const fullArray = Array.from(current.texto + current.emoji);
    const visible = fullArray.slice(0, charIndex).join("");

    // Aplicacion clases dinámicas
    let html = `<span class="shine-text">${visible.replace(current.emoji, "")}</span>`;
    if (visible.includes(current.emoji.trim())) {
      html += `<span class="emoji-fix">${current.emoji}</span>`;
    }

    cont.innerHTML = html + `<span class="cursor">|</span>`;

    if (!esBorrando && charIndex < fullArray.length) {
      charIndex++;
      setTimeout(type, 100);
    } else if (esBorrando && charIndex > 0) {
      charIndex--;
      setTimeout(type, 50);
    } else {
      esBorrando = !esBorrando;
      if (!esBorrando) index = (index + 1) % frases.length;
      setTimeout(type, esBorrando ? 2500 : 500);
    }
  }
  type();
}

// --- FUNCIONES DE TIENDA (RENDER, FILTRAR, CARRITO) ---
function render(lista) {
  const cat = document.getElementById("catalogo");
  if (!cat) return;
  cat.innerHTML = lista
    .map(
      (p) => `
        <div class="producto">
            <img src="${p.img}" 
                 onerror="this.src='./assets/logo.jpeg'" 
                 onclick='abrirDetalle(${JSON.stringify(p)})' 
                 style="cursor: zoom-in;">
            
            <div class="tag-cat">✨ ${p.categoria}</div>
            <div style="font-weight:bold; color:var(--blue);">
                ${p.nombre.replace(/\.[^/.]+$/, "").toUpperCase()}
            </div>            
            ${p.description ? `<p class="prod-desc shine-text">${p.description}</p>` : ""}
            
            <div style="color:var(--accent); font-size:1.3rem; margin:5px 0;">L. ${p.precio}</div>
            <button onclick="agregar('${p.id}')" class="btn-add">AÑADIR 🛒</button>
        </div>
    `,
    )
    .join("");
}

function filtrar() {
  const txt = document.getElementById("buscador").value.toLowerCase();
  render(productos.filter((p) => p.nombre.toLowerCase().includes(txt)));
}

function filtrarCategoria(cat) {
  // Convertimos a minúsculas lo que viene del botón para comparar fácil
  const categoriaBoton = cat.toLowerCase();

  if (categoriaBoton === "todo" || categoriaBoton === "todos") {
    // Si es "todo", mostramos la lista completa original
    render(productos);
  } else {
    // Filtramos ignorando si en el JSON está en mayúsculas o minúsculas
    const resultado = productos.filter((p) => {
      return p.categoria.toLowerCase() === categoriaBoton;
    });
    render(resultado);
  }
}

function agregar(id) {
  const item = carrito.find((p) => p.id === id);
  item
    ? item.cantidad++
    : carrito.push({ ...productos.find((p) => p.id === id), cantidad: 1 });
  actualizarInterfaz();
}

function actualizarInterfaz() {
  const badge = document.getElementById("badge-count");
  const resumen = document.getElementById("lista-resumen");
  badge.innerText = carrito.reduce((sum, p) => sum + p.cantidad, 0);

  resumen.innerHTML = carrito
    .map(
      (p) => `
        <div style="display:flex; justify-content:space-between; align-items:center; padding:10px; border-bottom:1px solid #333;">
            <div style="font-size:0.8rem;">
                <b>${p.nombre.toUpperCase()}</b><br>
                L. ${p.precio} x ${p.cantidad}
            </div>
            <div class="controles-carrito">
                <button onclick="cambiarCantidad('${p.id}', -1)" class="btn-qty">-</button>
                <span style="min-width: 15px; text-align: center;">${p.cantidad}</span>
                <button onclick="cambiarCantidad('${p.id}', 1)" class="btn-qty">+</button>
            </div>
        </div>
    `,
    )
    .join("");
}

function cambiarCantidad(id, delta) {
  const item = carrito.find((p) => p.id === id);
  if (item) {
    item.cantidad += delta;
    if (item.cantidad <= 0) carrito = carrito.filter((p) => p.id !== id);
  }
  actualizarInterfaz();
}

function toggleSidebar() {
  document.getElementById("sidebar").classList.toggle("open");
}

function enviarPedido() {
  const nombre = document.getElementById("cliente-nombre").value.trim();
  const direccion = document.getElementById("cliente-direccion").value.trim();
  if (!carrito.length || !nombre || !direccion)
    return alert("Completa los datos");

  const token = btoa(carrito.map((p) => `${p.id}-${p.cantidad}`).join(","));
  const link = `${window.location.href.split("?")[0]}?p=${token}`;
  let total = carrito.reduce((sum, p) => sum + p.precio * p.cantidad, 0);

  let m = `*PEDIDO - FIEL ES DIOS*\n\nCliente: ${nombre}\nTotal: L. ${total}\n\nVer detalle:\n${link}`;
  window.open(
    `https://wa.me/50499674298?text=${encodeURIComponent(m)}`,
    "_blank",
  );
}

function mostrarModoVendedor(datos) {
  document.getElementById("titulo-escrito").innerHTML =
    `<span class="shine-text">ORDEN RECIBIDA</span> ✅`;
  document.getElementById("categorias-nav").style.display = "none";
  document.getElementById("buscador").style.display = "none";

  const seleccionados = datos
    .split(",")
    .map((par) => {
      const [id, qty] = par.split("-");
      const prod = productos.find((p) => p.id === id);
      return prod ? { ...prod, cantidad: parseInt(qty) } : null;
    })
    .filter((p) => p);

  document.getElementById("catalogo").innerHTML = seleccionados
    .map(
      (p) => `
        <div class="producto">
            <img src="${p.img}">
            <div style="font-weight:bold; color:var(--blue);">${p.nombre.toUpperCase()}</div>
            <div style="color:var(--accent)">Cantidad: ${p.cantidad}</div>
            <div style="font-weight:bold">Subtotal: L. ${p.precio * p.cantidad}</div>
        </div>
    `,
    )
    .join("");
}

function abrirDetalle(p) {
  const modal = document.getElementById("product-modal");

  // Llenar datos en el modal
  document.getElementById("modal-img").src = p.img;
  document.getElementById("modal-titulo").innerText = p.nombre
    .replace(/\.[^/.]+$/, "")
    .toUpperCase();
  document.getElementById("modal-precio").innerText = `L. ${p.precio}`;
  document.getElementById("modal-desc").innerHTML = p.description
    ? `<span class="shine-text">${p.description}</span>`
    : "Calidad y bendición para tu hogar.";
  // Configurar el botón de añadir dentro del modal
  const btnModal = document.getElementById("modal-add-btn");
  btnModal.onclick = () => {
    agregar(p.id); // Llama a tu función original de agregar
    modal.style.display = "none";
  };

  modal.style.display = "block";

  // Cerrar al dar clic en la X
  document.querySelector(".close-modal").onclick = () =>
    (modal.style.display = "none");

  // Cerrar al dar clic fuera del cuadro
  window.onclick = (event) => {
    if (event.target == modal) modal.style.display = "none";
  };
}
