import express from 'express'
import cors from 'cors'


import userRoutes from './routes/user.routes.js'
import videoGameRoutes from './routes/videogame.routes.js'
import reviewRoutes from './routes/review.routes.js'
import videoGameConsoleRoutes from './routes/videoGameConsole.routes.js'

const app = express()

app.use(cors())
app.use(express.json())


app.use('/api/users', userRoutes)
app.use('/api/videogames', videoGameRoutes)
app.use('/api/reviews', reviewRoutes)
app.use('/api/videoGameConsoles', videoGameConsoleRoutes)

export default app