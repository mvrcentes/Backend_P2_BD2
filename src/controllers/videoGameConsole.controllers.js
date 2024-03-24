import driver from "../database.js"

const videoGameConsoles = {}

const greenColor = "\x1b[32m"
const resetColor = "\x1b[0m"

videoGameConsoles.createVideoGameConsole = async (req, res) => {
    const { name, developed, release_date, available, exclusives } = req.body
    const session = driver.session()
    const query =
        "MERGE (a:VideoGameConsole {name: $name, developed: $developed, release_date: $release_date, available: $available, exclusives: $exclusives}) RETURN a"

    try {
        const { records, summary } = await session.run(query, {
            name,
            developed,
            release_date,
            available,
            exclusives,
        })
        console.log("VideoGameConsole created successfully")
        console.log(`name: ${greenColor} ${name} ${resetColor}`)
        console.log(`developed: ${greenColor} ${developed} ${resetColor}`)
        console.log(`release_date: ${greenColor} ${release_date} ${resetColor}`)
        console.log(`available: ${greenColor} ${available} ${resetColor}`)
        console.log(
            `exclusives: ${greenColor} ${exclusives} ${resetColor}`
        )
    
        res.json(records)
    } catch (err) {
        res.json(err)
    }
}

videoGameConsoles.getVideoGameConsole = async (req, res) => {
    const { name } = req.body
    const session = driver.session()
    const query = "MATCH (a:VideoGameConsole {name: $name}) RETURN a"
    try {
        const { records, summary } = await session.run(query, { name })
        console.log("VideoGameConsole found successfully")

        res.json(records)
    } catch (err) {
        res.json(err)
    }
}

videoGameConsoles.getVideoGameConsoles = async (req, res) => {
    const session = driver.session()
    const query = "MATCH (a:VideoGameConsole) RETURN a"
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

videoGameConsoles.deleteVideoGameConsole = async (req, res) => {
    const { name } = req.body
    const session = driver.session()
    const query = "MATCH (a:VideoGameConsole {name: $name}) DETACH DELETE a"
    try {
        const { records, summary } = await session.run(query, { name })
        console.log("VideoGameConsole deleted successfully")
        res.json(records)
    } catch (err) {
        res.json(err)
    }
}

export default videoGameConsoles