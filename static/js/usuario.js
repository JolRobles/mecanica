async function buscarCliente(element, tipo) {
    $element = element
    let dataList = $element.parentElement.parentElement.children[1].id 
    let $dataListUser = document.getElementById(dataList)

    const urlObject = new URL(url)
    // TIPOS...
    // 1: cedula
    // 2: names
    parametro = $element.value
    const urlBuscar = `${urlObject}/usuarios/buscar_cliente/${tipo}/${parametro}`
    async function clientData(urlBuscar) {
        
        let response = await fetch(urlBuscar)
        let clientList = await response.json()
        return clientList
    }
    data_client = await clientData(urlBuscar)
    console.log(data_client);
    $dataListUser.innerHTML = ''
    console.log($dataListUser);
    let $dataListAll = document.querySelectorAll('datalist[id*="usuario"]')
    data_client.forEach(function(item) {
    let opcion = document.createElement('option')
    opcion.value = `${item['cedula']} - ${item['nombre_apellido']}`
    $dataListUser.appendChild(opcion)
    let options = document.querySelectorAll(`input[list="${dataList}"]`)
    options.forEach(element => element.addEventListener(
        'input', function(element) {
        element.preventDefault()
        fillFields(element, $dataListAll, $element)
        }
    ));

    })
    
  }


  
// / Llenado de campos del formulario al hacer click en un cliente encontrado
function fillFields(element, dataList, field) {

    let input = element.target
    let val = input.value
    let list = input.getAttribute('list')
    let options = document.getElementById(list).childNodes
  
    for (let i = 0; i < options.length; i++) {
      if (options[i].value === val) {
        // An item was selected from the list!
        // yourCallbackHere()
        let client = getClientCi(val)[0]
        //send data to inputs
        $('#id_tipo_identificacion').val(client.tipo_identificacion).change()
        $('#id_cedula').val(client.cedula)
        $('#id_nombre_apellido').val(client.nombre_apellido)
        $('#id_telefono').val(client.telefono)
        $('#id_direccion').val(client.direccion)
        $('#id_referencia').val(client.referencia)
        dataList.forEach(function(item) {
          item.innerHTML = ''
        })
        field.blur()
        document.getElementById('id_cedula').onkeyup = null
        document.getElementById('id_nombre_apellido').onkeyup= null
        break;
      }
    }
  }

function getClientCi(cedula) {
espacioCodigo = cedula.search(' ')
return data_client.filter(
    function(data_client) {
    return data_client.cedula == cedula.slice(0, espacioCodigo)
    }
);
}