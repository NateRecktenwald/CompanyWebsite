async function setSale() {
    console.log("trying to set sale");
    const mes = document.getElementById("sale_text").value;
    const response = await fetch("/api/sale", {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify({"message": mes})
    });
    if (response.status != 200) {
        console.log("sale didn't get set correctly");
    }
}

async function endSale() {
    const response = await fetch("/api/sale", {
        method: "DELETE"
    })
    if(response.status != 200) {
        console.log("sale didn't end correctly");
    }
}

const add = document.getElementById("set");
add.addEventListener('click', setSale)

const del = document.getElementById("end");
del.addEventListener('click', endSale)