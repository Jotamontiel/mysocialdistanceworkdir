function update_values(temp1, temp2, volts){
  $("#display_temp1").html(temp1);
  $("#display_temp2").html(temp2);
  $("#display_volt").html(volts);
}

/* Fernando Values Begin */
function update_values_fer(value_1, value_2, value_3, value_4, value_5){
  $("#display_value_1").html(value_1);
  $("#display_value_2").html(value_2);
  $("#display_value_3").html(value_3);
  $("#display_value_4").html(value_4);
  $("#display_value_5").html(value_5);
}
/* Fernando Values end */

function process_msg(topic, message){
  // ej: "10,11,12"
  if (topic == "values") {
    var msg = message.toString();
    var sp = msg.split(",");
    var temp1 = sp[0];
    var temp2 = sp[1];
    var volts = sp[2];
    update_values(temp1, temp2, volts);
  }
}

/* Fernando Values Begin */
function process_msg_fer(topic, message){
  // ej: "10,11,12,13,14"
  if (topic == "values_fer") {
    var msg = message.toString();
    var sp = msg.split(",");
    var value_1 = sp[0];
    var value_2 = sp[1];
    var value_3 = sp[2];
    var value_4 = sp[3];
    var value_5 = sp[4];
    update_values_fer(value_1, value_2, value_3, value_4, value_5);
  }
}
/* Fernando Values end */

function process_led1(){
  if ($('#input_led1').is(":checked")) {
    console.log("Encendido");
    
    client.publish('led1', 'on', (error) => {
      console.log(error || 'Mensaje enviado !!')
    })
  }else{
    console.log("Apagado");

    client.publish('led1', 'off', (error) => {
      console.log(error || 'Mensaje enviado !!')
    })
  }
}

function process_led2(){
  if ($('#input_led2').is(":checked")) {
    console.log("Encendido");
    
    client.publish('led2', 'on', (error) => {
      console.log(error || 'Mensaje enviado !!')
    })
  }else{
    console.log("Apagado");

    client.publish('led2', 'off', (error) => {
      console.log(error || 'Mensaje enviado !!')
    })
  }
}

// connection option
const options = {
  clean: true, // retain session
  connectTimeout: 4000, // Timeout period
  // Authentication information
  clientId: 'Client_user_'+ Math.round(Math.random() * (0-10000) * -1),
  username: 'jorge_1',
  password: 'jorgeuser3',

  // keepalive: 60,

}

// Connect string, and specify the connection method by the protocol
// ws Unencrypted WebSocket connection
// wss Encrypted WebSocket connection
// mqtt Unencrypted TCP connection
// mqtts Encrypted TCP connection
// wxs WeChat applet connection
// alis Alipay applet connection edition
const connectUrl = 'wss://socialdistance.cl:8084/mqtt'
const client = mqtt.connect(connectUrl, options)

client.on('connect', () => {
    console.log('Mqtt conectado por WS! Exito!')

    // subscribe(topic, qos, options/callback)
    client.subscribe('values', { qos: 0 }, (error) => {
      if (!error){
        console.log('Suscripción exitosa!')
      }else{
        console.log('Suscripción fallida!')
      }
    })

    /* Fernando Values Begin */
    // subscribe(topic, qos, options/callback)
    client.subscribe('values_fer', { qos: 0 }, (error) => {
      if (!error){
        console.log('Suscripción exitosa a canal de Fernando!')
      }else{
        console.log('Suscripción fallida a canal de Fernando!')
      }
    })
    /* Fernando Values end */

    // publish(topic, payload, options/callback)
    client.publish('fabrica', 'esto es un verdadero exito', (error) => {
      console.log(error || 'Mensaje enviado !!')
    })
})

var total_cicles = 50;
var chart_data = [];
var chart_data_temp2 = [];
var chart_data_volt = [];
var updateIntervalChart = 1000;
var chart_now = new Date().getTime();

/* Fernando Values Begin */
var chart_value_1 = [];
var chart_value_2 = [];
var chart_value_3 = [];
var chart_value_4 = [];
var chart_value_5 = [];
/* Fernando Values end */

