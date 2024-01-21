// For Url analysis

const predictedTabs = new Set();

chrome.webNavigation.onCommitted.addListener(async function (details) {
    const url = details.url;
    const tabId = details.tabId;
    // console.log(predictedTabs)

    // Check if the URL is the new tab page or a blank URL
    // Check if the URL is the new tab page, a blank URL, or the Chrome homepage
    if (
        url.toLowerCase().startsWith('chrome://newtab/') ||
        url === '' ||  // Check if the URL is empty
        url.toLowerCase().startsWith('chrome://homepage/')
    ) {
        // Handle new tab opening, blank URL, or Chrome homepage
        predictedTabs.delete(tabId); // Clear the record for this tab
        return;
    }


    // Check if the URL is the new tab page
    if (url.toLowerCase().startsWith('chrome://newtab/')
        || url === 'chrome://newtab/') {
        // Handle new tab opening
        predictedTabs.delete(tabId); // Clear the record for this tab
        return;
    }

    // Check if prediction is already performed for this tab
    if (predictedTabs.has(tabId)) {
        return;
    }

    // Continue with phishing detection
    try {
        // Fetch the URL content and send it to your Flask API
        const response = await fetch('http://127.0.0.1:5000/checkUrl', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url }),
        });

        const data = await response.json();
        const result = data.prediction === 'bad' ? 'This is a Phishing Site' : 'This is not a Phishing Site';

        if (data.prediction === 'bad') {
            // Show an alert instead of redirecting to the warning page
            const warningMessage = "Warning: This is a custom alert for the predicted tab.";
            alert(warningMessage);

            // Mark this tab as predicted (you may still need this for your logic)
            predictedTabs.add(tabId);
            // Show the intermediate warning page
            // const warningPage = chrome.runtime.getURL('warning.html') + `?url=${encodeURIComponent(url)}`;
            // predictedTabs.add(tabId); // Mark this tab as predicted
            // chrome.tabs.update({ url: warningPage });
        } else {
            // If prediction is good, log it or take other actions
            console.log('Good prediction:', result);
        }
    } catch (error) {
        console.error('Error during prediction:', error);
        // Handle the error
    }

});


// For QR Authentication
chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
    if (changeInfo.url) {
        // Send the URL to the Flask server
        fetch('http://127.0.0.1:5000/check_url', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: changeInfo.url }),
        })
            .then(response => response.json())
            .then(data => {
                if (data.protected) {
                    chrome.tabs.update(tabId, { url: 'http://127.0.0.1:5000/qr_code' });
                }
            })
            .catch(error => console.error('Error checking URL:', error));
    }
});
