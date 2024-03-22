import driver from "../database.js"

const users = {}

users.createUser = async (req, res) => {
    const { name, email } = req.body
    const session = driver.session()
    const query = 'MERGE (a:User {name: $name, email: $email}) RETURN a'
    try {
        const result = await session.run(query, { name, email })
        res.json(result)
    } catch (err) {
        res.json(err)
    } 
}

export default users
