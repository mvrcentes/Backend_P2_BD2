import driver from "../database.js"

const videogames = {}

videogames.createVideogame = async (req, res) => {
    const { title, price, release, videoGameConsole } = req.body
    const session = driver.session()
    const query =
        "MERGE (a:Videogame {title: $title, price: $price, release: $release, videoGameConsole: $videoGameConsole}) RETURN a"
    try {
        const { records, summary } = await session.run(query, {
            title,
            price,
            release,
            videoGameConsole,
        })
        console.log("Videogame created successfully")
    
        res.json(records)
    } catch (err) {
        res.json(err)
    }
}

videogames.getVideogame = async (req, res) => {
    const { title } = req.body
    const session = driver.session()
    const query = "MATCH (a:Videogame {title: $title}) RETURN a"
    try {
        const { records, summary } = await session.run(query, { title })
        console.log("Videogame found successfully")

        res.json(records)
    } catch (err) {
        res.json(err)
    }
}

videogames.getVideogames = async (req, res) => {
    const session = driver.session()
    const query = "MATCH (a:Videogame) RETURN a"
    try {
        const { records, summary } = await driver.executeQuery(
            query,
            {},
            { database: "neo4j" }
        )
        res.json(records)
    } catch (err) {
        res.json(err)
    }
}

videogames.deleteVideogame = async (req, res) => {
    const { title } = req.body
    const session = driver.session()
    const query = "MATCH (a:Videogame {title: $title}) DELETE a"
    try {
        const { records, summary } = await session.run(query, { title })
        console.log("Videogame deleted successfully")

        res.json(records)
    } catch (err) {
        res.json(err)
    }
}

videogames.updateVideoGame = async (req, res) => {
    const { title, price, release, videoGameConsole } = req.body
    const session = driver.session()

    const videoGame = await session.run("MATCH (v:Videogame {title: $title}) RETURN v", {
        title,
    })

    console.log(videoGame.records[0].get("v").properties)

    const updateVideoGameData = {
        title: title || videoGame.records[0].get("v").properties.title,
        price: price || videoGame.records[0].get("v").properties.price,
        release: release || videoGame.records[0].get("v").properties.release,
        videoGameConsole: videoGameConsole || videoGame.records[0].get("v").properties.videoGameConsole,
    }

    const setClauses = []
    if (title) setClauses.push("v.title = $title")
    if (price) setClauses.push("v.price = $price")
    if (release) setClauses.push("v.release = $release")
    if (videoGameConsole) setClauses.push("v.videoGameConsole = $videoGameConsole")

    const setQuery = setClauses.length > 0 ? "SET " + setClauses.join(", ") : ""

    const query = `MATCH (v:Videogame {title: $title}) ${setQuery} RETURN v`

    try {
        const { records, summary } = await driver.executeQuery(query, {
            title: updateVideoGameData.title,
            price: updateVideoGameData.price,
            release: updateVideoGameData.release,
            videoGameConsole: updateVideoGameData.videoGameConsole,
        })
        console.log("VideoGame updated successfully")
        res.json(records)
    } catch (err) {
        res.json(err)
    }
}


export default videogames
