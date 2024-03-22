import express from 'express'
import cors from 'cors'
import driver from './database.js'

import userRoutes from './routes/user.routes.js'

const app = express()

app.use(cors())
app.use(express.json())

// User routes
app.use('/api/users', userRoutes)


export default app