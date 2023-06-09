const express = require('express');
const router = express.Router();
const authController = require('../controllers/authController');

router.post('/signup', authController.signup);
router.post('/login', authController.login);
router.get('/profile/:id', authController.getProfile);
router.get('/game-history/:id', authController.getGameHistory);
router.post('/purchase-map', authController.purchaseMap);

module.exports = router;
