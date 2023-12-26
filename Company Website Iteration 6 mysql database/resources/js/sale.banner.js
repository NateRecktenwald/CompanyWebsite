

async function updateSale() {
    const response = await fetch("/api/sale", {method: "GET"});

    if (response.status == 200) {
        let dis = document.getElementById("sales_banner");
        try {
            const mes = await response.json();
            // const arr = JSON.parse(mes);
            // console.log(arr);
            console.log(mes.endTime);
            if(mes.endTime == null) {
                let sec = mes.content.replace("<", "&lt");
                sec.replace(">", "&gt")
                dis.innerText = sec;
                dis.style.visibility = 'visible';
            }
            else {
                dis.style.visibility = 'hidden';
            }
        }
        catch {
            console.log("no sale dislayed");
        }
    }
    else {
        console.log("sale message was not sent correctly")
    }
}

setInterval(updateSale, 1000);
