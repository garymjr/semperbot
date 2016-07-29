var Discord = require('discord.io');
var bot = new Discord.Client({
	autorun: true,
	token: ''
});

var COMMANDS = [
	'!help',
	'!times'
];

bot.on('ready', function(event) {
	console.log('Logged in as %s - %s\n', bot.username, bot.id);
});

bot.on('message', function(user, userID, channelID, message, event) {
	console.log([user, userID, channelID, message, event]);
	if (message === '!help') {
		bot.sendMessage({
			to: channelID,
			message: "<@!" + userID + "> I'm not very helpful right now"
		});
	} else if (message === '!poe') {
		bot.sendMessage({
			to: channelID,
			message: '<@!125071902556291072> tap tap tap'
		});
	} else if (message === '!times') {
		date = new Date();
		today = date.getDay();
		if (today < 6) {
			offset = 6 - today;
			next = new Date();
			next.setDate(date.getDate() + offset);
			next.setHours(19, 0, 0);
			time = (next - date) / 1000;
			hours = Math.round((time / 60) / 60);
			minutes = Math.round((time / 60) - (hours * 60));
			bot.sendMessage({
				to: channelID,
				message: '<@!' + userID + '> The next raid is in ' + hours + ' hours and ' + minutes + ' minutes'
			});
		}
	} else if (message === '!ilovehunters') {
		bot.sendMessage({
			to: channelID,
			message: '<@!207175112691023872> I heard you love hunters!'
		});
	}
});
