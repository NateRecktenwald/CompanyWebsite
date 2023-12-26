
//table date
function addTimeUntil() {
    let curr_time = new Date();
    for(let i = 1; i < children.length; i++) {
        let input_date = children[i].children[2].innerText;
        let strArr = input_date.split("-");
        let dateStr = strArr[0] + "-" + strArr[1] + "-" + strArr[2] + "  - ";
        let userDate = new Date(parseInt(strArr[2]), parseInt(strArr[0]) - 1, parseInt(strArr[1]));

        if (userDate.getTime() - curr_time.getTime() < 0) {
            console.log(children[i].children[2].innerText);
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
            console.log(children[i].children[2].innerText.children);
            children[i].children[2].innerText = dateStr + " " + diff;
        }
    }
}

setInterval(addTimeUntil, 1000);


//row deletion
function rowDelete() {
    document.getElementById(curr_row_id).remove();

    for(let i = 1; i < body.children.length; i++) {
        body.children[i].id = "index " + (i - 1).toString();
    }
}

let body = document.getElementById("table_body");
children = body.children;
let curr_row_id = "index 0";
let curr_index = 1;

for(let i = 1; i < children.length; i++) {
    curr_index = i;
    let curr_row_id = "index " + (i - 1).toString();
    let curr_button = children[i].children[5].children[0]
    curr_button.addEventListener('click', rowDelete);
}
