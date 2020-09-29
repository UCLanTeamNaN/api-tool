// API Looking Glass

const baseUrl = "http://challenge.uclan.ac.uk:8080/preston"

const poll = async (uri) => {
    console.log(`${baseUrl}${uri}`)
    const response = await fetch(`${baseUrl}${uri}`, {redirect: "follow", mode: "no-cors", headers: {
        "Content-Type": "text/plain"
    }})
    .catch(err => console.error(err))
    console.dir(response)
    const data = await response.text()
    console.log(data)
    let result = data.split("\n")
    console.dir(result)
    const status_msg = result[0].split(",")[0].replace('"', "")
    //const status_dsc = response[0].split(",")[1].replace('"', "")
    result.shift()

    return {
        "status_msg": status_msg,
        "data": result
    }
}

const updateMapList = async () => {
    const resp = await poll("/getMaps")
    console.dir(resp)

    if (resp.status_msg == "OK") {
        let tableHtml = ""
        resp.data.forEach(map => {
            console.dir(map)
            const map_name = map[0]
            map.shift()
            const rounds = map

            tableHtml += `<tr><td>${map_name}</td><td>${rounds.toString()}</td></tr>`
            document.getElementById("maps_table").innerHTML = tableHtml
        })
    }
}

updateMapList()