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

function agregarProducto() {
  $div = document.getElementById("id_productos")
  $row = document.createElement('div')
  $row.className="row"
  $row.style="padding: 5px;"
  $row.innerHTML = `<div class="row"">
  <div class="col-md-2">
    <a class="btn btn-danger" onclick="eliminarProducto(this)">Eliminar</a>
  </div>
  <div class="col-md-2" style="display: none;">
    <input id="id_producto_pk" class="form-control" name="pk_producto"  type="text" placeholder="pk_producto">
  </div>
  <div class="col-md-4">
    <input id="id_producto" class="form-control"  type="text" name="detalle_producto"  list="producto_by_nombre" placeholder="Producto" onkeyup="buscarProducto(this)">
    <datalist id="producto_by_nombre"></datalist>
  </div>
  <div class="col-md-3">
    <input id="id_cantidad" class="form-control" type="number" name="cantidad_producto" placeholder="Cantidad">
  </div>
  <div class="col-md-3">
    <input id="id_precio" class="form-control" type="number" name="precio_producto"  placeholder="Precio" onKeyUp=calcularCosto()>
  </div>
</div>`
$div.appendChild($row)

}

function eliminarProducto(element) {
  $element = element
  console.log($element);
  $element.parentElement.parentElement.remove()
  calcularCosto()
}

function calcularCosto() {
 $monto_cobrar = document.getElementById('id_monto_cobrar') 
 $precios_productos = document.getElementsByName('precio_producto')
 total = 0
 for (let i = 0; i < $precios_productos.length; i++) {
  total = parseFloat($precios_productos[i].value) + total
 }
  $monto_cobrar.value = total
}