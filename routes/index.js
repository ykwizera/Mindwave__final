const express = require('express');
const router = express.Router();
const bcrypt = require('bcrypt'); // For password hashing
const User = require('../models/user'); // Import your User schema

// Render views
router.get('/', (req, res) => res.render('home'));
router.get('/login', (req, res) => res.render('login'));
router.get('/signup', (req, res) => res.render('signup'));
router.get('/courses', (req, res) => res.render('courses'));
router.get('/csc', (req, res) => res.render('csc'));
router.get('/chem', (req, res) => res.render('chem'));
router.get('/biology', (req, res) => res.render('biology'));
router.get('/maths', (req, res) => res.render('maths'));
router.get('/geo', (req, res) => res.render('geo'));
router.get('/physics', (req, res) => res.render('physics'));

// Dashboard route - Accessible only to logged-in users
router.get('/dashboard', (req, res) => {
    if (!req.session.user) {
        return res.redirect('/login');
    }
    res.render('dashboard', { user: req.session.user });
});

// People route - Fetch and display all users
router.get('/people', async (req, res) => {
    try {
        // Fetch all registered users from the database
        const users = await User.find({}, 'firstName lastName schoolName profession phone email');
        
        // Render the 'people.ejs' view and pass the users
        res.render('people', { users });
    } catch (error) {
        console.error('Error fetching users:', error.message);

        // Handle errors gracefully
        res.status(500).send('Error fetching users: ' + error.message);
    }
});

// Signup route
router.post('/signup', async (req, res) => {
    const { first_name, last_name, email, password, profession, school_name, phone } = req.body;

    try {
        // Hash the password for security
        const hashedPassword = await bcrypt.hash(password, 10);

        // Create a new user instance
        const newUser = new User({
            firstName: first_name,
            lastName: last_name,
            email,
            password: hashedPassword,
            profession,
            schoolName: school_name,
            phone
        });

        await newUser.save();
        res.redirect('/login');
    } catch (error) {
        res.status(500).send('Signup failed: ' + error.message);
    }
});

// Login route
router.post('/login', async (req, res) => {
    const { email, password } = req.body;

    try {
        const user = await User.findOne({ email });
        if (!user) {
            return res.status(400).send('Invalid email or password');
        }

        // Compare entered password with hashed password in DB
        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) {
            return res.status(400).send('Invalid email or password');
        }

        // Save user to session and redirect to dashboard
        req.session.user = user;
        res.redirect('/dashboard');
    } catch (error) {
        res.status(500).send('Login failed: ' + error.message);
    }
});

// Logout route
router.get('/logout', (req, res) => {
    req.session.destroy(err => {
        if (err) {
            console.log('Error destroying session:', err);
            return res.status(500).send('Could not log out');
        }
        console.log('Session destroyed');
        res.redirect('/login'); // Redirect to login after logout
    });
});

module.exports = router;
