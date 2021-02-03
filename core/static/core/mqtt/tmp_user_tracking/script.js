var url = window.location.href;
var match = url.match(/tmpClient_(\d+)/);
if (match) {
    var tmpClientUser = 'tmpClient_'+ match[1];
} else {
    var tmpClientUser = 'tmpClient_'+ Math.round(Math.random() * (0-10000) * -1);
}
function addTmpUserToLink(id) {
    var anchor = document.getElementById(id);
    anchor.href = anchor.href+"?"+tmpClientUser;
}
const options = {
    clean: true,
    connectTimeout: 4000,
    clientId: tmpClientUser,
    username: 'jorge_1',
    password: 'jorgeuser3',
    // keepalive: 60,
}
const connectUrl = 'wss://socialdistance.cl:8084/mqtt'
const client = mqtt.connect(connectUrl, options)
client.on('connect', () => {
    console.log('Mqtt conectado por WSS! Exito!')
    client.subscribe('conn_channel', { qos: 0 }, (error) => {
        if (!error){
            console.log('Suscripción a conn_channel exitosa!')
        }else{
            console.log('Suscripción a conn_channel fallida!')
        }
    })
    user_number = tmpClientUser.match(/tmpClient_(\d+)/);
    user_section = document.title.split(" | ");
    console.log(user_section);
    client.publish('conn_channel', 'User '+user_number[1]+' en '+user_section[1], (error) => {
        console.log(error || 'Mensaje enviado !!')
    })
})
client.on('message', (topic, message) => {
    console.log('Mensaje recibido bajo el tópico ', topic,' -> ', message.toString())
})
client.on('reconnect', (error) => {
    console.log('reconnecting:', error)
})
client.on('error', (error) => {
    console.log('Connection failed:', error)
})