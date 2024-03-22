import neo4j from "neo4j-driver"
import dotenv from "dotenv"
dotenv.config({ path: "./.env" })

const URI = process.env.NEO4J_URI
const USER = process.env.NEO4J_USERNAME
const PASSWORD = process.env.NEO4J_PASSWORD

const driver = neo4j.driver(URI, neo4j.auth.basic(USER, PASSWORD))

async function establishConnection() {
    let session

    try {
        session = driver.session()
        const serverInfo = await driver.getServerInfo()
        console.log("Connection established")
        console.log(serverInfo)
    } catch (err) {
        console.log(`Connection error\n${err}\nCause: ${err.cause}`)
    } finally {
        if (session) await session.close()
    }
}

establishConnection()

export default driver
