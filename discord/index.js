const {Client, GatewayIntentBits, Partials} = require("discord.js");
const axios = require("axios");
const repl = require("repl");

const CLIENT_SECRET = process.env.CLIENT_SECRET;

const API_URL = process.env.API_URL || "http://server:8000";

// Check if the message contains "stacc" and text within backticks
function checkMessageForStacc(message) {
    const content = message.content;
    const containsStacc = content.includes("stacc");
    const regexCheck = /`([^`]*)`/;
    const containsBacktickText = regexCheck.test(content);
    return containsStacc && containsBacktickText;
}

// Extract text inside backticks
const extractCode = (content) => {
    const regexCheck = /`([^`]*)`/;
    const match = regexCheck.exec(content);
    return match ? match[1] : null;
};

// Execute the stacc command
const executeStacc = async (message) => {
    try {
        const code = extractCode(message.content);
        if (!code) {
            await message.reply("No valid code found in the message.");
            return;
        }

        // Send initial response
        await message.channel.send(`Executing: \`${code}\``);

        // Send request to Flask API
        const response = await axios.post(`${API_URL}/execute`, {
            instructions: code
        });

        // Format and send the response
        const result = response.data;
        let replyMessage = "Results:\n";

        // Add printed output if any exists
        if (result.prints && result.prints.length > 0) {
            replyMessage += "Printed output:\n```\n" + result.prints.join("\n") + "\n```\n";
        }

        // Add final stack state
        replyMessage += `Final stack state: ${result.final_stack}`;
        await message.reply(replyMessage);

    } catch (error) {
        console.error("Error executing stack:", error);
        const errorMessage = error.response?.data?.error || error.message;
        await message.reply(`Error: ${errorMessage}`);
    }
};

// Initialize the Discord client
const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent
    ],
    partials: [Partials.Channel]
});

client.on("ready", () => {
    console.log("Bot is ready!");
});

client.on("messageCreate", async (message) => {
    if (message.author.bot) return;

    if (checkMessageForStacc(message)) {
        await executeStacc(message);
    }
});

client.login(CLIENT_SECRET).catch((err) => {
    console.error("Failed to login:", err);
});