
/* the calculation fucntion looks at how many vowels the user put in the name and then adds a preditermined number 
   to the num_emails based on which select catagory they chose and adding those together gets the number of emails
   per week the user can expect to recieve
*/
function calculation() {

    let disp = document.getElementById("calculation");
    let num_emails = 0;

    for (let i = 0; i < name.value.length; i++) {
        let curr_char = name.value.charAt(i);
        if(curr_char == 'a' || curr_char == 'e' || curr_char == 'i' || curr_char == 'o' || curr_char == 'u') {
            num_emails += 1;
        }
        if(curr_char == 'A' || curr_char == 'E' || curr_char == 'I' || curr_char == 'O' || curr_char == 'U') {
            num_emails += 1;
        }
    }

    if (news.value == "all") {
        num_emails += 10
    }
    else if (news.value == "parks") {
        num_emails += 8;
    }
    else if (news.value == "movies") {
        num_emails += 6;
    }
    else if (news.value == "shows") {
        num_emails += 4;
    }
    else if (news.value == "cruise") {
        num_emails += 2;
    }

    disp.innerText = num_emails + " emails a week";
}


let news = document.getElementById("news");
let name = document.getElementById("name");

news.addEventListener('change', calculation);
name.addEventListener('change', calculation);