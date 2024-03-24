import { Router } from "express"

import developerController from "../controllers/developer.controllers.js"
const { createDeveloper, getDeveloper, getDevelopers, deleteDeveloper } = developerController

const router = Router()

router
    .route("/")
    .post(createDeveloper)
    .get(getDevelopers)
    .delete(deleteDeveloper)

export default router
