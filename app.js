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
	'!videos'
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

var GUIDES = [
	{
		'zone': 'Blackrock Foundry',
		'url': 'http://www.icy-veins.com/wow/blackrock-foundry-raid'
	},
	{
		'zone': 'Hellfire Citadel',
		'url': 'http://www.icy-veins.com/wow/hellfire-citadel-raid'
	}
];

var VIDEOS = [
	{
		'zone': 'Blackrock Foundry',
		'url': 'https://www.youtube.com/playlist?list=PLu3dsh6Bc2HXtv2OQWOwbgiwiTk9s14Ij'
	},
	{
		'zone': 'Hellfire Citadel',
		'url': 'https://www.youtube.com/playlist?list=PLu3dsh6Bc2HUuZ0BleQ-YMCQAmCFs5eyo'
	}
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
		var text = '';
		for (i=0; i < COMMANDS.length; i++) {
			text += COMMANDS[i] + ', ';
		}
		bot.sendMessage({
			to: channelID,
			message: mention(userID) + ' Available commands: ' + text
		});
	} else if (message === '!next') {
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
			message: mention(userID) + ' Next raid in ' + hours + ' hours and ' + minutes + ' minutes.'
		});
	} else if (message === '!times') {
		var text = '';
		for (i=0; i < RAID_TIMES.length; i++) {
			text += RAID_TIMES[i]['day'] + ': ' + RAID_TIMES[i]['start'] + ' - ' + RAID_TIMES[i]['end'] + '\n';
		}
		bot.sendMessage({
			to: channelID,
			message: mention(userID) + ' Current raid times are: (All times using server time)\n' + text
		});
	} else if (message === '!guides') {
		var text = '';
		for (i=0; i < GUIDES.length; i++) {
			text += 'Zone: ' + GUIDES[i]['zone'] + '\nLink: ' + GUIDES[i]['url'] + '\n'
		}
		bot.sendMessage({
			to: channelID,
			message: mention(userID) + ' Guides we use:\n' + text
		});
	} else if (message === '!videos') {
		var text = '';
		for (i=0; i < VIDEOS.length; i++) {
			text += 'Zone: ' + VIDEOS[i]['zone'] + '\nLink: ' + VIDEOS[i]['url'] + '\n'
		}
		bot.sendMessage({
			to: channelID,
			message: mention(userID) + ' Videos we watch:\n' + text
		});
	} else if (message === '!ilovehunters') {
		bot.sendMessage({
			to: channelID,
			message: mention('207175112691023872') + ' I heard you love hunters!'
		});
	} else if (message === '!poe') {
		bot.sendMessage({
			to: channelID,
			message: mention('125071902556291072') + ' tap tap tap '
		});
	}
});
