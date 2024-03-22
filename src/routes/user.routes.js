import { Router } from "express"

import userController from "../controllers/user.controllers.js"
const { createUser } = userController

const router = Router()

router.route("/")
    .post(createUser)

export default router