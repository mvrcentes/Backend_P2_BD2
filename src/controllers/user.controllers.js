import driver from "../database.js"

const users = {}

const greenColor = "\x1b[32m"
const resetColor = "\x1b[0m"

users.createUser = async (req, res) => {
    const { name, age, email, active, favorite_genders } = req.body
    const session = driver.session()
    const query =
        "MERGE (a:User {name: $name, age: $age, email: $email, active: $active, favorite_genders: $favorite_genders}) RETURN a"
    try {
        const { records, summary } = await session.run(query, {
            name,
            age,
            email,
            active,
            favorite_genders,
        })
        console.log("User created successfully")
        console.log(`user: ${greenColor} ${name} ${resetColor}`)
        console.log(`age: ${greenColor} ${age} ${resetColor}`)
        console.log(`email: ${greenColor} ${email} ${resetColor}`)
        console.log(`active: ${greenColor} ${active} ${resetColor}`)
        console.log(
            `favorite_genders: ${greenColor} ${favorite_genders} ${resetColor}`
        )

        res.json(records)
    } catch (err) {
        res.json(err)
    }
}

users.getUser = async (req, res) => {
    const { email } = req.body
    const session = driver.session()
    const query = "MATCH (a:User {email: $email}) RETURN a"
    try {
        const { records, summary } = await session.run(query, { email })
        console.log("User found successfully")

        res.json(records)
    } catch (err) {
        res.json(err)
    }
}

users.getUsers = async (req, res) => {
    const session = driver.session()
    const query = "MATCH (a:User) RETURN a"
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

users.deleteUser = async (req, res) => {
    const { email } = req.body
    const session = driver.session()
    const query = "MATCH (a:User {email: $email}) DELETE a"
    try {
        const result = await session.run(query, { email })
        console.log("User deleted successfully")
        res.json(result)
    } catch (err) {
        res.json(err)
    }
}

users.updateUser = async (req, res) => {
    const { email, name, age, active, favorite_genders } = req.body
    const session = driver.session()

    const user = await session.run("MATCH (a:User {email: $email}) RETURN a", {
        email,
    })

    console.log(user.records[0].get("a").properties)

    const updateUserData = {
        name: name || user.records[0].get("a").properties.name,
        age: age || user.records[0].get("a").properties.age,
        email: email || user.records[0].get("a").properties.email,
        active: active || user.records[0].get("a").properties.active,
        favorite_genders:
            favorite_genders ||
            user.records[0].get("a").properties.favorite_genders,
    }

    // const nameQuery = name ? "SET a.name = $name" : ""
    // const ageQuery = age ? "SET a.age = $age" : ""
    // const emailQuery = email ? "SET a.email = $email" : ""
    // const activeQuery = active ? "SET a.active = $active" : ""
    // const favorite_gendersQuery = favorite_genders ? "SET a.favorite_genres = $favorite_genres" : ""

    const setClauses = []
    if (name) setClauses.push("a.name = $name")
    if (age) setClauses.push("a.age = $age")
    if (email) setClauses.push("a.email = $email")
    if (active) setClauses.push("a.active = $active")
    if (favorite_genders)
        setClauses.push("a.favorite_genders = $favorite_genders")

    // Combinar las cláusulas SET en una cadena
    const setQuery = setClauses.length > 0 ? "SET " + setClauses.join(", ") : ""

    // Construir la consulta completa
    const query = `MATCH (a:User {email: $email}) ${setQuery} RETURN a`

    try {
        const { records, summary } = await driver.executeQuery(query, {
            name: updateUserData.name,
            age: updateUserData.age,
            email: updateUserData.email,
            active: updateUserData.active,
            favorite_genders: updateUserData.favorite_genders,
        })
        console.log("User updated successfully")
        res.json(records)
    } catch (err) {
        res.json(err)
    }
}

export default users
