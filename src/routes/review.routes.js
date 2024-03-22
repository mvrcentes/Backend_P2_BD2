import { Router } from "express"

import reviewController from "../controllers/review.controllers.js"
const { createReview, getReview, getReviews, deleteReview, updateReview } = reviewController

const router = Router()

router
    .route("/")
    .post(createReview)
    .get(getReviews)
    .delete(deleteReview)
    .put(updateReview)




export default router