client.on('message', (topic, message) => {
  console.log('Mensaje recibido bajo el tópico ', topic,' -> ', message.toString())
  process_msg(topic, message);

  if (chart_data.length < total_cicles ) {
    if (topic == "values") {
      var mesag = message.toString();
      var spe = mesag.split(",");
      var temp_chart1 = parseInt(spe[0]);
      var temp_chart2 = parseInt(spe[1]);
      var volt_chart = parseInt(spe[2]);
      var tempo = [chart_now += updateIntervalChart, temp_chart1];
      var tempo2 = [chart_now += updateIntervalChart, temp_chart2];
      var volto = [chart_now += updateIntervalChart, volt_chart];
      chart_data.push(tempo);
      chart_data_temp2.push(tempo2);
      chart_data_volt.push(volto);
      
      var dataset_chart = [
        { 
          data: chart_data,
          points: { show: true, radius: 1}, 
          splines: { show: true, tension: 0.45, lineWidth: 0, fill: 0.4} 
        }
      ];

      var dataset_chart2 = [
        { 
          data: chart_data_temp2,
          points: { show: true, radius: 1}, 
          splines: { show: true, tension: 0.45, lineWidth: 0, fill: 0.4} 
        }
      ];

      var dataset_chart3 = [
        { 
          data: chart_data_volt,
          points: { show: true, radius: 1}, 
          splines: { show: true, tension: 0.45, lineWidth: 0, fill: 0.4} 
        }
      ];

      var options_chart = {
        colors: ['#c20c0c'],
        series: { shadowSize: 3 },
        xaxis: { show: true, font: { color: '#ccc' }, position: 'bottom' },
        yaxis:{ show: true, font: { color: '#ccc' }, min:1},
        grid: { hoverable: true, clickable: true, borderWidth: 0, color: 'rgba(120,120,120,0.5)' },
        tooltip: true,
        tooltipOpts: { content: '%x.0 is %y.4',  defaultTheme: false, shifts: { x: 0, y: -40 } }
      };

      var options_chart2 = {
        colors: ['#e3da27'],
        series: { shadowSize: 3 },
        xaxis: { show: true, font: { color: '#ccc' }, position: 'bottom' },
        yaxis:{ show: true, font: { color: '#ccc' }, min:1},
        grid: { hoverable: true, clickable: true, borderWidth: 0, color: 'rgba(120,120,120,0.5)' },
        tooltip: true,
        tooltipOpts: { content: '%x.0 is %y.4',  defaultTheme: false, shifts: { x: 0, y: -40 } }
      };

      var options_chart3 = {
        colors: ['#12c20c'],
        series: { shadowSize: 3 },
        xaxis: { show: true, font: { color: '#ccc' }, position: 'bottom' },
        yaxis:{ show: true, font: { color: '#ccc' }, min:1},
        grid: { hoverable: true, clickable: true, borderWidth: 0, color: 'rgba(120,120,120,0.5)' },
        tooltip: true,
        tooltipOpts: { content: '%x.0 is %y.4',  defaultTheme: false, shifts: { x: 0, y: -40 } }
      };

      $.plot($("#placeholder1"), dataset_chart, options_chart);
      $.plot($("#placeholder2"), dataset_chart2, options_chart2);
      $.plot($("#placeholder3"), dataset_chart3, options_chart3);

      if (chart_data.length == total_cicles){
        chart_data.shift();
        chart_data_temp2.shift();
        chart_data_volt.shift();
      }
    }
  }

  /* Fernando Values Begin */
  if (chart_value_1.length < total_cicles ) {
    if (topic == "values_fer") {
      var mesag = message.toString();
      var spe = mesag.split(",");
      var temp_value_1 = parseInt(spe[0]);
      var temp_value_2 = parseInt(spe[1]);
      var temp_value_3 = parseInt(spe[2]);
      var temp_value_4 = parseInt(spe[3]);
      var temp_value_5 = parseInt(spe[4]);
      var tempo1 = [chart_now += updateIntervalChart, temp_value_1];
      var tempo2 = [chart_now += updateIntervalChart, temp_value_2];
      var tempo3 = [chart_now += updateIntervalChart, temp_value_3];
      var tempo4 = [chart_now += updateIntervalChart, temp_value_4];
      var tempo5 = [chart_now += updateIntervalChart, temp_value_5];
      chart_value_1.push(tempo1);
      chart_value_2.push(tempo2);
      chart_value_3.push(tempo3);
      chart_value_4.push(tempo4);
      chart_value_5.push(tempo5);

      var dataset_chart_1 = [
        { 
          data: chart_value_1,
          points: { show: true, radius: 1}, 
          splines: { show: true, tension: 0.45, lineWidth: 0, fill: 0.4} 
        }
      ];

      var dataset_chart_2 = [
        { 
          data: chart_value_2,
          points: { show: true, radius: 1}, 
          splines: { show: true, tension: 0.45, lineWidth: 0, fill: 0.4} 
        }
      ];

      var dataset_chart_3 = [
        { 
          data: chart_value_3,
          points: { show: true, radius: 1}, 
          splines: { show: true, tension: 0.45, lineWidth: 0, fill: 0.4} 
        }
      ];

      var dataset_chart_4 = [
        { 
          data: chart_value_4,
          points: { show: true, radius: 1}, 
          splines: { show: true, tension: 0.45, lineWidth: 0, fill: 0.4} 
        }
      ];

      var dataset_chart_5 = [
        { 
          data: chart_value_5,
          points: { show: true, radius: 1}, 
          splines: { show: true, tension: 0.45, lineWidth: 0, fill: 0.4} 
        }
      ];

      var options_chart_1 = {
        colors: ['#c20c0c'],
        series: { shadowSize: 3 },
        xaxis: { show: true, font: { color: '#ccc' }, position: 'bottom' },
        yaxis:{ show: true, font: { color: '#ccc' }, min:1},
        grid: { hoverable: true, clickable: true, borderWidth: 0, color: 'rgba(120,120,120,0.5)' },
        tooltip: true,
        tooltipOpts: { content: '%x.0 is %y.4',  defaultTheme: false, shifts: { x: 0, y: -40 } }
      };

      var options_chart_2 = {
        colors: ['#e3da27'],
        series: { shadowSize: 3 },
        xaxis: { show: true, font: { color: '#ccc' }, position: 'bottom' },
        yaxis:{ show: true, font: { color: '#ccc' }, min:1},
        grid: { hoverable: true, clickable: true, borderWidth: 0, color: 'rgba(120,120,120,0.5)' },
        tooltip: true,
        tooltipOpts: { content: '%x.0 is %y.4',  defaultTheme: false, shifts: { x: 0, y: -40 } }
      };

      var options_chart_3 = {
        colors: ['#12c20c'],
        series: { shadowSize: 3 },
        xaxis: { show: true, font: { color: '#ccc' }, position: 'bottom' },
        yaxis:{ show: true, font: { color: '#ccc' }, min:1},
        grid: { hoverable: true, clickable: true, borderWidth: 0, color: 'rgba(120,120,120,0.5)' },
        tooltip: true,
        tooltipOpts: { content: '%x.0 is %y.4',  defaultTheme: false, shifts: { x: 0, y: -40 } }
      };

      var options_chart_4 = {
        colors: ['#12c20c'],
        series: { shadowSize: 3 },
        xaxis: { show: true, font: { color: '#ccc' }, position: 'bottom' },
        yaxis:{ show: true, font: { color: '#ccc' }, min:1},
        grid: { hoverable: true, clickable: true, borderWidth: 0, color: 'rgba(120,120,120,0.5)' },
        tooltip: true,
        tooltipOpts: { content: '%x.0 is %y.4',  defaultTheme: false, shifts: { x: 0, y: -40 } }
      };

      var options_chart_5 = {
        colors: ['#12c20c'],
        series: { shadowSize: 3 },
        xaxis: { show: true, font: { color: '#ccc' }, position: 'bottom' },
        yaxis:{ show: true, font: { color: '#ccc' }, min:1},
        grid: { hoverable: true, clickable: true, borderWidth: 0, color: 'rgba(120,120,120,0.5)' },
        tooltip: true,
        tooltipOpts: { content: '%x.0 is %y.4',  defaultTheme: false, shifts: { x: 0, y: -40 } }
      };

      $.plot($("#placeholderfer1"), dataset_chart_1, options_chart_1);
      $.plot($("#placeholderfer2"), dataset_chart_2, options_chart_2);
      $.plot($("#placeholderfer3"), dataset_chart_3, options_chart_3);
      $.plot($("#placeholderfer4"), dataset_chart_4, options_chart_4);
      $.plot($("#placeholderfer5"), dataset_chart_5, options_chart_5);

      if (chart_value_1.length == total_cicles){
        chart_value_1.shift();
        chart_value_2.shift();
        chart_value_3.shift();
        chart_value_4.shift();
        chart_value_5.shift();
      }
    }
  }
  /* Fernando Values end */

})

