const express = require('express');
const router = express.Router();

router.get('/', (req, res) => res.render('home'));
router.get('/login', (req, res) => res.render('login'));
router.get('/signup', (req, res) => res.render('signup'));
router.get('/dashboard', (req, res) => res.render('dashboard'));
router.get('/courses', (req, res) => res.render('courses'));
router.get('/people', (req, res) => res.render('people'));
router.get('/csc', (req, res) => res.render('csc'));
router.get('/chem', (req, res) => res.render('chem'));
router.get('/biology', (req, res) => res.render('biology'));
router.get('/maths', (req, res) => res.render('maths'));
router.get('/geo', (req, res) => res.render('geo'));
router.get('/physics', (req, res) => res.render('physics'));

module.exports = router;
