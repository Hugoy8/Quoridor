const mysql = require('mysql');

// Configuration de la connexion à la base de données MySQL
const pool = mysql.createPool({
    host: 'nl-srv-web859.main-hosting.eu',
    user: 'u338035582_hugo',
    password: '123456789Quoridor',
    database: 'u338035582_Quoridor',
    connectionLimit: 10,
});


exports.getProfile = (req, res) => {
    const userId = req.params.id;

    // Requête pour récupérer le profil utilisateur
    const profileQuery = `SELECT id, username, win, games, money FROM users WHERE id = ?`;
    pool.query(profileQuery, [userId], (err, profileResults) => {
        if (err) {
            console.error('Erreur lors de la récupération du profil utilisateur :', err);
            res.status(500).json({ error: 'Erreur lors de la récupération des données du profil utilisateur' });
        } else {
            if (profileResults.length > 0) {
                const profile = profileResults[0];

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