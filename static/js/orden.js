function convertirMayusculas(element) {
    $element = element
    $element.value = $element.value.toUpperCase()
  }


async function buscarProducto(element) {
  $element = element
  console.log($element); 
  let dataList = $element.parentElement.children[1].id
  let $dataListProduct = document.getElementById(dataList)

  const urlObject = new URL(url)
  // TIPOS...
  // 1: cedula
  // 2: names
  parametro = $element.value
  const urlBuscar = `${urlObject}/productos/buscar_producto/${parametro}`
  async function productoData(urlBuscar) {
      
      let response = await fetch(urlBuscar)
      let productoList = await response.json()
      return productoList
  }
  data_product = await productoData(urlBuscar)
  console.log(data_product);
  $dataListProduct.innerHTML = ''
  console.log($dataListProduct);
  let $dataListAll = $element.parentElement.querySelectorAll('datalist[id*="producto"]')
  data_product.forEach(function(item) {
  let opcion = document.createElement('option')
  opcion.value = `${item['pk']} - ${item['nombre']}`
  $dataListProduct.appendChild(opcion)
  let options = $element.parentElement.querySelectorAll(`input[list="${dataList}"]`)
  options.forEach(element => element.addEventListener(
      'input', function(element) {
      element.preventDefault()
      LlenarDataProduct(element, $dataListAll, $element)
      }
  ));

  })
  
}

// / Llenado de campos del formulario al hacer click en un cliente encontrado
function LlenarDataProduct(element, dataList, field) {
  console.log(field);
  let input = element.target
  let val = input.value
  let list = input.getAttribute('list')
  let options = document.getElementById(list).childNodes
  console.log(options.length);

  for (let i = 0; i < options.length; i++) {
    if (options[i].value === val) {
      // An item was selected from the list!
      // yourCallbackHere()
      let product = getProductPk(val)[0]
      console.log(product);
      console.log(field.parentElement.parentElement.querySelector(`input[id="${id_producto}"]`));
      //send data to inputs
      field.parentElement.parentElement.querySelector(`input[id="id_producto_pk"]`).value = product.pk
      field.parentElement.parentElement.querySelector(`input[id="id_producto"]`).value = product.nombre
      field.parentElement.parentElement.querySelector(`input[id="id_cantidad"]`).value = product.cantidad
      field.parentElement.parentElement.querySelector(`input[id="id_precio"]`).value = product.precio
      dataList.forEach(function(item) {
        item.innerHTML = ''
      })
      field.blur()
      document.getElementById('id_producto').onkeyup = null
      break;
    }
  }

  calcularCosto()
}

function getProductPk(pk_producto) {
  espacioCodigo = pk_producto.search(' ')
  return data_product.filter(
      function(data_product) {
      return data_product.pk == pk_producto.slice(0, espacioCodigo)
      }
  );
  }

function agregarDetalle() {
  var div = document.getElementById("id_productos");
  if (!div) return;
  var row = document.createElement('div');
  row.className = "row g-2 align-items-center mb-2 fila-detalle";
  row.innerHTML =
    '<div class="col-md-2 col-4"><button type="button" class="btn btn-sm btn-outline-danger" onclick="eliminarProducto(this)" title="Eliminar"><i class="fas fa-trash-alt me-1"></i> Quitar</button></div>' +
    '<div class="col-md-2 d-none"><input class="form-control form-control-sm" name="pk_detalle" type="text" value=""></div>' +
    '<div class="col-md-3 col-8"><input class="form-control form-control-sm" type="text" name="detalle_producto" placeholder="Descripción"></div>' +
    '<div class="col-md-2 col-6"><select class="form-select form-select-sm" name="tipo_producto"><option value="externo">Externo</option><option value="inventario">Inventario</option></select></div>' +
    '<div class="col-md-2 col-6"><input class="form-control form-control-sm input-cantidad" type="number" step="0.01" min="0" name="cantidad_producto" value="1" placeholder="Cantidad" oninput="calcularCosto()"></div>' +
    '<div class="col-md-2 col-6"><input class="form-control form-control-sm input-precio" type="number" step="0.01" min="0" name="precio_producto" value="0.00" placeholder="0.00" oninput="calcularCosto()"></div>';
  var totalRow = div.querySelector('.fila-total-detalles');
  if (totalRow) div.insertBefore(row, totalRow);
  else div.appendChild(row);
  if (typeof calcularCosto === 'function') calcularCosto();
}

function agregarProducto() {
  agregarDetalle();
}

function eliminarProducto(element) {
  var fila = element.closest && element.closest('.fila-detalle');
  if (fila) fila.remove();
  else if (element.parentElement && element.parentElement.parentElement) element.parentElement.parentElement.remove();
  if (typeof calcularCosto === 'function') calcularCosto();
}

function calcularCosto() {
  var montoCobrar = document.getElementById('id_monto_cobrar');
  var totalDetallesEl = document.getElementById('valor-total-detalles');
  var filas = document.querySelectorAll('.fila-detalle:not(.fila-total-detalles)');
  var total = 0;

  filas.forEach(function(fila) {
    var cantInput = fila.querySelector('input[name="cantidad_producto"]');
    var precInput = fila.querySelector('input[name="precio_producto"]');
    if (!cantInput || !precInput) return;
    var cant = parseFloat(cantInput.value) || 0;
    var prec = parseFloat(precInput.value) || 0;
    total += cant * prec;
  });

  total = Math.round(total * 100) / 100;
  if (montoCobrar) montoCobrar.value = total.toFixed(2);
  if (totalDetallesEl) totalDetallesEl.textContent = total.toLocaleString('es-EC', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}