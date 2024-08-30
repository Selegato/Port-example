//console animation
function consoleText(words, id, colors) {
  if (colors === undefined) colors = ["#fff"];
  var visible = true;
  var con = document.getElementById("console");
  var letterCount = 1;
  var x = 1;
  var waiting = false;
  var target = document.getElementById(id);

  var langWords =
    lang === "en" ? words.en : lang === "pt-br" ? words.pt : words.uk;

  target.setAttribute("style", "color:" + colors[0]);
  window.setInterval(function () {
    if (letterCount === 0 && waiting === false) {
      waiting = true;
      target.innerHTML = langWords[0].substring(0, letterCount);
      window.setTimeout(function () {
        var usedColor = colors.shift();
        colors.push(usedColor);
        var usedWord = langWords.shift();
        langWords.push(usedWord);
        x = 1;
        target.setAttribute("style", "color:" + colors[0]);
        letterCount += x;
        waiting = false;
      }, 1000);
    } else if (letterCount === langWords[0].length + 1 && waiting === false) {
      waiting = true;
      window.setTimeout(function () {
        x = -1;
        letterCount += x;
        waiting = false;
      }, 1000);
    } else if (waiting === false) {
      target.innerHTML = langWords[0].substring(0, letterCount);
      letterCount += x;
    }
  }, 120);

  window.setInterval(function () {
    if (visible === true) {
      con.className = "console-underscore hidden";
      visible = false;
    } else {
      con.className = "console-underscore";
      visible = true;
    }
  }, 300);
}

const words = {
  en: ["Understanding your problems", "Creating Solutions"],
  pt: ["Entendendo seus problemas", "Criando Soluções"],
  uk: ["Розуміння ваших проблем", "Створення рішень"],
};

consoleText(words, "text", ["white"]);
//END console animation
