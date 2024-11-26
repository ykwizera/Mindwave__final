const express = require('express');
const router = express.Router();
const bcrypt = require('bcrypt'); 
const User = require('../models/user'); 

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

router.get('/dashboard', (req, res) => {
    if (!req.session.user) {
        return res.redirect('/login');
    }
    res.render('dashboard', { user: req.session.user });
});

router.get('/people', async (req, res) => {
    try {
        const users = await User.find({}, 'firstName lastName schoolName profession phone email');
 
        res.render('people', { users });
    } catch (error) {
        console.error('Error fetching users:', error.message);

        res.status(500).send('Error fetching users: ' + error.message);
    }
});

router.post('/signup', async (req, res) => {
    const { first_name, last_name, email, password, profession, school_name, phone } = req.body;

    try {
        const hashedPassword = await bcrypt.hash(password, 10);

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

router.post('/login', async (req, res) => {
    const { email, password } = req.body;

    try {
        const user = await User.findOne({ email });
        if (!user) {
            return res.status(400).send('Invalid email or password');
        }

        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) {
            return res.status(400).send('Invalid email or password');
        }

        req.session.user = user;
        res.redirect('/dashboard');
    } catch (error) {
        res.status(500).send('Login failed: ' + error.message);
    }
});

router.get('/logout', (req, res) => {
    req.session.destroy(err => {
        if (err) {
            console.log('Error destroying session:', err);
            return res.status(500).send('Could not log out');
        }
        console.log('Session destroyed');
        res.redirect('/login'); 
    });
});

module.exports = router;
