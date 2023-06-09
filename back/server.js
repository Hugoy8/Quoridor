const express = require('express');
const cors = require('cors');
const playerRoutes = require('./routes/playerRoutes');
const authRoutes = require('./routes/authRoutes');
const userRoutes = require('./routes/userRoutes');

const app = express();

app.use(cors());
app.use(express.json());

app.use('/api', playerRoutes);
app.use('/api', authRoutes);
app.use('/api', userRoutes);


// Gestionnaire d'erreur
app.use((err, req, res, next) => {
    console.error('Erreur non gérée :', err);
    res.status(500).json({ error: 'Erreur interne du serveur' });
});

// Démarrage du serveur
const port = process.env.PORT || 10000;
app.listen(port, () => {
    console.log(`Serveur démarré sur le port ${port}`);
});