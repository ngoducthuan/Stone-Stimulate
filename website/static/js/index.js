// document.addEventListener('DOMContentLoaded', function () {
//     var alertElement = document.getElementById('autoDismissAlert');
//     var closeButton = document.getElementById('manualCloseButton');

//     // Function to close the alert
//     function closeAlert() {
//         var alertInstance = bootstrap.Alert.getOrCreateInstance(alertElement);
//         alertInstance.close();
//     }

//     // Set up a timer to automatically close the alert after 5 seconds
//     var autoDismissTimer = setTimeout(closeAlert, 5000); // 5000 milliseconds = 5 seconds

//     // Add event listener to the close button
//     closeButton.addEventListener('click', function () {
//         clearTimeout(autoDismissTimer); // Clear the auto-dismiss timer
//         closeAlert(); // Close the alert immediately
//     });
// });

function deleteNote(noteId){
    fetch('/delete-note', {
        method: "POST",
        body: JSON.stringify({ noteId: noteId}),
    }).then((_res)=> {
        window.location.href = "/notes"
    });
}

function deleteUser(userEmail){
    fetch('/delete-user', {
        method: "POST",
        body: JSON.stringify({ userEmail:userEmail}),
    }).then((_res)=> {
        window.location.href ="/admin"
    });
}

function submitForm(event) {
    event.preventDefault();
    
    var hash = document.getElementById('hash').value;
    var baseUrl = 'https://www.virustotal.com/api/v3/files/';
    var fullUrl = baseUrl + hash;
    
    var formData = new FormData();
    formData.append('full_url', fullUrl);
    formData.append('hash', hash);
    
    fetch('/check_hash', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        var resultDiv = document.getElementById('result');
        
        // Kiểm tra dữ liệu để xác định nếu có lỗi
        if (data.includes('Error:') || data.includes('Unable to fetch data')) {
            resultDiv.innerHTML = `<h2>${data}</h2>`;  // Hiển thị thông báo lỗi
        } else {
            resultDiv.innerHTML = `<pre>${data}</pre>`;  // Hiển thị dữ liệu trả về
        }
    })
    .catch(error => {
        console.error('Error:', error);
        var resultDiv = document.getElementById('result');
        resultDiv.innerHTML = `<h2>Error: ${error.message}</h2>`;
    });
}