client.on('reconnect', (error) => {
    console.log('reconnecting:', error)
})

client.on('error', (error) => {
    console.log('Connection failed:', error)
})

/*Dynamic Chart*/
var data = [];
var dataset;
var totalPoints = 500;
var updateInterval = 1000;
var now = new Date().getTime();
function GetData() {
data.shift();
while (data.length < totalPoints) {    
    var y = Math.random() * 100;
    var temp = [now += updateInterval, y];
    data.push(temp);
}
}
var options_del = {
colors: ['#0cc2aa'],
series: { shadowSize: 3 },
xaxis: { show: true, font: { color: '#ccc' }, position: 'bottom' },
yaxis:{ show: true, font: { color: '#ccc' }, min:1},
grid: { hoverable: true, clickable: true, borderWidth: 0, color: 'rgba(120,120,120,0.5)' },
tooltip: true,
tooltipOpts: { content: '%x.0 is %y.4',  defaultTheme: false, shifts: { x: 0, y: -40 } }
};
$(document).ready(function mytesting () {
GetData();
dataset = [
    { 
    data: data,
    points: { show: true, radius: 1}, 
    splines: { show: true, tension: 0.45, lineWidth: 0, fill: 0.4} 
    }
];
$.plot($("#placeholder"), dataset, options_del);
function update() {
    GetData();
    $.plot($("#placeholder"), dataset, options_del)
    setTimeout(update, updateInterval);
}
update();
});