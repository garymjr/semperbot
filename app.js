var fs = require('fs');
var datejs = require('datejs');
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
	// [day_number, day_name, [start_time], [end_time]]
	[4, 'thursday', [19, 0], [21, 0]],
	[6, 'saturday', [19, 0], [21, 0]]
];

var GUIDES = JSON.parse(fs.readFileSync('guides.json', 'utf8'));

var get_next = {
	sunday: function() {
		return Date.today().next().sunday();
	},
	monday: function() {
		return Date.today().next().monday();
	},
	tuesday: function() {
		return Date.today().next().tuesday();
	},
	wednesday: function() {
		return Date.today().next().wednesday();
	},
	thursday: function() {
		return Date.today().next().thursday();
	},
	friday: function() {
		return Date.today().next().friday();
	},
	saturday: function() {
		return Date.today().next().saturday();
	}
};

function mention(user_id) {
	return '<@!' + user_id + '>';
}

function get_time(arr) {
	var today, date;
	today = Date.today();
	if (today.getDay() !== arr[0]) {
		date = get_next[arr[1]]();
	}
	return [date.setHours(arr[2][0], arr[2][1]), date.setHours(arr[3][0], arr[3][1])];
}

bot.on('ready', function(event) {
	console.log('Logged in as %s - %s\n', bot.username, bot.id);
});

bot.on('message', function(user, userID, channelID, message, event) {
	var text, keys, result, date, today;
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
		today = Date.today();
		for (i=0; i < RAID_TIMES.length; i++) {
			date = new Date(get_time(RAID_TIMES[i])[0]);
			if (today.getDay() === date.getDay() && today.getTime() < date.getTime()) {
				break;
			} else if (today.getDay() < date.getDay()) {
				break;
			}
		}
		seconds = (today.getTime() - date.getTime()) / 1000;
		hours = seconds / 3600;
		minutes = (seconds % 3600) / 60;
		bot.sendMessage({
			to: channelID,
			message: mention(userID) + ' Next raid in ' + hours + ' hour(s) and ' + minutes + ' minute(s).'
		});
	} else if (message[0] === '!times') {
		text = '';
		for (i=0; i < RAID_TIMES.length; i++) {
			times = get_time(RAID_TIMES[i]);
			start = new Date(times[0]);
			end = new Date(times[1]);
			text += RAID_TIMES[i][1].charAt(0).toUpperCase() + RAID_TIMES[i][1].slice(1) + ': ' + start.getHours() + ':' + start.getMinutes() + ' - ' + end.getHours() + ':' + end.getMinutes() + '\n';
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
