const details = document.getElementById('details');
const closeBtn2 = document.getElementById('close-btn');
const responseContent = document.getElementById('raw-response-content');
const requestContent = document.getElementById('raw-request-content');
const rawRequest = document.getElementById('raw_request');
const rawResponse = document.getElementById('raw_response')

closeBtn2.addEventListener('click', () => {
    closeBtn2.classList.add('hidden-button')
    details.classList.add('hidden-flex');
    rawRequest.classList.add('hidden-flex')
    rawResponse.classList.add('hidden-flex')
});

const observer = new MutationObserver(() => {
    if (details.classList.contains('hidden-flex')) {
        details.classList.remove('hidden-flex');
        closeBtn2.classList.remove('hidden-button')
        rawRequest.classList.remove('hidden-flex')
        rawResponse.classList.remove('hidden-flex')
    }
});

observer.observe(requestContent, { childList: true, subtree: true });
observer.observe(responseContent, { childList: true, subtree: true });
