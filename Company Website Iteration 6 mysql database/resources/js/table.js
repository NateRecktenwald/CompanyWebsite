
//table date
function addTimeUntil() {
    let curr_time = new Date();
    for(let i = 1; i < children.length; i++) {
        let input_date = children[i].children[2].innerText;
        let strArr = input_date.split("-");
        let dateStr = strArr[0] + "-" + strArr[1] + "-" + strArr[2] + "  - ";
        let userDate = new Date(parseInt(strArr[0]), parseInt(strArr[1]) - 1, parseInt(strArr[2]));

        if (userDate.getTime() - curr_time.getTime() < 0) {
            children[i].children[2].innerText = dateStr + " Past";
        } 
        else {
            let days = Math.floor((userDate.getTime() - curr_time.getTime())/86400000);
            let rem = (userDate.getTime() - curr_time.getTime()) % 86400000;
            let hours = Math.floor(rem / 3600000);
            rem = rem % 3600000;
            let mins = Math.floor(rem / 60000);
            rem = rem % 60000;
            let seconds = Math.floor(rem / 1000);
            let diff = days.toString() + " days, " + hours.toString() + " hours, " + mins.toString() + " minutes, " 
                    + seconds.toString() + " seconds, ";
            children[i].children[2].innerText = dateStr + " " + diff;
        }
    }
}

setInterval(addTimeUntil, 1000);



let body = document.getElementById("table_body");
children = body.children;
let curr_row_id = "index0";
let curr_index = 1;

for(let i = 1; i < children.length; i++) {
    curr_index = i;
    let curr_button = children[i].children[5].children[0]

    async function rowDelete() {
        
        const response = await fetch("/api/contact", { 
            method: "DELETE", 
            headers: { "Content-Type": "application/json"}, 
            body: JSON.stringify({"id": curr_button.id, "length": 2})});

        if(response.status == 200 || response.status == 404) {
            document.getElementById("index" + curr_button.id.toString()).remove();
        }
        else {
            console.log("invalid fetch sent");
        }
        
    }

    curr_button.addEventListener('click', rowDelete);

    
}

