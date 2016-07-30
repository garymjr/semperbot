var Discord = require('discord.io');
var bot = new Discord.Client({
	autorun: true,
	token: ''
});

var COMMANDS = [
	'!help',
	'!times'
];

function mention(user_id) {
	return '<@!' + user_id + '>';
}

bot.on('ready', function(event) {
	console.log('Logged in as %s - %s\n', bot.username, bot.id);
});

bot.on('message', function(user, userID, channelID, message, event) {
	var d = event['d'];
	console.log({
		'author': d['author'].id,
		'user_id': userID,
		'channel_id': channelID,
		'content': message
	});
	if (message === '!help') {
		bot.sendMessage({
			to: channelID,
			message: mention(userID) + " I'm not very helpful right now"
		});
	} else if (message === '!poe') {
		bot.sendMessage({
			to: channelID,
			message: mention('125071902556291072') + ' tap tap tap '
		});
	} else if (message === '!times') {
		var date, seconds, hours, minutes;
		var today = new Date();
		if (today.getDay() === 4 || today.getDay === 6) {
			date = new Date();
			date.setHours(19, 0, 0);
			seconds = (date.getTime() - today.getTime()) / 1000;

			// get hours
			if (seconds >= 3600) {
				hours = Math.floor(seconds / 3600);
			} else {
				hours = 0;
			}

			// get minutes
			minutes = Math.floor((seconds % 3600) / 60)
		} else if (today.getDay() === 5) {
			date = new Date();
			date.setDate(date.getDate() + 1);
			date.setHours(19, 0, 0);
			seconds = (date.getTime() - today.getTime()) / 1000;
			hours = Math.floor(seconds / 3600);
			minutes = Math.floor((seconds % 3600) / 60);
		} else if (today.getDate() < 4) {
			var offset = 4 - today.getDay();
			date = new Date();
			date.setDate(date.getDate() + offset);
			date.setHours(19, 0, 0);
			seconds = (date.getTime() - today.getTime()) / 1000;
			hours = Math.floor(seconds / 3600);
			minutes = Math.floor((seconds % 3600) / 60);
		}
		bot.sendMessage({
			to: channelID,
			message: mention(userID) + 'Next raid in ' + hours + ' hours and ' + minutes + ' minutes.'
		});
	} else if (message === '!ilovehunters') {
		bot.sendMessage({
			to: channelID,
			message: '<@!207175112691023872> I heard you love hunters!'
		});
	}
});
