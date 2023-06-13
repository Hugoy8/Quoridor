const mysql = require('mysql');
const crypto = require('crypto');
const jwt = require('jsonwebtoken');


// Configuration de la connexion à la base de données MySQL
const pool = mysql.createPool({
    host: 'nl-srv-web859.main-hosting.eu',
    user: 'u338035582_hugo',
    password: '123456789Quoridor',
    database: 'u338035582_Quoridor',
    connectionLimit: 10,
});

exports.signup = (req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    const { username, password, confirmPassword } = req.body;
    if (!username || !password || !confirmPassword) {
        return res.status(400).json({ error: 'Veuillez remplir tous les champs' });
    }
    if (password !== confirmPassword) {
        return res.status(400).json({ error: 'Les mots de passe ne correspondent pas' });
    }

    // Check if username already exists
    const checkUsernameQuery = `SELECT username FROM users WHERE username = '${username}'`;
    pool.query(checkUsernameQuery, (err, result) => {
        if (err) {
            console.error('Erreur lors de la vérification du nom d\'utilisateur :', err);
            return res.status(500).json({ error: 'Erreur lors de la vérification du nom d\'utilisateur' });
        }

        if (result.length > 0) {
            return res.status(400).json({ error: 'Ce nom d\'utilisateur est déjà pris' });
        }
        
        const hashedPassword = crypto.createHash('sha256').update(password).digest('hex');

        const query = `INSERT INTO users (username, password) VALUES ('${username}', '${hashedPassword}')`;
        pool.query(query, (err) => {
            if (err) {
                console.error('Erreur lors de la création du compte :', err);
                return res.status(500).json({ error: 'Erreur lors de la création du compte' });
            } else {
                res.json({ message: 'Compte créé avec succès' });
            }
        });
    });
};

exports.login = (req, res) => {
    const username = req.body.username;
    const password = req.body.password;
    if (!username || !password) {
        return res.status(400).json({ error: 'Veuillez remplir tous les champs' });
    }

    const hashedPassword = crypto.createHash('sha256').update(password).digest('hex');

    const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${hashedPassword}'`;
    pool.query(query, (err, results) => {
        if (err) {
            console.error('Erreur lors de la connexion :', err);
            res.status(500).json({ error: 'Erreur lors de la connexion' });
        } else {
            if (results.length > 0) {
                const user = results[0];
                const token = jwt.sign({ id: user.id, username: user.username }, 'your-secret-key', { expiresIn: '1h' });
                res.json({ message: 'Connecté avec succès', token });
            } else {
                res.status(401).json({ error: 'Nom d\'utilisateur ou mot de passe incorrect' });
            }
        }
    });
};

exports.getProfile = (req, res) => {
    const userId = req.params.id;

    // Requête pour récupérer le profil utilisateur
    const profileQuery = `SELECT id, username, win, games, money, maps FROM users WHERE id = ?`;
    pool.query(profileQuery, [userId], (err, profileResults) => {
        if (err) {
            console.error('Erreur lors de la récupération du profil utilisateur :', err);
            res.status(500).json({ error: 'Erreur lors de la récupération des données du profil utilisateur' });
        } else {
            if (profileResults.length > 0) {
                const profile = profileResults[0];
                const maps = profile.maps.split(',').map(map => map.trim());
                profile.Electricity = maps.includes('Electricity');
                profile.Ice = maps.includes('Ice');
                profile.Sugar = maps.includes('Sugar');
                
                // Requête pour calculer le classement du joueur
                const rankingQuery = `SELECT COUNT(*) AS ranking FROM users WHERE win >= ?`;
                pool.query(rankingQuery, [profile.win], (err, rankingResults) => {
                    if (err) {
                        console.error('Erreur lors du calcul du classement du joueur :', err);
                        res.status(500).json({ error: 'Erreur lors du calcul du classement du joueur' });
                    } else {
                        const ranking = rankingResults[0].ranking;

                        // Requête pour récupérer le nombre total de joueurs
                        const countQuery = `SELECT COUNT(*) AS totalPlayers FROM users`;
                        pool.query(countQuery, (err, countResults) => {
                            if (err) {
                                console.error('Erreur lors de la récupération du nombre total de joueurs :', err);
                                res.status(500).json({ error: 'Erreur lors de la récupération du nombre total de joueurs' });
                            } else {
                                const totalPlayers = countResults[0].totalPlayers;

                                // Ajoutez les informations de classement et de nombre total de joueurs au profil
                                profile.ranking = ranking;
                                profile.totalPlayers = totalPlayers;

                                res.json(profile);
                            }
                        });
                    }
                });
            } else {
                res.status(404).json({ error: 'Utilisateur non trouvé' });
            }
        }
    });
};

