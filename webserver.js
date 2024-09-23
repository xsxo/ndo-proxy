var host = window.location.hostname
var port = parseInt(window.location.port) + 2

const socket = new WebSocket('ws://' + host + ':' + port);

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);

    const networkBody = document.getElementById('network-body');

    const existingRow = document.querySelector(`tr[data-number='${data.number}']`);

    if (existingRow) {
        updateRow(existingRow, data);
    } else {
        const newRow = createRow(data);
        networkBody.insertBefore(newRow, networkBody.firstChild);
    }
};

function createRow(data) {
    const row = document.createElement('tr');
    row.dataset.number = data.number;
    row.dataset.method = data.method;
    row.dataset.api = data.api;
    row.dataset.responseStatusCode = data.response_status_code || '';
    row.dataset.rawRequest = data.raw_request || '';
    row.dataset.rawResponse = data.raw_response || '';
    row.dataset.time = data.time;

    row.innerHTML = `
        <td>${data.number}</td>
        <td>${data.method}</td>
        <td>${data.api}</td>
        <td>${data.response_status_code || ''}</td>
        <td>${new Date(data.time).toLocaleTimeString()}</td>
        <td><button class='delete-btn' onclick='deleteRow(event)'>Delete</button></td>
    `;

    row.onclick = function() {
        displayDetails(this.dataset);
    };

    return row;
}

function updateRow(row, data) {
    if (data.raw_request) {
        row.dataset.rawRequest = data.raw_request;
    }
    if (data.raw_response) {
        row.dataset.rawResponse = data.raw_response;
    }
    row.dataset.method = data.method;
    row.dataset.api = data.api;
    row.dataset.responseStatusCode = data.response_status_code || row.dataset.responseStatusCode;
    row.dataset.time = data.time;

    row.innerHTML = `
        <td>${data.number}</td>
        <td>${data.method}</td>
        <td>${data.api}</td>
        <td>${data.response_status_code || ''}</td>
        <td>${new Date(data.time).toLocaleTimeString()}</td>
        <td><button class='delete-btn' onclick='deleteRow(event)'>Delete</button></td>
    `;
    
    // تأكد من عرض التحديثات بعد كل تعديل
    displayDetails(row.dataset);
}

function displayDetails(data) {
    document.getElementById('raw-request-content').textContent = data.rawRequest || '';
    document.getElementById('raw-response-content').textContent = data.rawResponse || '';
}

function deleteRow(event) {
    event.stopPropagation();
    const row = event.target.closest('tr');
    if (row) {
        row.remove();
    }
}