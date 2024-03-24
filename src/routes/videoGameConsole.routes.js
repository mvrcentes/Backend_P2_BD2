import { Router } from "express"

import videoGameConsoleController from "../controllers/videoGameConsole.controllers.js"
const { createVideoGameConsole, getVideoGameConsoles, deleteVideoGameConsole } =
    videoGameConsoleController

const router = Router()

router
    .route("/")
    .post(createVideoGameConsole)
    .get(getVideoGameConsoles)
    .delete(deleteVideoGameConsole)
// .put(updateVideoGameConsole);

export default router
