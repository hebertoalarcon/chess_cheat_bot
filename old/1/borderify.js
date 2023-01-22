    document.body.style.border = "20px solid green";

// var process_moves = (el) => {
//     move_list = []

//     var listOfChildren = el.children;

//     for (let item of listOfChildren) {
//         let moveData = item.children;
//         for (let m of moveData) {
//             found_data = {}
//             let att = { ...m.attributes };
//             let keys = Object.keys(att);
//             for (let index = 0; index < keys.length; index++) {
//                 let found_att = att[index];
//                 if (found_att-name == "data-ply") {
//                     found_data['ply'] = found_att.nodeValue;
//                 }
//             }
//             found_data['move'] = m.innerHTML;
//             move_list.push(found_data);
//         }
//     }
//     let mstr = "";
//     for (let index = 0; index < move_list.length; index++) {
//         const element = move_list[index];
//         mstr += `${element['move']}`
//         if (index < move_list.length - 1) {
//             mstr += "_"
//         }
//     }
//     console.log(JSON.stringify({ moves: mstr }));


//     fetch("http://localhost:5000/game_moves", { 
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json'}, //,'Access-Control-Allow-Origin': '*' 
//         body: JSON.stringify({ moves: mstr })
//     }).then(res => console.log("res:", res));
// }


let elementToObserve = document.getElementsByTagName("vertical-move-list");


const observer = new MutationObserver((mutations) => {
    mutations.forEach(function (mutation) {
        if (mutation.addedNodes.length != 0) {
            console.log("Observed mutation:", mutation.addedNodes);
            // process_moves(elementToObserve[0])
        }
    })
});

observer.observe(elementToObserve[0], { subtree: true, childList: true });