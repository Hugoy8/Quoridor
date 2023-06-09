const mysql = require('mysql');
// Configuration de la connexion à la base de données MySQL
const pool = mysql.createPool({
    host: 'nl-srv-web859.main-hosting.eu',
    user: 'u338035582_hugo',
    password: '123456789Quoridor',
    database: 'u338035582_Quoridor',
    connectionLimit: 10,
});

exports.getTopPlayers = (req, res) => {
    const query = 'SELECT username, win, id FROM users ORDER BY win DESC LIMIT 3';
    pool.query(query, (err, results) => {
        if (err) {
            console.error('Erreur lors de la récu   pération des meilleurs joueurs :', err);
            res.status(500).json({ error: 'Erreur lors de la récupération des données' });
        } else {
            res.json(results);
        }
    });
};

exports.getDefaultPlayers = (req, res) => {
    const query = 'SELECT username, win, id FROM users ORDER BY win DESC LIMIT 10';
    pool.query(query, (err, results) => {
        if (err) {
            console.error('Erreur lors de la récupération des joueurs par défaut :', err);
            res.status(500).json({ error: 'Erreur lors de la récupération des données' });
        } else {
            res.json(results);
        }
    });
};

exports.searchPlayers = (req, res) => {
    const searchTerm = req.query.username;
    const query = `SELECT username, win, id FROM users WHERE username LIKE '%${searchTerm}%' ORDER BY win DESC`;

    pool.query(query, (err, results) => {
        if (err) {
            console.error('Erreur lors de la recherche des joueurs :', err);
            res.status(500).json({ error: 'Erreur lors de la recherche des joueurs' });
            return;
        }

        const players = results;
        const rankingQuery = 'SELECT COUNT(*) AS ranking FROM users WHERE win > ?';
        let playersWithRanking = [];

        players.forEach((player, index) => {
            pool.query(rankingQuery, [player.win], (err, rankingResults) => {
                if (err) {
                    console.error('Erreur lors du calcul du classement du joueur :', err);
                    res.status(500).json({ error: 'Erreur lors du calcul du classement du joueur' });
                    return;
                }

                const ranking = rankingResults[0].ranking + 1; // Ajouter 1 pour obtenir le rang du joueur
                const playerWithRanking = { ...player, ranking: ranking };

                playersWithRanking.push(playerWithRanking);

                if (index === players.length - 1) {
                    console.log(playersWithRanking);
                    res.json(playersWithRanking);
                }
            });
        });
    });
};
