import express from 'express'
import cors from 'cors'
import driver from './database.js'

import userRoutes from './routes/user.routes.js'
import videoGameRoutes from './routes/videogame.routes.js'
import reviewRoutes from './routes/review.routes.js'

const app = express()

app.use(cors())
app.use(express.json())


app.use('/api/users', userRoutes)
app.use('/api/videogames', videoGameRoutes)
app.use('/api/reviews', reviewRoutes)


export default app