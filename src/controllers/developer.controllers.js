import driver from "../database.js"

const developers = {}

const greenColor = "\x1b[32m"
const resetColor = "\x1b[0m"

developers.createDeveloper = async (req, res) => {
    const { name, founded, location, website, rating } = req.body
    const session = driver.session()
    const query =
        "MERGE (a:Developer {name: $name, founded: $founded, location: $location, website: $website, rating: $rating}) RETURN a"

    try {
        const { records, summary } = await session.run(query, {
            name,
            founded,
            location,
            website,
            rating,
        })
        console.log("Developer created successfully")
        console.log(`name: ${greenColor} ${name} ${resetColor}`)
        console.log(`founded: ${greenColor} ${founded} ${resetColor}`)
        console.log(`location: ${greenColor} ${location} ${resetColor}`)
        console.log(`website: ${greenColor} ${website} ${resetColor}`)
        console.log(`rating: ${greenColor} ${rating} ${resetColor}`)

        res.json(records)
    } catch (err) {
        res.json(err)
    }
}

developers.getDeveloper = async (req, res) => {
    const { name } = req.body
    const session = driver.session()
    const query = "MATCH (a:Developer {name: $name}) RETURN a"
    try {
        const { records, summary } = await session.run(query, { name })
        console.log("Developer found successfully")

        res.json(records)
    } catch (err) {
        res.json(err)
    }
}

developers.getDevelopers = async (req, res) => {
    const session = driver.session()
    const query = "MATCH (a:Developer) RETURN a"
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

developers.deleteDeveloper = async (req, res) => {
    const { name } = req.body
    const session = driver.session()
    const query = "MATCH (a:Developer {name: $name}) DETACH DELETE a"
    try {
        const { records, summary } = await session.run(query, { name })
        console.log("Developer deleted successfully")

        res.json(records)
    } catch (err) {
        res.json(err)
    }
}

export default developers