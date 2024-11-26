const express = require('express');
const router = express.Router();
const User = require('../models/User'); // Adjust the path to your User model

// Route to display all registered users
router.get('/people', async (req, res) => {
    try {
        // Fetch all users from the database
        const users = await User.find();
        res.render('people', { users }); // Pass users to the template
    } catch (error) {
        console.error('Error fetching users:', error);
        res.status(500).send('Internal Server Error');
    }
});

module.exports = router;
