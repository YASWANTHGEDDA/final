// test-email.js (place this file in D:\AI\chat-bot\server)
const { sendEmail } = require('./services/emailService');

sendEmail('y8330988896@gmail.com', 'Test Email', 'This is a test email from your AI project.')
  .then(() => console.log('Email sent!'))
  .catch(console.error);