const express = require('express');
const router = express.Router();
const playerController = require('../controllers/playerController');

router.get('/top-players', playerController.getTopPlayers);
router.get('/default-players', playerController.getDefaultPlayers);
router.get('/search-players', playerController.searchPlayers);

module.exports = router;