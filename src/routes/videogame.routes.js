import { Router } from "express"

import videoGameController from "../controllers/videogame.controllers.js"
const { createVideogame, getVideogame, getVideogames, deleteVideogame, updateVideoGame } = videoGameController
const router = Router()

router
    .route("/videogame")
    .post(createVideogame)
    .get(getVideogame)
    .delete(deleteVideogame)
    .put(updateVideoGame) 

// router.route("/videogames").get(getVideoGames)

export default router
