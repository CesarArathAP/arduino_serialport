async function fetchData() {
  const response = await fetch('/datos_serial');
  const data = await response.json();
  const serialDataElement = document.getElementById('serial-data');
  serialDataElement.textContent = data.datos[data.datos.length - 1]; // Mostrar solo el último dato
}

fetchData();
setInterval(fetchData, 1000); // Actualizar cada segundo
