const qrcode = require('qrcode-terminal');
const { Client, LocalAuth } = require('whatsapp-web.js');

const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: { args: ['--no-sandbox'] }
});

client.on('qr', qr => {
    qrcode.generate(qr, { small: true });
});

client.initialize();

client.on('loading', (percent, message) => {
    console.log('Carregando', percent, message);
});

client.on('authenticated', () => {
    console.log('Autenticado');
});

client.on('auth_failure', msg => {
    console.error('Falha na autenticacao', msg);
});

client.on('ready', async () => {
    console.log('Cliente iniciado e pronto para uso!');
    try {
        const chats = await client.getChats();
        console.log("List of groups:");
        chats.forEach(chat => {
            if (chat.isGroup) {
                console.log(chat.name, chat.id._serialized);
            }
        });
    } catch (error) {
        console.error('Erro ao obter os chats:', error);
    }
});

client.on('message', async (msg) => {
    // Lógica para processar mensagens recebidas
    console.log('Mensagem recebida:', msg.body);
});

client.on('group_join', (notification) => {
    console.log('Grupo ingressado:', notification.id._serialized);
});