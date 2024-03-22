import driver from "../database.js"

const reviews = {}

const greenColor = "\x1b[32m"
const resetColor = "\x1b[0m"

reviews.createReview = async (req, res) => {
    const { title, content, rating, date, good } = req.body
    const session = driver.session()
    const query =
        "MERGE (a:Review {title: $title, content: $content, rating: $rating, date: $date, good: $good}) RETURN a"

    try {
        const { records, summary } = await session.run(query, {
            title,
            content,
            rating,
            date,
            good,
        })
        console.log("Review created successfully")
        console.log(`title: ${greenColor} ${title} ${resetColor}`)
        console.log(`content: ${greenColor} ${content} ${resetColor}`)
        console.log(`rating: ${greenColor} ${rating} ${resetColor}`)
        console.log(`date: ${greenColor} ${date} ${resetColor}`)
        console.log(`good: ${greenColor} ${good} ${resetColor}`)

        res.json(records)
    } catch (err) {
        res.json(err)
    }
}

reviews.getReview = async (req, res) => {
    const { title } = req.body
    const session = driver.session()
    const query = "MATCH (a:Review {title: $title}) RETURN a"
    try {
        const { records, summary } = await session.run(query, { title })
        console.log("Review found successfully")

        res.json(records)
    } catch (err) {
        res.json(err)
    }
}

reviews.getReviews = async (req, res) => {
    const session = driver.session()
    const query = "MATCH (a:Review) RETURN a"
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

reviews.deleteReview = async (req, res) => {
    const { title } = req.body
    const session = driver.session()
    const query = "MATCH (a:Review {title: $title}) DELETE a"
    try {
        const { records, summary } = await session.run(query, { title })
        console.log("Review deleted successfully")

        res.json(records)
    } catch (err) {
        res.json(err)
    }
}

reviews.updateReview = async (req, res) => {
    const { title, content, rating, date, good } = req.body
    const session = driver.session()

    const review = await session.run("MATCH (r:Review {title: $title}) RETURN r", {
        title,
    })

    console.log(review.records[0].get("r").properties)

    const updateReviewData = {
        title: title || review.records[0].get("r").properties.title,
        content: content || review.records[0].get("r").properties.content,
        rating: rating || review.records[0].get("r").properties.rating,
        date: date || review.records[0].get("r").properties.date,
        good: good || review.records[0].get("r").properties.good,
    }

    const setClauses = []
    if (content) setClauses.push("r.content = $content")
    if (rating) setClauses.push("r.rating = $rating")
    if (date) setClauses.push("r.date = $date")
    if (good) setClauses.push("r.good = $good")

    const setQuery = setClauses.length > 0 ? "SET " + setClauses.join(", ") : ""

    const query = `MATCH (r:Review {title: $title}) ${setQuery} RETURN r`

    try {
        const { records, summary } = await driver.executeQuery(query, {
            title: updateReviewData.title,
            content: updateReviewData.content,
            rating: updateReviewData.rating,
            date: updateReviewData.date,
            good: updateReviewData.good,
        })
        console.log("Review updated successfully")
        res.json(records)
    } catch (err) {
        res.json(err)
    }
}


export default reviews