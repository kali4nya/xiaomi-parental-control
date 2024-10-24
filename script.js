document.getElementById('myButton').addEventListener('click', function() {
    const devices = document.getElementById('devices').value;

    // Get values directly from the inputs
    const cutoffHour = document.getElementById('cutoffHours').value.trim();  // Use trim() to remove extra spaces
    const cutoffMinute = document.getElementById('cutoffMinutes').value.trim();
    const restoreHour = document.getElementById('restoreHours').value.trim();
    const restoreMinute = document.getElementById('restoreMinutes').value.trim();

    // Pad hours and minutes to ensure they are always two digits
    const paddedCutoffHour = padWithLeadingZero(cutoffHour);
    const paddedCutoffMinute = padWithLeadingZero(cutoffMinute);
    const paddedRestoreHour = padWithLeadingZero(restoreHour);
    const paddedRestoreMinute = padWithLeadingZero(restoreMinute);

    // Validate that cutoff and restore times are filled
    if (paddedCutoffHour && paddedCutoffMinute && paddedRestoreHour && paddedRestoreMinute) {
        const cutoffTime = `${paddedCutoffHour}:${paddedCutoffMinute}`;  // Combine hours and minutes for cutoff time
        const restoreTime = `${paddedRestoreHour}:${paddedRestoreMinute}`; // Combine hours and minutes for restore time
        
        const dataString = `devices=${devices}&cutoffTime=${cutoffTime}&restoreTime=${restoreTime}`;
        sendDataToPython(dataString);
        
        // Display the selected values
        alert(
            `Devices: ${devices}\nCutoff Time: ${cutoffTime}\nRestore Time: ${restoreTime}`
        );
    } else {
        alert("Please fill in all time fields before submitting.");
    }
});

// Function to pad numbers with leading zero if they are less than 10
function padWithLeadingZero(value) {
    return value.padStart(2, '0'); // Ensure it's at least 2 digits long
}

function sendDataToPython(dataString) {
    fetch('/execute', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'data=' + encodeURIComponent(dataString) // Encode the data to be safe for URL
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.text();
    })
    .then(data => {
        console.log('Response from server:', data); // Handle the response from the server
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function fetchTimesFromServer() {
    fetch('/get_times')  // Send a GET request to the server
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();  // Parse the response as JSON
        })
        .then(data => {
            console.log('devices:', data.devices);  // Log the devices
            console.log('Cutoff Time:', data.cutoff_time);  // Log the cutoff_time
            console.log('Restore Time:', data.restore_time);  // Log the restore_time
            
            // Check if devices exist and are either an array or a string
            let devices = data.devices;
            if (Array.isArray(devices)) {
                let devicesString = devices.join(',');  // Join devices into a string with commas
                document.getElementById('devices').value = devicesString;  // Display devices
            } else if (typeof devices === 'string') {
                document.getElementById('devices').value = devices;  // Display the string directly
            } else {
                console.warn('Invalid or missing devices');
            }

            // Check if cutoff_time exists and is valid
            if (data.cutoff_time && data.cutoff_time.includes(':')) {
                let cutoffHours = data.cutoff_time.split(':')[0];
                let cutoffMinutes = data.cutoff_time.split(':')[1];
                document.getElementById('cutoffHours').value = cutoffHours;
                document.getElementById('cutoffMinutes').value = cutoffMinutes;
            } else {
                console.warn('Invalid or missing cutoff_time');
            }

            // Check if restore_time exists and is valid
            if (data.restore_time && data.restore_time.includes(':')) {
                let restoreHours = data.restore_time.split(':')[0];
                let restoreMinutes = data.restore_time.split(':')[1];
                document.getElementById('restoreHours').value = restoreHours;
                document.getElementById('restoreMinutes').value = restoreMinutes;
            } else {
                console.warn('Invalid or missing restore_time');
            }
        })
        .catch((error) => {
            console.error('Error fetching times:', error);
        });
}

// Call this function as soon as the page loads
window.addEventListener('load', fetchTimesFromServer);