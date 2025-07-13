var app = require('express')();
var http = require('http');
var server = http.Server(app)
var io = require('socket.io')(server);
var port = process.env.PORT || 3000;

const URL_BOTESUS = "http://localhost:6000/resposta/";
const CONFIANCA_MINIMA = 0.65;

app.get('/', function (req, res) {
  res.sendFile(__dirname + '/index.html');
});

getResposta = (mensagem) => {
  let dados = "";

  http.get(URL_BOTESUS + encodeURIComponent(mensagem), (resposta) => {
    resposta.on("data", (pedaco) => {
      dados += pedaco;
    });

    resposta.on("end", () => {
      dados = JSON.parse(dados);
      console.log(dados);
      
      if (dados.confianca >= CONFIANCA_MINIMA) {
        // Verificar se a resposta contém coordenadas
        var coordenadasMatch = dados.resposta.match(/Latitude\s*([-\d.,]+)[,\s]*Longitude\s*([-\d.,]+)/i);
        if (coordenadasMatch) {
          // Extrair coordenadas e nome do estabelecimento
          var lat = parseFloat(coordenadasMatch[1].replace(',', '.'));
          var lon = parseFloat(coordenadasMatch[2].replace(',', '.'));
          var nome = "Estabelecimento"
          console.log(`Coordenadas: ${lat}, ${lon} - Nome: ${nome}`);
          
          // Enviar resposta com coordenadas para criar mapa
          io.emit('chat message', {
            coordenadas: { lat: lat, lon: lon },
            nome: nome,
            texto: dados.resposta
          });
        } else {
          // Resposta normal de texto
          io.emit('chat message', "🤖 " + dados.resposta);
        }
      } else {
        io.emit('chat message', "🤖 Desculpe, não encontrei informações sobre esse estabelecimento de saúde. Verifique o nome e tente novamente.");
      }
    });
  }).on('error', (err) => {
    console.error('Erro na requisição:', err);
    io.emit('chat message', "🤖 Desculpe, ocorreu um erro interno. Tente novamente em alguns instantes.");
  });
}

io.on('connection', function (socket) {
  socket.on('chat message', function (msg) {
    getResposta(msg);
  });
});

server.listen(port, function () {
  console.log('BoteSUS Chat listening on *:' + port);
});
