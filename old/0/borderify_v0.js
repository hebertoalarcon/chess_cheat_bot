document.body.style.border = "20px solid green";

let elementToObserve = document.getElementsByTagName("vertical-move-list");

const observer = new MutationObserver((mutations) => {
    mutations.forEach(function (mutation) {
        if (mutation.addedNodes.length != 0) {
            console.log("Observed mutation:", mutation.addedNodes);
        }
    })
});

observer.observe(elementToObserve[0], { subtree: true, childList: true });