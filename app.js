var fs = require('fs');
var Discord = require('discord.io');
var bot = new Discord.Client({
	autorun: true,
	token: ''
});

var COMMANDS = [
	'!help',
	'!next',
	'!times',
	'!guides',
	'!videos',
	'!code'
];

var RAID_TIMES = [
	{
		'day': 'Thursday',
		'start': '10PM',
		'end': '12AM'
	},
	{
		'day': 'Saturday',
		'start': '10PM',
		'end': '12AM'
	}
];

var GUIDES = JSON.parse(fs.readFileSync('guides.json', 'utf8'));

function mention(user_id) {
	return '<@!' + user_id + '>';
}

bot.on('ready', function(event) {
	console.log('Logged in as %s - %s\n', bot.username, bot.id);
});

bot.on('message', function(user, userID, channelID, message, event) {
	var text, keys, result;
	message = message.split(' ');
	var d = event.d;
	console.log({
		'author': d.author.id,
		'user_id': userID,
		'channel_id': channelID,
		'content': message
	});

	if (message[0] === '!help') {
		for (i=0; i < COMMANDS.length; i++) {
			text += COMMANDS[i] + ', ';
		}
		bot.sendMessage({
			to: channelID,
			message: mention(userID) + ' Available commands: ' + text.slice(0, -2)
		});
	} else if (message[0] === '!next') {
		var date, seconds, days, hours, minutes;
		var today = new Date();
		if (today.getDay() === 4 || today.getDay() === 6) {
			date = new Date();
			date.setHours(19, 0, 0);
			seconds = (date.getTime() - today.getTime()) / 1000;
			days = Math.floor(seconds / 86400);
			hours = Math.floor((seconds % 86400) / 3600);
			minutes = Math.floor(((seconds % 86400) % 3600) / 60);
		} else if (today.getDay() === 5) {
			date = new Date();
			date.setDate(date.getDate() + 1);
			date.setHours(19, 0, 0);
			seconds = (date.getTime() - today.getTime()) / 1000;
			days = Math.floor(seconds / 86400);
			hours = Math.floor((seconds % 86400) / 3600);
			minutes = Math.floor(((seconds % 86400) % 3600) / 60);
		} else if (today.getDay() < 4) {
			var offset = 4 - today.getDay();
			date = new Date();
			date.setDate(date.getDate() + offset);
			date.setHours(19, 0, 0);
			seconds = (date.getTime() - today.getTime()) / 1000;
			days = Math.floor(seconds / 86400);
			hours = Math.floor((seconds % 86400) / 3600);
			minutes = Math.floor(((seconds % 86400) % 3600) / 60);
		}
		bot.sendMessage({
			to: channelID,
			message: mention(userID) + ' Next raid in ' + days + ' day(s) ' + hours + ' hour(s) and ' + minutes + ' minute(s).'
		});
	} else if (message[0] === '!times') {
		text = '';
		for (i=0; i < RAID_TIMES.length; i++) {
			text += RAID_TIMES[i].day + ': ' + RAID_TIMES[i].start + ' - ' + RAID_TIMES[i].end + '\n';
		}
		bot.sendMessage({
			to: channelID,
			message: mention(userID) + ' Current raid times are: (All times using server time)\n' + text
		});
	} else if (message[0] === '!guides') {
		text = '';
		keys = Object.keys(GUIDES);
		if (message.length === 1) {
			for (i=0; i < keys.length; i++) {
				text += keys[i] + ', ';
			}
			bot.sendMessage({
				to: channelID,
				message: mention(userID) + ' Guides available for ' + text.slice(0, -2)
			});
		} else {
			result = [];
			search = message[1].toLowerCase();
			for (i=0; i < keys.length; i++) {
				if (keys[i].indexOf(search) !== -1) {
					result.push(keys[i]);
				}
			}

			if (result.length >= 1) {
				for (i=0; i < result.length; i++) {
					bot.sendMessage({
						to: channelID,
						message: GUIDES[result[i]].guide
					});
				}
			}
		}
	} else if (message[0] === '!videos') {
		text = '';
		keys = Object.keys(GUIDES);
		if (message.length === 1) {
			for (i=0; i < keys.length; i++) {
				if (GUIDES[keys[i]].video !== '') {
					text += keys[i] + ', ';
				}
			}
			bot.sendMessage({
				to: channelID,
				message: mention(userID) + ' Videos available for ' + text.slice(0, -2)
			});
		} else {
			result = [];
			search = message[1].toLowerCase();
			for (i=0; i < keys.length; i++) {
				if (keys[i].indexOf(search) !== -1 && GUIDES[keys[i]].video !== '') {
					result.push(keys[i]);
				}
			}

			if (result.length >= 1) {
				for (i=0; i < result.length; i++) {
					bot.sendMessage({
						to: channelID,
						message: GUIDES[result[i]].video
					});
				}
			}
		}
	} else if (message[0] === '!code') {
		bot.sendMessage({
			to: channelID,
			message: mention(userID) + ' https://github.com/garymjr/semperbot'
		});
	} else if (message[0] === '!ilovehunters') {
		bot.sendMessage({
			to: channelID,
			message: mention('207175112691023872') + ' I heard you love hunters!'
		});
	} else if (message[0] === '!poe') {
		bot.sendMessage({
			to: channelID,
			message: mention('125071902556291072') + ' tap tap tap'
		});
	}
});
