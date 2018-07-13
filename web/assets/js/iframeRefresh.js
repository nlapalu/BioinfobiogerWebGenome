// on ne sélectionne que les liens appartenant aux boutons "btn"
var links = document.getElementsByClassName('btn') ;
var frame = document.getElementById('webpage') ;
for (var i = 0 ; i < links.length ; ++i) {
    // Au clique sur ces liens 
    links[i].onclick = function() {
      frame.src = this.href; // On change l'attribut src de l'image en le remplaçant par la valeur du lien
      frame.alt = this.title; // On change son titre
      return false; //inhibe l'action réelle du lien
    };
  }