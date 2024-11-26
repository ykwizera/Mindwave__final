// models/user.js
const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
    firstName: { type: String, required: true },
    lastName: { type: String, required: true },
    email: { type: String, required: true, unique: true },
    password: { type: String, required: true },
    profession: { type: String },
    schoolName: { type: String },
    phone: { type: String },
});

module.exports = mongoose.model('User', userSchema);
