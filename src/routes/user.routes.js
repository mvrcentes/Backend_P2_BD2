import { Router } from "express"

import userController from "../controllers/user.controllers.js"
const { createUser, getUser, getUsers, updateUser, deleteUser } = userController
const router = Router()

router
    .route("/user")
    .post(createUser)
    .get(getUser)
    .put(updateUser)
    .delete(deleteUser)

router.route("/users").get(getUsers)

export default router
