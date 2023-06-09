const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');

router.get('/profil/:id', userController.getProfile);
router.get('/game-history/:id', userController.getGameHistory);

module.exports = router;