exports.getGameHistory = (req, res) => {
    const userId = req.params.id;

    const historyQuery = `SELECT * FROM game_history WHERE user_id = ?`;
    pool.query(historyQuery, [userId], (err, historyResults) => {
        if (err) {
            console.error('Erreur lors de la récupération de l\'historique des parties :', err);
            res.status(500).json({ error: 'Erreur lors de la récupération de l\'historique des parties' });
        } else {
            res.json(historyResults);
        }
    });
};

exports.getPurchaseHistory = (req, res) => {
    const userId = req.params.id;

    const historyQuery = `SELECT * FROM purchases WHERE user_id = ? ORDER BY purchase_time DESC`;
    pool.query(historyQuery, [userId], (err, historyResults) => {
        if (err) {
            console.error('Erreur lors de la récupération de l\'historique des achats :', err);
            res.status(500).json({ error: 'Erreur lors de la récupération de l\'historique des achats' });
        } else {
            res.json(historyResults);
        }
    });
};

exports.purchaseMap = (req, res) => {
    const { userId, mapName } = req.body;
    const mapPrices = {
        Ice: 1000,
        Electricity: 2500,
        Sugar: 5000,
    };

    const price = mapPrices[mapName];
    if (!price) {
        return res.status(400).json({ error: 'Carte invalide' });
    }

    const checkBalanceQuery = `SELECT money, maps FROM users WHERE id = ${userId}`;
    pool.query(checkBalanceQuery, (err, result) => {
        if (err) {
            console.error('Erreur lors de la vérification du solde :', err);
            return res.status(500).json({ error: 'Erreur lors de la vérification du solde' });
        }

        const user = result[0];
        if (user.money < price) {
            return res.status(400).json({ error: 'Solde insuffisant' });
        }

        if (user.maps.split(',').map(map => map.trim()).includes(mapName)) {
            return res.status(400).json({ error: 'Carte déjà achetée' });
        }

        const newBalance = user.money - price;
        const newMaps = user.maps ? `${user.maps}, ${mapName}` : mapName;

        const updateQuery = `UPDATE users SET money = ${newBalance}, maps = '${newMaps}' WHERE id = ${userId}`;
        pool.query(updateQuery, (err) => {
            if (err) {
                console.error('Erreur lors de l\'achat de la carte :', err);
                return res.status(500).json({ error: 'Erreur lors de l\'achat de la carte' });
            }

            const purchaseTime = new Date().toISOString().slice(0, 19).replace('T', ' ');

            const insertPurchaseQuery = `INSERT INTO purchases (user_id, map_name, purchase_time) VALUES (${userId}, '${mapName}', '${purchaseTime}')`;
            pool.query(insertPurchaseQuery, (err) => {
                if (err) {
                    console.error('Erreur lors de l\'ajout de l\'achat à l\'historique :', err);
                    return res.status(500).json({ error: 'Erreur lors de l\'ajout de l\'achat à l\'historique' });
                }
            
                res.json({ message: 'Carte achetée avec succès', newBalance });
            });            
        });
    });
};
